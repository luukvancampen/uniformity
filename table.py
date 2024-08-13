import json


class table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns

    def to_json(self):
        query_dict = {
            "name": self.name,
            "columns": []
        }

        for col in self.columns:
            query_dict["columns"].append(col.to_json(2))

        return json.dumps(query_dict)

    def to_json_dict(self):
        query_dict = {
            "name": self.name,
            "columns": []
        }

        for col in self.columns:
            query_dict["columns"].append({col.name: col.data[:5]})
        return query_dict
