from flask import Flask
from flask_socketio import SocketIO, send
from client import FtxClient
import os

app = Flask('Crypto Viewer')
socketio = SocketIO(app, cors_allowed_origins="*")

fxt_client = FtxClient(
    api_key=os.environ.get('API_KEY'),
    api_secret=os.environ.get('API_SECRET')
)


@socketio.on('message')
def handle_message(req):

    if req == 'connected' or req == '/help':
        connected()
    elif req == '/markets':
        markets()


def connected():
    res = '''
Commands: <br>
/markets - get list of markets <br>
/market {name} - get data for a market <br>
/help - show list of commands <br>
'''
    send(res)


def markets():
    mark = fxt_client.list_markets()
    mark = list(filter(lambda m: '/' in m['name'], mark))
    mark = list(f'{m["name"]}: {m["price"]}' for m in mark)
    send('<br>'.join(mark))


if __name__ == '__main__':
    socketio.run(app)
