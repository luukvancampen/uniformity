table_system = {
    "role": "system",
    "content": ("You get two database tables as input, formatted as JSON."
                "You will determine whether the concepts represented by the tables are the same."
                "To know at what level of abstraction the tables should be compared, you are provided with a list of concepts that indicates the required level of abstraction. If you think the concepts are the same, say \"yes\", else say \"no\"."
                "Concepts: "
                "       - wifi configuration"
                "       - email"
                "       - emails from specific mail clients"
                "       - chat messages")
}

columns_same_meaning = {
    "role": "system",
    "content": (
        "You get two database columns as input, ."
        "You will determine whether the columns have a similar meaning."
        "Columns mean the same if they contain the same kind of data and represent the same kind of thing."
        "- if you are not confident in the decision, return only unsure."
        "- if you think the columns are semantically similar, return only yes. "
        "- if you think the columns are not semantically similar, return only no"
        "The following are examples of columns that are similar. You can use this to understand the level of abstraction at which to determine whether columns are similar."
        "Message_sent_timestamp and sent_timestamp"
        "Mail_content and message_content"
        "Wifi network name and SSID")
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
               'If the database table contains a column with similar semantics as the column provided to you as input, say yes. If not say no. If you can not make a decision, say unsure..'
               # 'Examples of columns that are similar:'
               # ' - Message_sent_timestamp and sent_timestamp'
               # ' - Mail_content and message_content'
               # ' - Wifi network name and SSID'
}


structural_syntactic_sim_2 = {
    'role' : 'system',
    'content':  'Task Description:'
                'You will receive two lines of input, each containing a value. Your task is to determine whether the two values share the same syntactic structure.'
                ' - If the values have the same syntactic structure, respond only with "yes".'
                ' - If the values do not have the same syntactic structure, respond only with "no".'
                ' - If you can not decide, as a fallback, you can respond with "unsure". Try to always respond with "yes" or "no".'
                'Syntactic Structure Definition:'
                'The syntactic structure refers to the format, pattern, or notation used to represent a value.'
                'examples of non-similar syntax:'
                ' - epoch vs human-readable timestamp'
                ' - ipv-4 vs ipv-6'
                ' - windows filepaths vs unix filepaths'
}