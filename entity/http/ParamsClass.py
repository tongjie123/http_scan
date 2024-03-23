from entity.base.PropertiesClasses import Properties

"""
对应的是url直接参数
有时也可以视为请求体部中格式之一
"""


class Params(Properties):
    def __init__(self, data_obj=None):
        super().__init__()
        self.sep1 = '&'
        self.sep2 = '='
        self.value_strip_flag = False
        self.name_ignoreCase_flag = False

        self.parse(data_obj)