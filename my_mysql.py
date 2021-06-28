
from typing import Sequence
import pymysql


class MyMysql():

    def __init__(self, db_host, db_port, db_name, db_user, db_password) -> None:
        self.db_host = db_host 
        self.db_port = db_port 
        self.db_name = db_name 
        self.db_user = db_user 
        self.db_password = db_password

        self.conn = pymysql.connect(
            host = self.db_host,
            port = self.db_port,
            user = self.db_user,
            password = self.db_password,
            database = self.db_name,
            charset='UTF8',
            autocommit=True,    # 如果插入数据，自动提交? 和conn.commit()功能一致。
        )

        self.cur = self.conn.cursor()

    def insert_data(self, tabel_name, time, value):
        try:
            sql = f"insert into {tabel_name} (time, value) values ('{time}', {value});"
            self.cur.execute(sql)

        except Exception as e:
            print(e)
    
        
if __name__ == '__main__':
    import time
    time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(time) 
    m = MyMysql('10.0.6.161', 3306, 'co2_data', 'root', 'root')
    m.insert_data('data', time, 1000)
    while True:
        pass

