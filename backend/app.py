import socket
import threading
import ws
import responses as r


def handle(s):
    keep = True
    while keep:
        data = ws.receive(8196, s)
        if not data:
            keep = False

        try:
            if data == 'connected' or data == '/help':
                r.command_list(s)
            elif data.startswith('/markets'):
                r.markets(data, s)
            elif data.startswith('/market'):
                r.market_info(data.split(' ')[1], s)
            elif data.startswith('/orders'):
                r.orders(data.split(' ')[1], s)
            elif data.startswith('/trades'):
                r.trades(data.split(' ')[1], s)
            else:
                r.unknown_command(s)
        except StopIteration as ex:
            ws.send('Cannot find element you\'re searching for.', s)
        except Exception as ex:
            ws.send(ex.__str__(), s)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 8081))
    sock.listen(5)

    while True:
        conn, addr = sock.accept()
        print('New connection from {} {}'.format(addr[0], addr[1]))
        if ws.handshake(conn):
            t = threading.Thread(target=handle, args=(conn,))
            t.start()
