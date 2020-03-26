import re
import socket
import matplotlib.pyplot as plt   #导入matplotlib
import sys
#PIL图像处理标准库
from PIL import Image
from io import BytesIO


# TCPClient
"""
Author:Later
Time:2020/3/25 20:39
"""

# todo: 视频流展示

def start_tcp_client(ip, port):
    pic_data = b''
    plt.figure()

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

            msg = s.recv(1024)
            pic_data += msg
            # print(msg.decode('utf-8'))
            print(msg)
            print("recv len is : [%d]" % len(msg))

            # 做分离处理
            if pic_data.hex().find("ffd8") != -1 and pic_data.hex().find("ffd9") != -1:
                # 接收的字节
                print(pic_data)
                # 提取完整图片(最前面的一帧)字节为hexStr,用于正则表达式
                pic = re.findall(r'ffd8(.+?)ffd9', pic_data.hex())  # 正则表达式匹配长江学者人数  提取“长江学者”和其后的“人”之间的字符，返回一个列表
                pic = 'ffd8'+pic[0]+'ffd9'
                print(pic)
                # 将16进制hexStr转回字节数组
                pic = bytes.fromhex(pic)
                # 将bytes结果转化为字节流
                bytes_stream = BytesIO(pic)
                # 读取到图片
                jpg = Image.open(bytes_stream)
                # 展示图片
                jpg.show()
                # 展示视频
                # plt.imshow(jpg)
                # plt.xticks([])
                # plt.yticks([])
                # plt.show()
                # 清除缓冲器
                new = re.findall(r'ffd9(.+?)', pic_data.hex())  # 正则表达式匹配长江学者人数  提取“长江学者”和其后的“人”之间的字符，返回一个列表
                print("new: " + new[0])
                # 防止接收包恰好ffd9结尾,以及以0结尾
                if len(new) > 0 and new[0] != '0':
                    pic_data = bytes.fromhex(new[0])
                else:
                    pic_data = b''

        break

    s.close()


if __name__ == '__main__':
    start_tcp_client('192.168.0.8', 8089)
