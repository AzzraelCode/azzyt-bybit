"""
!!! При регистрации на ByBit используй рефкод      G5REPY
!!! Поддержи канал                        https://azzrael.ru/spasibo
!!! AzzraelCode YouTube                   https://www.youtube.com/@AzzraelCode
"""
import os
from time import sleep

import click

# from videos.V1PublicData import main
# from videos.V2Keys import main
# from videos.V3SpotMarketOrder import main
# from videos.V4SpotLimitOrder import main
# from videos.V5WebsocketPublic import main
# from videos.V5WebsocketPrivate import main
from videos.V6FuturesOrders import main

from pybit.unified_trading import WebSocket

API_KEY = os.getenv('BB_API_KEY')
API_SECRET = os.getenv('BB_SECRET_KEY')

@click.group()
def cli():
    pass

@cli.command()
def ws():
    print("*** WebSocket Starting / AzzraelCode YT ***")
    def handle_message(m): print(m)
    ws_private = WebSocket(
        testnet=False,
        channel_type="private",
        api_key=API_KEY,
        api_secret=API_SECRET,
        callback_function=handle_message
    )
    ws_private.position_stream(callback=handle_message)
    ws_private.order_stream(callback=handle_message)

    while True: sleep(1)

@cli.command()
def nested():
    print("***Hola, AzzraelCode YT ***")
    main()

if __name__ == '__main__':
    cli()


