import os
import socket

from bean import Fragment
from variable import SAVED_DIR


class TCP_Receiver:
    def __init__(self, ip, timeout):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.settimeout(timeout)
        self.tcp_socket.bind((ip, 0))
        self.tcp_socket.listen(1)
        self.port = self.tcp_socket.getsockname()[1]

    def receive_tcp(self, filename):
        client_socket = None
        try:
            client_socket, client_address = self.tcp_socket.accept()
        except socket.timeout:
            return False

        with open(os.path.join(SAVED_DIR, filename), 'wb') as f:
            while True:
                data = client_socket.recv(2048)
                if data:
                    f.write(data)
                else:
                    break
        client_socket.close()
        self.tcp_socket.close()
        return True


def send_tcp(ip, port, file_path):
    """
    向目标主机发送文件
    :param ip: 目标主机地址
    :param port: 目标主机端口
    :param file_path: 文件地址
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    with open(file_path, mode='rb') as f:
        read = f.read()
        s.send(read)
    s.close()


def send_udp(fragment: Fragment, times: int):
    """
    发送UDP报文段
    :param fragment: 报文段类
    :param times: 一条报文段一次性发送几次
    :return: 无
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    for i in range(times):
        s.sendto(fragment.to_json().encode(), (fragment.dest_ip, fragment.dest_port))
    s.close()


def receive_udp(ip, port, timeout):
    """
    接收UDP报文段
    :param ip: 绑定用于接收特定ip的报文段
    :param port: 绑定端口
    :param timeout: 超时时间
    :return: 接收到的报文段对象
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, port))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)
    fragment_json, ip_port = s.recvfrom(2048)
    fragment = Fragment()
    fragment.from_json(fragment_json)
    s.close()
    return fragment
