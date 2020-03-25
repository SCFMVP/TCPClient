import re
import socket
import sys
#PIL图像处理标准库
from PIL import Image
from io import BytesIO

# TCPClient

# receive_count: int = 0


def start_tcp_client(ip, port):
    pic_data = b''
    # 创建socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 循环连接服务器
    failed_count = 0
    while True:
        try:
            print("start connect to server ")
            s.connect((ip, port))
            break
        except socket.error:
            failed_count += 1
            print("fail to connect to server %d times" % failed_count)
            if failed_count == 100: return

    # 连接成功进入循环 send and receive
    while True:
        print("connect success")

        # get the socket send buffer size and receive buffer size
        s_send_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        s_receive_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

        print("client TCP send buffer size is %d" % s_send_buffer_size)
        print("client TCP receive buffer size is %d" % s_receive_buffer_size)

        # 最底层循环
        while True:
            # msg = 'hello server, i am the client'
            # s.send(msg.encode('utf-8'))
            # print("send len is : [%d]" % len(msg))

            msg = s.recv(2048+602)
            pic_data += msg
            # print(msg.decode('utf-8'))
            print(msg)
            print("recv len is : [%d]" % len(msg))

            # 做分离处理
            if len(pic_data) == (2048 + 602):
                # 接收的字节
                print(pic_data)
                # 提取完整图片字节为hexStr
                pic = re.findall(r'ffd8(.+?)ffd9', pic_data.hex())  # 正则表达式匹配长江学者人数  提取“长江学者”和其后的“人”之间的字符，返回一个列表
                pic = 'ffd8'+pic+'ffd9'
                print(pic)
                # 将16进制hexStr转回字节数组
                pic.decode("hex")
                # 将bytes结果转化为字节流
                bytes_stream = BytesIO(pic)
                # 读取到图片
                jpg = Image.open(bytes_stream)
                jpg.show()  #展示图片
        break

    s.close()


if __name__ == '__main__':
    start_tcp_client('192.168.1.101', 6000)
