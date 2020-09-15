import threading

from bean import Fragment
from sockets import receive_udp, send_udp, TCP_Receiver, send_tcp
from tools import search_file, get_local_ip
from variable import *


class QueryFlood(threading.Thread):
    """
    在请求流中检索需要的文件
    """

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        while True:
            syn = Fragment()
            syn.local_ip = get_local_ip()
            syn.local_port = 0
            syn.dest_ip = '<broadcast>'
            syn.dest_port = 10000
            syn.filename = str(input('Please Enter the Filename You Want to Search: '))
            print('Begin to Search: ', syn.filename)

            ack = None
            for i in range(QUERY_TIMES):
                send_udp(syn, 3)
                print("SYN send", syn.to_json(), 3, 'times')
                try:
                    ack = receive_udp('', UDP_ACK, UDP_TIME_OUT)
                except TimeoutError:
                    print("not find", syn.filename, 'yet, try', i + 1)
                if ack is not None:
                    print("ACK receive", ack.to_json())
                    break

            if ack is None:
                continue

            tcp_receiver = TCP_Receiver(get_local_ip(), TCP_TIME_OUT)
            print('success create tcp server')

            ack.dest_ip = ack.local_ip
            ack.local_ip = get_local_ip()
            ack.local_port = tcp_receiver.port
            ack.dest_port = TCP_CON

            for i in range(QUERY_TIMES):
                send_udp(ack, 3)
                print('CON TCP send', ack.to_json())
                is_success = tcp_receiver.receive_tcp(ack.filename)
                if is_success:
                    print('finish download', ack.filename)
                    break
                else:
                    print('TCP connect timeout, try', i + 1)


class SendFile(threading.Thread):
    """
    发送文件
    """

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        while True:
            fragment = receive_udp('', TCP_CON, 0)
            print('CON TCP receive', fragment.to_json())
            file_path = search_file(fragment.filename)
            if file_path:
                send_tcp(fragment.local_ip, fragment.local_port, file_path)
            else:
                print("file", fragment.filename, "is not exists")


class Receive_UDP_SYN(threading.Thread):
    """
    接收外界发送的文件检索请求
    检索指定文件夹底下是否存在文件
    """

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        """
        检索指定文件夹底下是否存在文件
        如果存在返回ACK
        不存在不返回任何消息
        :return:
        """
        while True:
            fragment = receive_udp('', UDP_SYN, 0)
            print('SYN receive', fragment.to_json())

            file_path = search_file(fragment.filename)
            if file_path is None:
                print(fragment.filename, 'not exist')
                continue
            print(fragment.filename, 'find in', file_path)

            fragment.dest_ip = fragment.local_ip
            fragment.local_ip = get_local_ip()
            fragment.dest_port = UDP_ACK
            fragment.local_port = UDP_SYN
            send_udp(fragment, 3)
            print('ACK send', fragment.to_json(), 3, 'times')
