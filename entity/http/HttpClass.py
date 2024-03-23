from entity.http import EncodeModule
from entity.http.UrlClass import Url

"""
tb_http表对象
"""


class Http:
    def __init__(self, args=None):
        self.id = -1
        self.method = ''
        self.url = ''
        self.u = Url()
        self.ip = ''
        self.headers_string = ''
        self.body = ''
        # 为1表示文本，为0表示非文本
        self.body_text_flag = 0
        self.status_code = ''
        self.reason = ''
        self.res_headers_string = ''
        self.res_body = ''
        self.res_headers_string_len = 0
        self.res_body_len = 0
        # 为1表示文本，为0表示非文本
        self.res_body_text_flag = 0
        self.content_type = ''
        self.send_time = ''
        self.wait_time = -1
        self.mark = ''

        # 暂时不考虑写入数据表，作为输出报文时的默认值
        self.protocol_version = 'HTTP/1.1'

        if args is not None:
            self.set_byArgs(args)

    """
    基于list数据
    """

    def set_byArgs(self, args: list):
        if type(args) == list or type(args) == tuple and len(args) == 23:
            self.id = args[0]
            self.method = args[1]
            self.url = args[2]
            self.u.schema = args[3]
            self.u.hostname = args[4]
            self.u.port = args[5]
            self.u.path = args[6]
            self.u.query = args[7]
            self.ip = args[8]
            self.headers_string = args[9]
            self.body = args[10]
            self.body_text_flag = args[11]
            self.status_code = args[12]
            self.reason = args[13]
            self.res_headers_string = args[14]
            self.res_body = args[15]
            self.res_headers_string_len = args[16]
            self.res_body_len = args[17]
            self.res_body_text_flag = args[18]
            self.content_type = args[19]
            self.send_time = args[20]
            self.wait_time = args[21]
            self.mark = args[22]

    """
    基于url
    """

    def set_byUrl(self, url: str):
        self.url = url
        self.u = Url(url)

    """
    基于请求报文
    """
    def set_byReqMessage(self, request_message):
        if type(request_message) == bytes and len(request_message)>0:
            # 有些场景中报文是不带\r\n，而是仅\n，比如ui读取或文件读取
            index = request_message.find('\r\n\r\n'.encode('utf-8'))
            index_2 = request_message.find('\n\n'.encode('utf-8'))
            if -1 < index < index_2 or index_2 == -1:
                split = request_message.split('\r\n\r\n'.encode('utf-8'), maxsplit=1)
            else:
                split = request_message.split('\n\n'.encode('utf-8'), maxsplit=1)
            if len(split) == 2:
                self.body, charset = EncodeModule.decode(split[1])
                if charset == 'iso-8859-1':
                    self.body_text_flag = 0
                else:
                    self.body_text_flag = 1
            s = split[0].decode('utf-8').replace('\r', '')
            split_2 = s.split('\n', maxsplit=1)
            if len(split_2) == 2:
                self.headers_string = split_2[1]
            split_3 = split_2[0].split(' ')
            self.method = split_3[0]
            self.protocol_version = split_3[2]
            # 基于报文请求，一般不关心url，会由直接url设置http

    """
    基于响应报文
    """

    def set_byResMessage(self, response_message):
        if type(response_message) == bytes and len(response_message) > 0:
            # 有些场景中报文是不带\r\n，而是仅\n，比如ui读取或文件读取
            index = response_message.find('\r\n\r\n'.encode('utf-8'))
            index_2 = response_message.find('\n\n'.encode('utf-8'))
            if -1 < index < index_2 or index_2 == -1:
                split = response_message.split('\r\n\r\n'.encode('utf-8'), maxsplit=1)
            else:
                split = response_message.split('\n\n'.encode('utf-8'), maxsplit=1)
            if len(split) == 2:
                self.res_body, charset = EncodeModule.decode(split[1])
                if charset == 'iso-8859-1':
                    self.res_body_text_flag = 0
                else:
                    self.res_body_text_flag = 1
            s = split[0].decode('utf-8').replace('\r', '')
            split_2 = s.split('\n', maxsplit=1)
            if len(split_2) == 2:
                self.res_headers_string = split_2[1]
            split_3 = split_2[0].split(' ')
            self.status_code = split_3[1]
            self.reason = split_3[2]

    """
    获取请求报文
    """

    def get_req_message(self):
        return '%s %s %s\n%s\n\n%s' % (
            self.method, self.u.path + self.u.query, self.protocol_version, self.headers_string, self.body)

    """
    获取响应报文
    """

    def get_res_message(self):
        return '%s %s %s\n%s\n\n%s' % (
            self.protocol_version, self.status_code, '', self.res_headers_string, self.res_body)
