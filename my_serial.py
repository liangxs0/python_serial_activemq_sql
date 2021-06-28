import serial
import time

serial_com = 'com8'
serial_bps = 9600

class MySerial(object):

    def __init__(self, com, bps):
        # assert isinstance(ser, serial.Serial)
        # 连接串口 com是串口号，bps是波特率固定值9600
        self.ser = serial.Serial(com, int(bps), parity="E", stopbits=1, bytesize=8)
        
    def read(self):
        print("读取数据：", end=" ")
        while True:
            if self.ser.inWaiting():
                data  = self.ser.read(self.ser.inWaiting())
            else:
                break
        print(data)
        print("读取完成")
        return data

    def write(self,data): 
        # 数据发送， data的数据类型是字节流。
        self.ser.write(data)
        return True

    def crc16(self, x):
        # crc检验.
        a = 0xFFFF
        b = 0xA001
        for byte in x:
            a ^= byte
            for i in range(8):
                last = a % 2
                a >>= 1
                if last == 1:
                    a ^= b
        return x+[a&0xFF, a>>8]

    def close(self):
        self.ser.close()


m_serial = MySerial(serial_com, serial_bps)#打开串口连接

if __name__ == '__main__':
    w = [0X42,0X4D,0XE3,0X00,0X00,0X01,0X72]#请求数据的指令--硬件的数据请求指令
    myserial = MySerial("com8",9600)
    while True:
        myserial.write(bytes(w))
        time.sleep(0.3)
        data = myserial.read().hex()

        s = [data[i:i+2] for i in range(0, len(data), 2)]
        res = int(s[2], 16)*256+int(s[8], 16)
        print(res)
        time.sleep(4)
    # res = s[8]*255+s[9]*8+s[10]
    # print(f"浓度：{res}")