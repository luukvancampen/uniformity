import itertools
import json
import os
import pickle
import random
import threading

import api_communication
import prompts
from api_communication import DefaultConversationalHandler


# This method determines whether object belongs in a list. For example, it determines whether a column belongs in a group of other column,
# which is relevant when determining low-level semantic uniformity.
def object_belongs_in_list(handler, list, object, query, lock):
    list_item = random.choice(list)
    if query == "similar_type":
        comparison = list_item.to_json() + "\n" + object.to_json()
        return api_communication.match(handler, comparison, prompts.type_similarity_system, lock)
    if query == "structural_syntactic_uniformity":
        comparison = list_item.to_json() + "\n" + object.to_json()
        return api_communication.match(handler, comparison, prompts.syntax_similarity_system, lock)
    if query == "structural_semantic_uniformity":
        comparison = list_item.to_json() + "\n" + object.to_json()
        return api_communication.match(handler, comparison, prompts.structural_semantic_sim, lock)
    if query == "similar_table":
        table_message = list_item.to_json() + "\n" + object.to_json()
        return api_communication.match(handler, table_message, prompts.table_system, lock)
    if query == "low_level_syntactic":
        comparison = list_item.to_json() + "\n" + object.to_json()
        return api_communication.match(handler, comparison, prompts.columns_same_meaning, lock)


def object_belongs_in_list_map(similarity_map, object_list, _object):
    belongs = False
    for item in object_list:
        combination_hash = str(hash(item[0])) + str(hash(_object))
        belongs = belongs or similarity_map[combination_hash]

    return belongs


def construct_sub_map(combinations, result, handler, lock, prompt, dict_lock):
    for combination in combinations:
        comparison = combination[0].data[0] + "\n" + combination[1].data[0]
        api_result = api_communication.match(handler, comparison, prompt, lock)
        with dict_lock:
            result[str(hash(combination[0])) + str(hash(combination[1]))] = api_result


def parallel_construct_similarity_map(columns, prompt, n_threads=8):
    similarity_map = dict()
    all_combinations = list(itertools.combinations(columns, 2))
    thread_list = []
    input_lock = threading.Lock()
    dictionary_lock = threading.Lock()
    parts = list(divide_list(all_combinations, n_threads))
    for i in range(n_threads):
        handler = DefaultConversationalHandler()
        thread_list.append(threading.Thread(target=construct_sub_map, args=(parts[i], similarity_map, handler, input_lock, prompt, dictionary_lock,)))
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    return similarity_map


def table_contains_similar_column(handler, column, table, lock):
    comparison = column.to_json() + "\n" + table.to_json()
    return api_communication.match(handler, comparison, prompts.low_level_semantic_sim, lock)


def divide_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


# This method takes a list of sublists, and it assigns object to the sublist in which it belongs.
def assign_to_sublist(handler, group_list, object, query, lock):
    for sublist in group_list:
        if object_belongs_in_list(handler, sublist, object, query, lock):
            sublist.append(object)
            return group_list
    group_list.append([object])
    return group_list


def assign_to_sublist_map(similarity_map, group_list, _object):
    for sublist in group_list:
        if object_belongs_in_list_map(similarity_map, group_list, _object):
            sublist.append(_object)
            return group_list
    group_list.append([_object])
    return group_list


# This function takes a list of columns or tables, and it groups them according to a particular query.
def group(start_list, query, prompt, with_map=False):
    handler = DefaultConversationalHandler()
    group_list = []
    lock = threading.Lock()
    if with_map:
        if os.path.isfile('./similarity_dict' + query) and query != "structural_syntactic_similarity" and query != "structural_semantic_similarity":
            similarity_map = pickle.load(open('similarity_dict' + query, 'rb'))
        else:
            similarity_map = parallel_construct_similarity_map(start_list, prompt)
            pickle.dump(similarity_map, open('similarity_dict' + query, 'wb'))
    for _object in start_list:
        if len(group_list) == 0:
            group_list.append([_object])
            continue
        if with_map:
            group_list = assign_to_sublist_map(similarity_map, group_list, _object)
        else:
            group_list = assign_to_sublist(handler, group_list, _object, query, lock)
    return group_list


