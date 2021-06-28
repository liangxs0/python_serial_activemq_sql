

from my_serial import MySerial
from my_mq import MyActiveMq
from my_mysql import MyMysql, m_serial

import stomp
import time
import threading

queue_SensorData = 'SensorData' #传感器消息队列名称
queue_host = '10.0.6.161'
queue_port = 61613
queue_username = 'admin'
queue_password = 'admin'
# serial_com = 'com8'
# serial_bps = 9600

db_host = '10.0.6.161'
db_port = 3306
db_user = 'root'
db_password = 'root'
db_name = 'co2_data'
table_name = 'data'


co2_requests = [0X42,0X4D,0XE3,0X00,0X00,0X01,0X72] #co2数据请求帧


def send_to_mq(arg):
    myserial = arg[1]
    myconn = arg[0]
    mymysql = arg[2]

    while True:
        myserial.write(bytes(co2_requests))
        time.sleep(0.3)
        data = myserial.read().hex()
        s = [data[i:i+2] for i in range(0, len(data), 2)]
        res = int(s[2], 16)*256+int(s[8], 16) #获取指定数据
        myconn.send_data(queue_SensorData, f"message:{res}") #数据存入消息队列
        mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        mymysql.insert_data(table_name, mtime, res)#数据库数据存储
        # print(res)
        time.sleep(10)

def get_mq(arg):
    myconn = arg[0]
    myconn.read_data(queue_SensorData) #这个地方将来换成控制的队列
    

if __name__ == '__main__':
    m_mq = MyActiveMq(queue_host, queue_port, queue_username, queue_password)
    m_mq.mq_conn() #连接mq
    # m_serial = MySerial(serial_com, serial_bps)#打开串口连接
    m_sql = MyMysql(db_host, db_port, db_name, db_user, db_password)
    
    t1 = threading.Thread(target=send_to_mq, args=((m_mq, m_serial,m_sql), ), daemon=True)
    t2 = threading.Thread(target=get_mq, args=((m_mq, m_serial,m_sql), ), daemon=True)

    t1.start()
    t2.start()

    while True:
        time.sleep(1)
    
