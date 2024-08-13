column_name_system = {
    "role": "system",
    "content": "You get two column names as input, separated by a new line."
               "- if the names are likely to mean the same, return yes"
               "- if the names are not likely to mean the same, return no"
               "- if you are unsure whether the names mean the same, return unsure"
}

table_system = {
    "role": "system",
    "content": ("You get two database tables as input, formatted as JSON."
                "You will determine whether the concepts represented by the tables are the same."
                "To know at what level of abstraction the tables should be compared, you are provided with a list of concepts that indicates the required level of abstraction. If you think the concepts are the same, say \"yes\", else say \"no\"."
                "Concepts: - wifi configuration"
                "       - email"
                "       - gps coordinate"
                "       - phone call")
}

columns_same_meaning = {
    "role": "system",
    "content": (
        "You get two database columns as input, ."
        "You will determine whether the columns have a similar meaning."
        "Columns mean the same if they contain the same kind of data and represent the same kind of thing."
        "- if you are not confident in the decision, return only unsure."
        "- if you think the columns are semantically similar, return only yes. "
        "- if you think the columns are not semantically similar, return only no")
}

type_similarity_system = {
    "role": "system",
    "content": (
        "You get two values. If the values represent the same kind of information, say only yes, otherwise, say only no."
        "Kinds of information that are similar are, for example:"
        "- timestamps"
        "- file paths ")
}

type_similarity_system_3 = {
    "role": "system",
    "content": (
        "You will receive two values. Determine whether these values represent the same kind of information, based on their content and purpose, not just their data type. "
        " - If they represent the same kind of information, respond with only 'yes'. "
        " - If they do not, respond with only 'no'. "
        " - If there is not enough information to determine this, respond with only 'unsure'. This option should be reserved for situations where there is really not enough information."
        "Examples of similar kinds of information include:"
        "Two timestamps (e.g., '2022-02-01 12:30:31.519732' and '2023-03-01 08:15:20')."
        "Two file paths (e.g., '/home/user/document.txt' and '/var/log/system.log')."
        "Two MAC addresses (e.g., 'e8:26:89:26:8c' and '4c:5e:c:7c:13:90')."
        "Note: Do not base your answer solely on the fact that both values might be strings or numbers; consider their actual meaning and context."
        "If you across natural text, it is only the same kind of information as other natural text. For example, timestamps and natural text are never the same kind of information."
    )
}

type_similarity_system_2 = {
    "role": "system",
    "content": (
        "determine whether the values in the 'data' field of the first object is of the same type as the that in the 'data' list of the second object. If so, say yes, if not, say no. If you are unsure, say unsure."
        "Distinguish, for example, between timestamps, email addresses, zipcodes, and names."
    )
}

syntax_similarity_system = {
    "role": "system",
    "content": (
        "You get two lines with values as input, formatted as JSON. The JSON objects represent columns from a database. If the syntactic structure of the values in the two columns is similar, say yes, otherwise, say no."
        "For example, distinguish between timestamps in different formats.")
}

structural_semantic_sim = {
    "role": "system",
    "content": (
        "You get two lines with values as input, formatted as JSON. The JSON objects represent columns from a database. The columns contain the same type of data, for example, timestamps, file paths, or phone numbers. If the values in the columns contain exactly the same amount of information, say yes, otherwise, say no."
        "For example, a timestamp format that includes a timezone contains more information than a timestampt that does not.")
}

structural_semantic_sim_2 = {
    "role": "system",
    "content": (
        'You get two values that represent the same kind of information as input, separated by a newline. If the values contain the exact same amount of information, return only yes. If they do not, return only no. If you are unsure, return only unsure.'
        'Examples of values that do NOT contain the same amount of information are: '
        '2024-08-13T15:30:00Z and 1691935800 do not contain the same amount of information because the first value includes a timezone.'
        'Input values:'
    )
}

low_level_semantic_sim = {
    "role": "system",
    "content": 'You get two lines of input. The first line is a JSON representation of a database column. It contains the name of the column and a sample of the data. The second line is a JSON representation of a database table. '
               'If the database table contains a column with similar semantics as the column provided to you as input, say yes. If not say no.'
}

structural_syntactic_sim = {
    'role': 'system',
    'content': 'As input, you get two lines. On each line, there is a value.'
               ' - if the values have the same syntactic structure, say only "yes".'
               ' - if the values do not have the same syntactic structure, say only "no".'
               'Examples of syntactic structures that are not similar are:'
               ' - timestamps in different notation: 2023-08-11T14:30:00Z and 1691766600'
}

structural_syntactic_sim_2 = {
    'role' : 'system',
    'content':  'Task Description:'
                'You will receive two lines of input, each containing a value. Your task is to determine whether the two values share the same syntactic structure.'
                ' - If the values have the same syntactic structure, respond only with "yes".'
                ' - If the values do not have the same syntactic structure, respond only with "no".'
                ' - If you can not decide, as a very last resort you can respond with "unsure". Try to always respond with "yes" or "no".'
                'Syntactic Structure Definition:'
                'The syntactic structure refers to the format, pattern, or notation used to represent a value. '
}