# This method takes a list of groups. For each group, it creates a pair structured as (number of objects in group, number of different names)
def group_list_name_count(object_group_list):
    pair_list = []
    for _group in object_group_list:
        name_list = set()
        for _object in _group:
            name_list.add(_object.name)
        pair_list.append((len(_group), len(name_list)))
    return pair_list


# structural syntactic uniformity is about values of the same datatype, such as timestamp or location, having the same syntactic structure.
# To compute this, we must first divide the columns into groups of columns that contain data of the same type, and secondly, divide those lists further into lists
# containing values that also have a similar syntactic structure.
def compute_structural_syntactic_uniformity(columns):
    # Step 1: group columns by whether they contain values of the same type.
    group_list = group(columns, "similar_type", prompts.type_similarity_system_3, True)

    # Step 2: further divide the columns by whether their syntactic structure is the same.
    subdivision = []
    for subgroup in group_list:
        subdivision.append(group(subgroup, "structural_syntactic_similarity", prompts.structural_syntactic_sim_2, True))
    average_total = 0
    for sublist in subdivision:
        average_total += 1 / len(sublist)
    return average_total / len(subdivision)


def compute_structural_semantic_uniformity(columns):
    # Step 1: group columns by whether they contain values of the same datatype
    group_list = group(columns, "similar_type", prompts.type_similarity_system_3, True)

    # Step 2: further divide the columns by whether the values contained within them contain the exact same amount of information
    subdivision = []
    for subgroup in group_list:
        subdivision.append(group(subgroup, "structural_semantic_similarity", prompts.structural_semantic_sim_2, True))

    average_total = 0
    for sublist in subdivision:
        average_total += 1 / len(sublist)
    return average_total / len(subdivision)


# Computing high-level syntactic uniformity means determining whether tables that have the same meaning, also have the same name.
# We do this by grouping tables by whether they have the same meaning and then determining whether all tables in a group have the same name.
def compute_high_level_syntactic_uniformity(tables):
    group_list = group(tables, "similar_table", prompt=None)
    dissimilar_sum = 0
    for pair in group_list_name_count(group_list):
        dissimilar_sum += pair[1]
    return len(group_list) / dissimilar_sum


# Low-level syntactic uniformity means that columns that have the same meaning, also have the same name. The first step in computing it is
# grouping columns by whether they have the same meaning, the second step is determining whether they are named the same.
def compute_low_level_syntactic_uniformity(columns):
    group_list = group(columns, "low_level_syntactic", prompts.columns_same_meaning)
    set_list = []
    for sub_list in group_list:
        subset = set()
        for _object in sub_list:
            subset.add(_object.name)
        set_list.append((len(sub_list), len(subset)))

    print(set_list)
    badness = 0
    for subset in set_list:
        badness += 1 / len(subset)
    return badness / len(set_list)


# Low-level semantic uniformity means semantically similar concepts having similar properties. This means that tables representing
# similar concepts also have similar columns.
def compute_low_level_semantic_uniformity(tables):
    # Group similar tables....
    grouping = group(tables, "similar_table", prompt=None)
    group_with_missing = []
    subgroup_uniformity = []
    for subgroup in grouping:
        total_missing = 0
        columns_in_permutation = 0
        if len(subgroup) > 1:
            print(subgroup)
            permutations = list(itertools.permutations(subgroup, 2))
            print(permutations)
            for permutation in permutations:
                columns_in_permutation += len(permutation[0].columns) + len(permutation[1].columns)
                total_missing += count_missing_columns(permutation[0], permutation[1])
        group_with_missing.append((columns_in_permutation, total_missing))
        if columns_in_permutation > 0:
            subgroup_uniformity.append(1 - (total_missing / columns_in_permutation))
    return subgroup_uniformity


def count_missing_columns(table1, table2):
    handler = DefaultConversationalHandler()
    missing_column_counter = 0
    lock = threading.Lock()
    for _column in table1.columns:
        print(_column.to_json() + " in " + table2.to_json())
        if not table_contains_similar_column(handler, _column, table2, lock):
            missing_column_counter += 1
    return missing_column_counter


def compute_high_level_semantic_uniformity(tables):
    abstraction_level_set = set()

    for table in tables:
        print(f'Domain expert, what is the level of abstraction of the following table?')
        print(json.dumps(table.to_json_dict(), indent=2))
        level = input('Input level: ')
        abstraction_level_set.add(level)
    return 1 / len(abstraction_level_set)
