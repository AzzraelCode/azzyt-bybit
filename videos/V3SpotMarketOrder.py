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

def get_assets(cl : HTTP, coin):
    """
    Получаю остатки на аккаунте по конкретной монете
    :param cl:
    :param coin:
    :return:
    """
    r = cl.get_wallet_balance(accountType="UNIFIED")
    assets = {
        asset.get('coin') : float(asset.get('availableToWithdraw', '0.0'))
        for asset in r.get('result', {}).get('list', [])[0].get('coin', [])
    }
    return assets.get(coin, 0.0)

def float_trunc(f, prec):
    """
    Ещё один способ отбросить от float лишнее без округлений
    :param f:
    :param prec:
    :return:
    """
    l, r = f"{float(f):.12f}".split('.') # 12 дб достаточно для всех монет
    return  float(f'{l}.{r[:prec]}')

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
    )

    try:
        r = cl.get_instruments_info(category="spot", symbol="SOLUSDT")
        print(r)

        # avbl = get_assets(cl, "SOL")
        # print(avbl, round(avbl, 3), round_down(avbl, 3), float_trunc(avbl, 3))

        # r = cl.place_order(
        #     category="spot",
        #     symbol="SOLUSDT",
        #     side="SELL",
        #     orderType="Market",
        #     qty=round_down(avbl, 3),
        #     # marketUnit="quoteCoin",
        # )
        #
        # print(r)

    except exceptions.InvalidRequestError as e:
        print("ByBit API Request Error", e.status_code, e.message, sep=" | ")
    except exceptions.FailedRequestError as e:
        print("HTTP Request Failed", e.status_code, e.message, sep=" | ")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print('Hola, AzzraelCode YT Subs!')
    main()
