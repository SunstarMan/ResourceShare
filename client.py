from worklines import Receive_UDP_SYN, SendFile, QueryFlood

if __name__ == '__main__':
    receive_udp_syn = Receive_UDP_SYN()
    receive_udp_syn.start()
    send_file = SendFile()
    send_file.start()
    query_flood = QueryFlood()
    query_flood.start()