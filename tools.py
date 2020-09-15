import os
import socket

from variable import SHARED_DIR


def search_file(filename: str):
    """
    寻找指定文件夹下是否存在文件
    :param filename: 文件名
    :return: 结果文件路径，不存在就返回None
    """
    for root, dirs, files in os.walk(SHARED_DIR):
        for file in files:
            if filename == file:
                return os.path.join(root, file)
    return None


def get_local_ip():
    """
    获取本地IP
    :return: 本地IP
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
