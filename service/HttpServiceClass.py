from dao.HttpDbClass import HttpDb
from entity.http.HttpClass import Http

"""
tb_http的服务层
"""


class HttpService:
    def __init__(self):
        self.httpDb = HttpDb()

    def insert(self, http: Http):
        return self.httpDb.insert(http)

    def select(self, id: int):
        return self.httpDb.select(id)

    def select_list(self):
        return self.httpDb.select_list()

    def select_list_bySql(self, sql: str):
        return self.httpDb.select_list_bySql(sql)

    def truncate(self):
        self.httpDb.truncate()

