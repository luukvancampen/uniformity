import hashlib
import json


class column:
    def __init__(self, name, data, table_name):
        self.table_name = table_name
        self.name = name
        self.data = data

    def __key__(self):
        return tuple((self.name, str(len(self.data))))

    def __hash__(self):
        key_str = str(self.__key__()).encode('utf-8')
        # Use hashlib to produce a consistent hash value
        return int(hashlib.md5(key_str).hexdigest(), 16)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def to_small_string(self):
        return f'{self.table_name} {self.name}: {self.data[:3]}'

    def to_json(self, data_size=2):
        _dict = {
            "name": self.table_name + ' ' + self.name,
            "data": []
        }

        for dat in self.data[:data_size]:
            _dict["data"].append(dat)

        return json.dumps(_dict)

    def type_sample(self, data_size=4):
        sample_list = self.data[:data_size]
        return_sample_list = []
        for sample in sample_list:
            return_sample_list.append(str(sample))
        return str(return_sample_list)
