"""
!!! При регистрации на ByBit используй рефкод      G5REPY
!!! Поддержи канал                        https://azzrael.ru/spasibo
!!! AzzraelCode YouTube                   https://www.youtube.com/@AzzraelCode
"""
import os

from pybit import exceptions
from pybit.unified_trading import HTTP

import pandas as pd
from pandas import DataFrame

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# API_KEY = "dsfsdf4345345" # можно просто захардкодить
# SECRET_KEY = "dsfsdf4345345" # можно просто захардкодить
API_KEY = os.getenv("BB_API_KEY")
SECRET_KEY = os.getenv("BB_SECRET_KEY")

def log_limits(headers : dict):
    print(f"Limits  {headers.get('X-Bapi-Limit-Status')} / {headers.get('X-Bapi-Limit')}")

def assets(cl : HTTP):
    """
    Получаю остатки на UNIFIED аккаунте (не на кошельке целиком)
    копитрейдинг, фандинг, инверс - здесь не видно
    :param cl:
    :return:
    """
    r, _, h = cl.get_wallet_balance(accountType="UNIFIED")
    r = r.get('result', {}).get('list', [])[0]

    total_balance = float(r.get('totalWalletBalance', '0.0'))
    coins = [f"{float(c.get('walletBalance', '0.0')):>12.6f} {c.get('coin'):>12}" for c in r.get('coin', [])]

    print("\n".join(coins))
    print(f"---\nTotal: {total_balance:>18.2f}\n")

    log_limits(h)

def get_transfers(cl : HTTP):
    """
    Логи переводов средств на аккаунте

    ! в этом примере БЕЗ пагинации !
    подписывайся https://www.youtube.com/@AzzraelCode
    чтобы не пропустить про пагинацию

    :param cl:
    :return:
    """
    r, _, h = cl.get_transaction_log()

    df = DataFrame([dict(
        currency=e.get('currency'),
        type=e.get('type'),
        change=e.get('change'),
        cashBalance=e.get('cashBalance'),
        transactionTime=int(e.get('transactionTime')),
    ) for e in r.get('result', {}).get('list', []) if e.get('type').startswith('TRANSFER')])

    df['transactionTime']=pd.to_datetime(df['transactionTime'], unit='ms')
    df.sort_values(by=['transactionTime'], inplace=True, ascending=False)
    print(df)

    log_limits(h)

def main():

    cl = HTTP(
        api_key=API_KEY,
        api_secret=SECRET_KEY,
        recv_window=60000,
        return_response_headers=True,
    )

    try:
        # assets(cl)
        get_transfers(cl)

    except exceptions.InvalidRequestError as e:
        print("ByBit Request Error", e.status_code, e.message, sep=" | ")
    except exceptions.FailedRequestError as e:
        print("ByBit Request Failed", e.status_code, e.message, sep=" | ")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print('Hola, AzzraelCode YT Subs!')
    main()
