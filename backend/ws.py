import base64
import hashlib
import json
import struct
import re
from hashlib import sha1


# shake hands after connection
def handshake(socket):
    req = socket.recv(1024).decode('utf-8')
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    websocket_answer = (
        'HTTP/1.1 101 Switching Protocols',
        'Upgrade: websocket',
        'Connection: Upgrade',
        'Sec-WebSocket-Accept: {key}\r\n\r\n',
    )

    key = (re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', req)
           .groups()[0]
           .strip())

    response_key = base64.b64encode(sha1((key + GUID).encode('utf-8')).digest()).decode('utf-8')
    response = '\r\n'.join(websocket_answer).format(key=response_key)

    socket.send(response.encode('utf-8'))
    return True


def receive(size, socket):
    try:
        recv_data = socket.recv(size)
    except ConnectionAbortedError:
        return False

    if not recv_data:
        return False

    length = recv_data[1] & 127
    if length == 126:
        masks = recv_data[4:8]
        data = recv_data[8:]
    elif length == 127:
        masks = recv_data[10:14]
        data = recv_data[14:]
    else:
        masks = recv_data[2:6]
        data = recv_data[6:]

    raw_str = ""
    i = 0
    for d in data:
        raw_str += chr(d ^ masks[i % 4])
        i += 1

    return raw_str


def send(data, socket):
    if not isinstance(data, str):
        data = json.dumps(data)

    token = b"\x81"
    length = len(data)
    data = data.encode('utf-8')
    if length < 126:
        token += struct.pack(b"B", length)
    elif length <= 0xFFFF:
        token += struct.pack(b"!BH", 126, length)
    else:
        token += struct.pack(b"!BQ", 127, length)
    data = b'%s%s' % (token, data)

    socket.send(data)
    return True
