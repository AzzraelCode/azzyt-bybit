"""
!!! Исходники к ролику                    https://youtu.be/e7Np2ICYBzg
!!! При регистрации на ByBit используй рефкод         G5REPY
!!! Поддержи канал                        https://azzrael.ru/spasibo
!!! AzzraelCode YouTube                   https://www.youtube.com/@AzzraelCode
"""
from time import sleep

import requests
from pybit.unified_trading import WebSocket

def handle_message(m):
    print(m)

def handle_ticker(m):
    d = m.get('data', {})
    print(d['symbol'], d['lastPrice'], sep=":")

def subscribe_all_inst(ws : WebSocket):
    """
    Подписка на SPOT на все торгуемые к USDT пары,
    с разбивкой на 10 аргументов
    в ответ на комментарий
    https://www.youtube.com/watch?v=8SY-G0Hk64Y&lc=Ugxh1doXi5r-k4fEhK14AaABAg
    :param ws:
    :return:
    """
    url = "https://api.bybit.com/v5/market/instruments-info"
    l = requests.get(url, dict(category='spot')).json().get('result', {}).get('list', [])
    symbols = [ s['symbol'] for s in l if s['quoteCoin'] == 'USDT' and s['status'] == 'Trading']

    args_limit = 10
    for i in range(0, len(symbols), args_limit):
        ws.ticker_stream(symbol=(symbols[i:i + args_limit]), callback=handle_ticker)
        sleep(0.5)

def main():

    ws = WebSocket(
        testnet=False,
        channel_type="spot",
    )

    # subscribe_all_inst(ws)

    ws.ticker_stream(symbol=[
        "BTCUSDT",
        "ETHUSDT",
        "NEARUSDT",
        "BNBUSDT",
        "LTCUSDT",
        "ADAUSDT",
        "AVAXUSDT",
        "SUIUSDT",
        "IDUSDT",
        "BCHUSDT",
        "DOTUSDT",
        "MATICUSDT",
        "TONUSDT",
    ], callback=handle_ticker)

    while True: sleep(1)

if __name__ == '__main__':
    print('Hola, AzzraelCode YT Subs!')
    main()
