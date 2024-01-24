"""
!!! ************** При регистрации используй рефкод ************** !!!
!!! **************            G5REPY                ************** !!!
              https://www.bybit.com/invite?ref=G5REPY
"""
from pybit import exceptions
from pybit.unified_trading import HTTP

import pandas as pd
from pandas import DataFrame

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def tickers(cl : HTTP):
    """
    * Пример использования API ByBit для поиска фьючерса с наибольшим движением за 24 часа
    :param cl:
    :return:
    """
    r = cl.get_tickers(category="linear")
    df = DataFrame([dict(
        symbol=e.get('symbol'),
        price=e.get('lastPrice'),
        p24h=float(e.get('price24hPcnt')) * 100,
        p24h_abs=abs(float(e.get('price24hPcnt')) * 100)
    ) for e in r.get('result', {}).get('list', [])])
    df.sort_values(by=['p24h_abs'], inplace=True, ascending=False)
    print(df)

def instruments_info(cl : HTTP):
    """
    * Вынимаем все торгуемые инструменты, точности по ним и минимальный лот
    :return:
    """
    r = cl.get_instruments_info(category="spot")
    [print(
        f"{e.get('symbol')}, {e.get('lotSizeFilter', {}).get('basePrecision')}/{e.get('lotSizeFilter', {}).get('quotePrecision')} * {e.get('lotSizeFilter', {}).get('minOrderQty')}"
    ) for e in r.get('result', {}).get('list', []) if e.get('status') == 'Trading']

def main():
    try:
        cl = HTTP(recv_window=60000, )

        # !! Раскоментируй нужную функцию !!
        tickers(cl)
        # instruments_info(cl)

    except exceptions.InvalidRequestError as e:
        print("ByBit Request Error", e.status_code, e.message, sep=" | ")
    except exceptions.FailedRequestError as e:
        print("ByBit Requewst Failed", e.status_code, e.message, sep=" | ")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print('Hola, AzzraelCode YT Subs!')
    main()
