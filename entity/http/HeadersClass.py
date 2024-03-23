import requests

from entity.base.PropertiesClasses import Properties

"""
http头部字段
对应http请求或响应的头部字段
"""


class Headers(Properties):
    def __init__(self, data_obj=None):
        super().__init__()
        self.sep1 = '\n'
        self.sep2 = ':'
        self.value_strip_flag = True
        self.name_ignoreCase_flag = True

        if type(data_obj) == requests.structures.CaseInsensitiveDict:
            for name, value in data_obj.items():
                self.add(name=str(name), value=str(value))
        elif type(data_obj) == str and data_obj != '':
            self.parse(data_obj)