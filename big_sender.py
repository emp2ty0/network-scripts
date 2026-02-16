import argparse
import socket

# На Linux используем константы из socket, а не отдельный модуль IN
IP_MTU = getattr(socket, 'IP_MTU', 14)  # 14 - стандартное значение для IP_MTU на Linux
IP_MTU_DISCOVER = getattr(socket, 'IP_MTU_DISCOVER', 10)
IP_PMTUDISC_DO = getattr(socket, 'IP_PMTUDISC_DO', 2)


def send_big_datagram(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IP, IP_MTU_DISCOVER, IP_PMTUDISC_DO)
    sock.connect((host, port))

    try:
        sock.send(b'#' * 65000)
    except socket.error:
        print('Alas, the datagram did not make it')
        max_mtu = sock.getsockopt(socket.IPPROTO_IP, IP_MTU)
        print(f'Actual MTU: {max_mtu}')
    else:
        print('The big datagram was sent!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send UDP packet to get MTU')
    parser.add_argument('host', help='the host to which to target the packet')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    send_big_datagram(args.host, args.p)