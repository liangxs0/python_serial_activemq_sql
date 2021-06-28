import time
import stomp
from my_serial import *
from my_mysql import MyMysql, m_serial

class MyListener(stomp.ConnectionListener):

    def on_message(self, message):
        # header 消息头信息，可以通过header 判断那个topic的数据
        # {'message-id': 'ID:jtcsOTMS-db-47634-1552380859117-1:1:1:1:7249045', 'destination': '/queue/test_topic', 'timestamp': '15529}
        print(message)#获取到的队列信息
        #串口发送
        # data = message
        # m_serial.write(bytes(data))


        

class MyActiveMq():
    def __init__(self, queue_host, queue_port, queue_username, queue_password) -> None:
        self.queue_host = queue_host
        self.queue_port = queue_port
        self.queue_username = queue_username
        self.queue_password = queue_password

    def mq_conn(self):#连接mq
        self.conn = stomp.Connection10([(self.queue_host, self.queue_port)])
        self.conn.connect(username=self.queue_username, passcode=self.queue_password)
    
    def send_data(self, queue_name, data):
        '''
        queue_name:消息队列名称
        data:发送的数据
        '''
        self.conn.send(queue_name, f"message:{data}") #数据存入消息队列

    def read_data(self, queue_name):
        '''
        queue_name:消息队列名称
        '''
        self.conn.set_listener('serial_a', MyListener())
        self.conn.subscribe(destination=queue_name, ack='auto')
        while True:
            pass


if __name__ == '__main__':
    pass