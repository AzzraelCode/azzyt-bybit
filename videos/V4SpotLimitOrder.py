"""
!!! Исходники к ролику                    https://youtu.be/e7Np2ICYBzg
!!! При регистрации на ByBit используй рефкод         G5REPY
!!! Поддержи канал                        https://azzrael.ru/spasibo
!!! AzzraelCode YouTube                   https://www.youtube.com/@AzzraelCode
"""
import os

from pybit import exceptions
from pybit.unified_trading import HTTP

API_KEY = os.getenv("BB_API_KEY")
SECRET_KEY = os.getenv("BB_SECRET_KEY")
SYMBOL = "DOTUSDC"

def round_down(value, decimals):
    """
    Ещё один способ отбросить от float лишнее без округлений
    :return:
    """
    factor = 1 / (10 ** decimals)
    return (value // factor) * factor

def main():

    cl = HTTP(
        api_key=API_KEY,
        api_secret=SECRET_KEY,
        recv_window=60000,
        max_retries=1,
    )

    try:

        price = float(cl.get_tickers(category="spot", symbol=SYMBOL).get('result').get('list')[0].get('ask1Price'))
        print(price)

        r = cl.place_order(
            category="spot",
            symbol=SYMBOL,
            side="Sell",
            orderType="Limit",
            qty=1,
            price=round_down(price * 0.99, 2),
        )

        # r = cl.get_open_orders(category='spot')
        # r = cl.get_open_orders(category='spot', orderId='1615447093214975232')
        # r = cl.cancel_order(category="spot", orderId='xxx')
        # r = cl.cancel_all_orders(category="spot")

        print(r)

    except exceptions.InvalidRequestError as e:
        print("ByBit API Request Error", e.status_code, e.message, sep=" | ")
    except exceptions.FailedRequestError as e:
        print("HTTP Request Failed", e.status_code, e.message, sep=" | ")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print('Hola, AzzraelCode YT Subs!')
    main()
