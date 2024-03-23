from xml.etree import ElementTree
import base64

import pandas as pd

from entity.http import EncodeModule
from entity.http.HttpClass import Http
from entity.http.UrlClass import Url
from service.HttpServiceClass import HttpService

"""
http日志读写，目前是针对burp的三种格式进行读取
"""


class HttpLog:
    def __init__(self):
        # http服务层对象，逐个读取写入
        self.httpService = HttpService()
        # 日志文件路径
        self.filePath = ''

    def read(self, filePath: str):
        # 读取日志文件
        with open(file=filePath, mode='r', encoding='iso-8859-1') as f:
            s = f.read()
        self.filePath = filePath
        # 创建接收对象
        http_list = list()
        try:
            # burp的分隔符格式
            if s.startswith('======================================================'):
                http_list = self.read_burp_separator()
            # burp的xml格式
            elif s.startswith('<'):
                http_list = self.read_burp_xml()
            # 分隔符的csv格式
            elif s.startswith('ID,'):
                http_list = self.read_burp_csv()
        except Exception as e:
            print(e)
        return http_list

    def read_burp_separator(self):
        # 分隔符
        sep = '======================================================'
        # 读取日志文件字节
        with open(file=self.filePath, mode='rb') as f:
            bytes_value = f.read()
        # 分割为http单元的字节数据
        unit_list = bytes_value.split(('\r\n'+sep+'\r\n\r\n\r\n\r\n').encode('utf-8'))
        # 待赋值的http对象列表
        http_list = list()
        # 遍历处理http单元文本
        for unit in unit_list:
            http = Http()
            if len(unit) > 0:
                try:
                    # 分割为信息行、请求报文和响应报文
                    split = unit.split(sep.encode('utf-8'))
                    # 信息行处理，去掉首尾的\r\n
                    info_row = EncodeModule.decode(split[1][2:-2])
                    info_row_split = info_row.split('  ')
                    # 信息行元素0为发送时间
                    http.send_time = info_row_split[0]
                    # 信息行元素1为url
                    http.u = Url(info_row_split[1])
                    # 信息行元素2如果存在，为ip
                    if len(info_row_split) == 3:
                        http.id = info_row_split[2][2:-2]

                    if len(split) == 4:
                        request_message = split[2][2:-2]
                        response_message = split[3][2:]
                        http.set_byReqMessage(request_message)
                        http.set_byResMessage(response_message)
                    elif len(split) == 3:
                        request_message = split[2][2:]
                        response_message = None
                        http.set_byReqMessage(request_message)
                        http.set_byResMessage(response_message)
                    else:
                        print('异常')

                    http_list.append(http)
                except Exception as e:
                    print(e)
        return http_list

    """
    time，表示时间，cst格式
    url，
    host，例如static.deepl.com，该节点还具有一个属性ip
    port
    protocol，例如https
    method
    path
    extension，扩展名
    request，请求报文的base64编码
    status 状态码，例如200
    responseLength，响应报文的字符长度，包括\r
    mimetype 例如XML
    response 响应报文的base64编码
    comment 备注信息

    以上字段只关注部分，其它用不到或者信息冗余
    """
    def read_burp_xml(self):
        xml = ElementTree.parse(self.filePath)
        items = xml.getroot()
        http_list = list()
        index = 0
        for i in range(len(items)):
            http = Http()
            item = items[i]
            # url
            http.u = Url(item.find('url').text)
            # 设置ip
            http.ip = item.find('host').get('ip')
            # 请求报文，该值是base64编码，解码为字节后交给Http方法处理
            request_message = base64.b64decode(item.find('request').text)
            http.set_byReqMessage(request_message)
            # 响应报文，该值是base64编码，解码为字节后交给Http方法处理
            response_message = base64.b64decode(item.find('response').text)
            http.set_byResMessage(response_message)
            http_list.append(http)
        return http_list

    """
    ID,Time,Tool,Method,Protocol,Host,Port,URL,IP,Path,Query,Param count,Param names,Status code,Length,MIME type,
    Extension,Page title,Start response timer,End response timer,Comment,Connection ID,Request,Response

    以上字段只关注部分，其它用不到或者信息冗余
    """
    def read_burp_csv(self):
        df = pd.read_csv(self.filePath)
        http_list = list()
        for i in range(df.shape[0]):
            try:
                http = Http()
                # 请求的发送时间
                http.send_time = df.loc[i]['Time']
                # 响应时延，为0表示不确定
                http.wait_time = 0
                # 设置url
                http.u = Url(df.loc[i]['URL'])
                # ip
                http.ip = df.loc[i]['IP']
                # 请求报文，该值是base64编码，解码为字节后交给Http方法处理
                request_message = base64.b64decode(df.loc[i]['Request'])
                http.set_byReqMessage(request_message)
                # 响应报文，该值是base64编码，解码为字节后交给Http方法处理
                response_message = base64.b64decode(df.loc[i]['Response'])
                http.set_byResMessage(response_message)
                # 标记目前来说没有严格分析定义，暂时来说指明http来源
                http.mark = '[burp][%s][%s]' % (self.filePath, df.loc[i]['ID'])
                http_list.append(http)
            except Exception as e:
                # 输出处理异常的项，以及异常原因
                print(i, e)
        return http_list
