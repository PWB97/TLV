import socket
import threading
import pickle
from TLV import *
# 定义保存所有socket的列表
socket_list = []
# 创建socket对象
ss = socket.socket()
# 将socket绑定到本机IP和端口
ss.bind(('localhost', 2333))
# 服务端开始监听来自客户端的连接
ss.listen()
def read_from_client(s):
    try:
        data = pickle.loads(s.recv(2048))
        # test
        tlvp = TLVParser(data.buffer, t_ext=7, l_ext=7)
        for avp in tlvp.parse():
            print("%d(%d): %s" % (avp["type"], avp["length"], avp["value"]))
        # return s.recv(2048).decode('utf-8')
        return tlvp
    # 如果捕获到异常，则表明该socket对应的客户端已经关闭
    except:
        # 删除该socket
        socket_list.remove(s)   # ①
def server_target(s):
    try:
        # 采用循环不断地从socket中读取客户端发送过来的数据
        while True:
            content = read_from_client(s)
            # print(content)
            if content is None:
                break
            #    test
            # for client_s in socket_list:
            #     client_s.send(content.encode('utf-8'))
    except Exception:
        print(Exception.with_traceback())
while True:
    # 此行代码会阻塞，将一直等待别人的连接
    s, addr = ss.accept()
    socket_list.append(s)
    # 每当客户端连接后启动一个线程为该客户端服务
    threading.Thread(target=server_target, args=(s, )).start()