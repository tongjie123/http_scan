from dao.BaseDbClass import BaseDb
from entity.http.HttpClass import Http

"""
tb_http的dao层
"""


class HttpDb:
    def __init__(self):
        self.table_name = 'tb_http'
        self.baseDb = BaseDb()

    def insert(self, http: Http):
        dict_value = {'method': http.method, 'url': http.url, 'schema_string': http.u.schema, 'host': http.u.hostname,
                      'port': http.u.port, 'path': http.u.path, 'query': http.u.query, 'ip': http.ip,
                      'headers_string': http.headers_string, 'body': http.body, 'body_text_flag': http.body_text_flag,
                      'status_code': http.status_code, 'reason': http.reason,
                      'res_headers_string': http.res_headers_string, 'res_body': http.res_body,
                      'res_headers_string_len': http.res_headers_string_len, 'res_body_len': http.res_body_len,
                      'res_body_text_flag': http.res_body_text_flag,
                      'content_type': http.content_type, 'send_time': http.send_time, 'wait_time': http.wait_time,
                      'mark': http.mark}
        sql = 'insert into tb_http (%s) value (%s)'
        return self.baseDb.insert(sql=sql, dict_value=dict_value)

    def select(self, id: int):
        sql = 'select * from tb_http where id=%s'
        self.baseDb.execute(sql=sql, args=[id])
        result = self.baseDb.cursor.fetchone()
        if result is not None:
            return Http(result)
        return None

    def select_list(self):
        sql = 'select * from tb_http'
        self.baseDb.execute(sql=sql)
        result = self.baseDb.cursor.fetchall()
        http_list = list()
        for row in result:
            http_list.append(Http(row))
        return http_list

    def select_list_bySql(self, sql: str):
        self.baseDb.execute(sql=sql)
        result = self.baseDb.cursor.fetchall()
        http_list = list()
        for row in result:
            http_list.append(Http(row))
        return http_list

    def truncate(self):
        sql = 'truncate table %s' % self.table_name
        self.baseDb.execute(sql=sql)
