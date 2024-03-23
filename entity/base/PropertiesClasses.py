"""
属性值对集合
"""


class Properties:
    def __init__(self, data_obj=''):
        # 属性值对list，元素为[str, str]
        self.property_list = list()
        # 值对与值对之间的分隔符
        self.sep1 = ''
        # 属性名称与值之间的分隔符
        self.sep2 = ''
        # 是否对value去除首尾空白字符，仅用于判断值而不用于分割操作
        self.value_strip_flag = False
        # 是否对name忽略大小写
        self.name_ignoreCase_flag = False

    """
    清除所有元素
    """
    def clear(self):
        self.property_list.clear()

    """
    基于字符串解析
    """
    def parse(self, data_obj):
        self.clear()
        if type(data_obj) == str and data_obj != '':
            split = data_obj.split(self.sep1)
            for i in range(len(split)):
                if self.sep2 in split[i]:
                    nameValue = split[i].split(self.sep2, maxsplit=1)
                    self.add(name=nameValue[0], value=nameValue[1])

    """
    获取大小
    """
    def size(self):
        return len(self.property_list)

    """
    添加元素
    """
    def add(self, name: str, value: str):
        self.property_list.append([name, value])

    """
    字符串化
    """
    def toString(self):
        if self.size() == 0:
            return ''
        else:
            s = self.property_list[0][0] + self.sep2 + self.property_list[0][1]
            for i in range(1, self.size()):
                s = s + self.sep1 + self.property_list[i][0] + self.sep2 + self.property_list[i][1]
            return s

    """
    克隆
    """
    def clone(self):
        # 创建克隆对象，类型是Properties或其子类
        clone_obj = type(self)()
        # list的copy是浅克隆，但是这里list的元素都是list，所以不能直接用
        for i in range(self.size()):
            clone_obj.add(name=self.property_list[i][0], value=self.property_list[i][1])
        return clone_obj

    """
    根据当前规则判断两个name是否相等
    """
    def name_equals(self, name: str, name_2: str):
        if name == name_2 or (self.name_ignoreCase_flag and name.lower() == name_2.lower()):
            return True
        return False

    """
    @first_flag: bool类型，为True表示仅对第一个匹配项操作
    @add_flag: bool类型，为True表示当name不存在已知项时，直接添加
    """

    def update(self, name: str, value: str, first_flag=False, add_flag=False):
        update_count = 0
        for i in range(self.size()):
            if self.name_equals(name=name, name_2=self.property_list[i][0]):
                self.property_list[i][0] = name
                self.property_list[i][1] = value
                update_count = update_count + 1
                if first_flag:
                    return
        if add_flag and update_count == 0:
            self.add(name=name, value=value)

    def remove(self, name: str, first_flag=False):
        property_list = list()
        remove_count = 0
        for i in range(self.size()):
            if self.name_equals(name=name, name_2=self.property_list[i][0]):
                if not first_flag or (first_flag and remove_count == 0):
                    remove_count = remove_count + 1
                    continue
            property_list.append([self.property_list[i][0], self.property_list[i][1]])
        self.property_list = property_list

    def getValue(self, name: str, default=''):
        for i in range(self.size()):
            if self.name_equals(name=name, name_2=self.property_list[i][0]):
                return self.property_list[i][1]
        return default

    def getValueList(self, name: str=None):
        value_list = list()
        for i in range(self.size()):
            if name is None or self.name_equals(name=name, name_2=self.property_list[i][0]):
                value_list.append(self.property_list[i][1])
        return value_list

    def getNameList(self):
        value_list = list()
        for i in range(self.size()):
            value_list.append(self.property_list[i][0])
        return value_list

    def hasName(self, name: str):
        for i in range(self.size()):
            if self.name_equals(name=name, name_2=self.property_list[i][0]):
                return True
        return False

    def markValues(self):
        index_list = list()
        if self.size() > 0:
            name = self.property_list[0][0]
            value = self.property_list[0][1]
            x = len(name) + len(self.sep2)
            index_list.append(x)
            x = x + len(value)
            index_list.append(x)
            for i in range(1, self.size()):
                x = x + len(self.sep1)
                name = self.property_list[i][0]
                value = self.property_list[i][1]
                x = x + len(name) + len(self.sep2)
                index_list.append(x)
                x = x + len(value)
                index_list.append(x)
        return index_list

    """
    字典化
    需要注意的是该机制会对name自动去重
    """
    def to_dict(self):
        d = {}
        for i in range(self.size()):
            d.update({self.property_list[i][0]: self.property_list[i][1]})