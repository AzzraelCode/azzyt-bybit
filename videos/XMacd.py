import pandas as pd
from  ta.trend import MACD
from pybit.unified_trading import HTTP

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def main():
    """
    Простой пример получения баров через API ByBit
    и расчета MACD с помощью библиотеки https://github.com/bukosabino/ta
    :return:
    """
    klines = HTTP().get_kline(symbol='BTCUSDT', interval='15', limit=300, category='spot')
    df = pd.DataFrame.from_dict(klines.get('result').get('list')).iloc[:, :5]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close']
    df.sort_values('Time', ascending=False, inplace=True)
    df.index = pd.to_datetime(pd.to_numeric(df['Time']), unit='ms')

    # https://github.com/bukosabino/ta
    macd_obj = MACD(close=df['Close'].iloc[::-1], window_slow=26, window_fast=12, window_sign=9, fillna=True)
    df['MACD'] = macd_obj.macd()
    df['MACD_Signal'] = macd_obj.macd_signal()
    print(df)