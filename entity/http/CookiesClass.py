from entity.base.PropertiesClasses import Properties

"""
cookie集合
对应http请求中cookies字段的值
"""


class Cookies(Properties):
    def __init__(self, data_obj=None):
        super().__init__()
        self.sep1 = ';'
        self.sep2 = '='
        self.value_strip_flag = True
        self.name_ignoreCase_flag = False

        self.parse(data_obj)