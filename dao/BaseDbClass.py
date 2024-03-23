import pymysql
from pymysql.cursors import Cursor


class BaseDb:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = '123456'
        self.database = 'http_scan'
        self.port = 3306

        # 连接对象
        self.conn: pymysql.Connection = None
        # 浮标
        self.cursor: Cursor = None
        # 受影响行数
        self.effect_row_count = -1

    def init_conn(self):
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                    port=self.port)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    def execute(self, sql: str, args: list = None, close_flag=True):
        self.init_conn()
        if args is None:
            args = tuple()
        self.cursor: Cursor
        self.effect_row_count = self.cursor.execute(sql, args=args)
        self.conn: pymysql.Connection
        self.conn.commit()
        if close_flag:
            self.close()

    """
    形如insert into table_name (%s, create_time) value (%s, now())
    """
    def insert(self, sql, dict_value:dict):
        s1, s2 = '', ''
        key_list, value_list = list(dict_value.keys()), list(dict_value.values())
        for i in range(len(key_list)):
            if i != 0:
                s1 = s1 + ','
                s2 = s2 + ','
            s1 = s1 + key_list[i]
            s2 = s2 + '%s'
        sql = sql % (s1, s2)
        try:
            self.execute(sql=sql, args=value_list)
            return self.cursor.lastrowid
        except Exception as e:
            print(e)
