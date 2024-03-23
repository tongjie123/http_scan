import re

from entity.http.ParamsClass import Params

'''
url对象
'''


class Url:
    def __init__(self, s=''):
        # 协议名称，一般为http://或https://
        self.schema = ''
        # 主机名称，可能包含用户名和密码部分，可能是ip、域名或者是localhost
        self.hostname = ''
        # 端口，可能不存在。如果存在，为:8080形式
        self.port = ''
        # 路径，可能不存在。如果存在，为/a/b/c形式
        self.path = ''
        # 直接参数，可能不存在。如果存在，为?name=&password=形式
        self.query = ''
        # fragment，可能不存在。如果存在，为#123456形式
        self.fragment = ''

        """
        一方面，由parse解析，确定是否正常解析。另一方面，调用check方法，检查各部分是否合法
        """
        self.parse(s=s)

    def parse(self, s: str):
        if s != '':
            pattern = '^([a-zA-Z]+://)([^:/?#\\s]+)(:[0-9]*)?(/[^?#]*)?([?][^#]*)?(#\\S*)?'
            result = re.findall(pattern=pattern, string=s)
            if result:
                self.set_url(result[0])
                return

    def set_url(self, args):
        self.schema = args[0]
        self.hostname = args[1]
        self.port = args[2]
        self.path = args[3]
        self.query = args[4]
        self.fragment = args[5]

    def check(self):
        # 协议检查
        if self.schema.lower() not in ['http://', 'https://']:
            return False
        # 用户名和密码检查
        if ':' in self.hostname:
            if '@' not in self.hostname:
                return False
            else:
                if self.hostname.index(':') > self.hostname.index('@'):
                    return False
        # 端口范围检查
        if self.port != '':
            try:
                port = int(self.port)
                if port < 0 or port > 65535:
                    return False
            except Exception as e:
                print(e)
                return False
        return True

    """
    完整的url
    """
    def toString(self):
        return self.schema + self.hostname + self.port + self.path + self.query + self.fragment

    def toString_toPort(self):
        return self.schema + self.hostname + self.port

    def toString_toPath(self):
        return self.toString_toPort() + self.path

    def toString_toQuery(self):
        return self.toString_toPath() + self.query

    """
    克隆
    """
    def clone(self):
        u = Url()
        u.set_url([self.schema, self.hostname, self.port, self.path, self.query, self.fragment])
        return u

    """
    获取主域名的开始和结束索引
    分割host域名，返回list[int, int]。前者表示主域名的开始索引，后者表示顶级域名的开始索引
    """
    def split_domainName(self):
        # 按.拆分
        split = self.hostname.split('.')
        # 判断顶级域名所占位
        top_list = ['.com.cn', '.edu.cn', '.gov.cn']
        top_bit = 1
        for i in range(len(top_list)):
            if self.hostname.endswith(top_list[i]):
                top_bit = 2
                break
        # 顶级域名
        temp = ''
        for i in range(top_bit):
            temp = split[-i - 1] + temp
        index_1 = len(self.hostname)
        index_2 = index_1 - len(temp)
        index_3 = index_2 - len(split[-top_bit - 1])
        result = [index_2, index_3]

        return result

    """
    将一个url进行分解，元素0包括协议、域名、端口信息，路径按/进行分割，不包括参数部分
    """

    def address_arr(self):
        result = [self.schema + self.hostname + self.port]
        if self.path != '':
            result.extend(self.path.split('/')[1:])
        return result

    """
    自动标记
    """

    def mark(self):
        # 如果存在直接参数，则对其标记
        if len(self.query) > 1:
            return self.mark_query()
        # 不存在直接参数，但存在路径参数，则该部分标记
        elif len(self.path) > 1 and '.' not in self.path:
            return self.mark_path()
        return []

    def mark_query(self):
        index_list = list()
        if len(self.query) > 1:
            params = Params(self.query)
            index_list = params.markValues()
            # 还需要记录前缀长度
            x = len(self.toString_toPath())
            for i in range(len(index_list)):
                index_list[i] = x + index_list[i]
        return index_list

    def mark_path(self):
        index_list = list()
        if len(self.path) > 1:
            # 还需要记录前缀长度
            x = len(self.toString_toPort())
            arr = self.path.split('/')
            temp = x + 2
            for i in range(1, len(arr)):
                if arr[i] != '':
                    index_list.append(temp)
                    temp = temp + len(arr[i])
                    index_list.append(temp)
                    # /字符
                    temp = temp + 1

        return index_list


def is_url(string: str):
    u = Url(string)
    return u.check()

if __name__ == '__main__':
    print('abc')
    u = Url('https://gitee.com?a=bc&name=')
    print(u.mark())
    print(len(u.toString_toPort()))