from helpers.general_helpers import files_to_tables
from uniformity import compute_structural_semantic_uniformity, compute_high_level_syntactic_uniformity, compute_low_level_syntactic_uniformity, \
    compute_high_level_semantic_uniformity, compute_low_level_semantic_uniformity, compute_structural_syntactic_uniformity


if __name__ == '__main__':
    print("Uniformity!")

    tables = files_to_tables("./input/")
    columns = []
    for table in tables:
        columns.extend(table.columns)

    # ________________________________________________
    # high_level_syntactic_uniformity = compute_high_level_syntactic_uniformity(tables)
    # low_level_syntactic_uniformity = compute_low_level_syntactic_uniformity(columns)
    # high_level_semantic_uniformity = compute_high_level_semantic_uniformity(tables)
    low_level_semantic_uniformity = compute_low_level_semantic_uniformity(tables)
    # structural_syntactic_uniformity = compute_structural_syntactic_uniformity(columns)
    # structural_semantic_uniformity = compute_structural_semantic_uniformity(columns)

    # print(f'High level syntactic: {high_level_syntactic_uniformity}')
    # print(f'Low level syntactic: {low_level_syntactic_uniformity}')
    # print(f'High level semantic: {high_level_semantic_uniformity}')
    print(f'Low level semantic: {low_level_semantic_uniformity}')
    # print(f'structural syntactic: {structural_syntactic_uniformity}')
    # print(f'Structural semantic: {structural_semantic_uniformity}')
    # uniformity_sum = high_level_syntactic_uniformity + low_level_syntactic_uniformity + high_level_semantic_uniformity + low_level_semantic_uniformity + structural_semantic_uniformity + structural_syntactic_uniformity
    # print(f'Average: {uniformity_sum / 6}')
    # ________________________________________________
