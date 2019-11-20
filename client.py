import socket
import threading
import pickle
from TLV import *
# 创建socket对象
s = socket.socket()
# 连接远程主机
s.connect(('localhost', 2333))
def read_from_server(s):
    while True:
        print(s.recv(2048).decode('utf-8'))
# 客户端启动线程不断地读取来自服务器的数据
threading.Thread(target=read_from_server, args=(s, )).start()   # ①
# while True:
    # line = input()
    # if line is None or line == 'exit':
    #     break
    # 将用户的键盘输入内容写入socket
tlv = TLV(t_ext=7, l_ext=7)
tlv.add(10, "Foobar")
data = pickle.dumps(tlv)
# s.send(line.encode('utf-8'))
s.send(data)