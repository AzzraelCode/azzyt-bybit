"""
!!! Исходники к ролику                    https://youtu.be/e7Np2ICYBzg
!!! При регистрации на ByBit используй рефкод         G5REPY
!!! Поддержи канал                        https://azzrael.ru/spasibo
!!! AzzraelCode YouTube                   https://www.youtube.com/@AzzraelCode
!!! Документация                          https://bybit-exchange.github.io/docs/v5/ws/connect
"""
import os
from time import sleep
from pybit.unified_trading import WebSocket

API_KEY = os.getenv('BB_API_KEY')
API_SECRET = os.getenv('BB_SECRET_KEY')

def handle_message(m):
    print(m)

def main():

    ws_private = WebSocket(testnet=False, channel_type="private", api_key=API_KEY, api_secret=API_SECRET, callback_function=handle_message)
    # ws_spot = WebSocket(testnet=False, channel_type="spot")
    # ws_fut = WebSocket(testnet=False, channel_type="linear")

    ws_private.position_stream(callback=handle_message)
    ws_private.order_stream(callback=handle_message)

    # ws_private.wallet_stream(callback=handle_message)
    # ws_spot.ticker_stream(symbol="BTCUSDT", callback=handle_message)
    # ws_fut.ticker_stream(symbol="BTCUSDT", callback=handle_message)


    while True: sleep(1)

if __name__ == '__main__':
    print('Hola, AzzraelCode YT Subs!')
    main()
