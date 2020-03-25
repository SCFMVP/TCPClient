import socket
import sys

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

        # receive_count = 0
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

            # receive_count += 1

            # 只做14次交流
            # if receive_count == 14:
            #     msg = 'disconnect'
            #     print("total send times is : %d " % receive_count)
            #     s.send(msg.encode('utf-8'))
            #     break
        break

    s.close()


if __name__ == '__main__':
    start_tcp_client('192.168.1.101', 6000)
