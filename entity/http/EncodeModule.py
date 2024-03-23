
"""
返回解码后的文本和解码方案
"""


def decode(content: bytes):
    for charset in ['utf-8', 'gbk', 'gb2312', 'iso-8859-1']:
        try:
            s = content.decode(charset)
            return s, charset
        except Exception as e:
            print(e)
            continue
