import ws
from client import FtxClient
import os

ftx_client = FtxClient(
    api_key=os.environ.get('API_KEY'),
    api_secret=os.environ.get('API_SECRET')
)


def command_list(s):
    res = '''
Commands: <br>
<b>/markets {search: string (optional)} {up-to: number (optional)}</b> - get list of markets. search - string to search in 
market name. up-to - max number of search results <br>
<b>/market {market: string}</b> - get data for a market <br>
<b>/orders {market: string}</b> - get order book for a market <br>
<b>/trades {market: string}</b> - get list of recent trades for a market<br>
<b>/help</b> - show list of commands <br>
'''
    ws.send(res, s)


def markets(req, s):
    params = req.split(' ')
    params = params[1:] if len(params) > 1 else []
    mark = ftx_client.list_markets()
    mark = filter(lambda m: '/' in m['name'], mark)

    if len(params) > 0:
        mark = filter(lambda m: params[0] in m['name'], mark)

    if len(params) > 1 and str.isdigit(params[1]):
        mark = list(mark)[:int(params[1])]

    mark = list(f'{m["name"]}: {m["price"]}' for m in mark)
    if len(mark) == 0:
        ws.send('No entries for this search. Try something else.', s)
        return

    ws.send('<br>'.join(mark), s)


def market_info(market, s):
    info = ftx_client.list_markets()
    info = next(filter(lambda m: '/' in m['name'] and m['name'] == market, info))
    info = list(f'{k}: {info[k]}' for k in info)
    ws.send('<br>'.join(info), s)


def orders(market, s):
    result = ftx_client.get_orderbook(market)
    asks = 'Asks: <br>' + '<br>'.join(f'price: {ord[0]} amount: {ord[1]}' for ord in result['asks'])
    bids = 'Bids: <br>' + '<br>'.join(f'price: {ord[0]} amount: {ord[1]}' for ord in result['bids'])
    ws.send(asks + '<br><br>' + bids, s)


def trades(market, s):
    curs = market.split('/')
    result = ftx_client.get_trades(market)
    ws.send('Last trades:<br>' + '<br><br>'.join(
        f'{"Sold" if trd["side"] == "buy" else "Bought "} '
        f'{trd["size"]} {curs[0]} at price {trd["price"]} '
        f'at {trd["time"][11:19]} {trd["time"][:10]}'
        for trd in result), s)


def unknown_command(s):
    res = '''
Unknown command: <br>
send /help to see list of commands <br>
'''
    ws.send(res, s)
