"""
!!! Исходники к ролику                    https://youtu.be/e7Np2ICYBzg
!!! При регистрации на ByBit используй рефкод         G5REPY
!!! Поддержи канал                        https://azzrael.ru/spasibo
!!! AzzraelCode YouTube                   https://www.youtube.com/@AzzraelCode
"""
import decimal
import inspect
import os
import time
from typing import Optional

from pybit import exceptions
from pybit.unified_trading import HTTP

API_KEY = os.getenv("BB_API_KEY")
SECRET_KEY = os.getenv("BB_SECRET_KEY")
SYMBOL = "SHIB1000USDT"

"""
! Примеры для режима One Way Mode
! Примеры не предназначены для ПРОДА и требуют дополнительных обработок ошибок 
"""
class FuturesOrders:
    def __init__(self):
        """
        Конструктор класса и инициализация
        - клиента pybit
        - получение параметров и фильтров Инструмента
        """
        self.cl = HTTP(api_key=API_KEY, api_secret=SECRET_KEY)
        self.category = "linear"
        self.symbol = SYMBOL
        self.price_decimals, self.qty_decimals, self.min_qty = self.get_filters()

    def get_filters(self):
        """
        Фильтры заданного инструмента
        - макс колво знаков в аргументах цены,
        - мин размер ордера в Базовой Валюте,
        - макс размер ордера в БВ
        """
        r = self.cl.get_instruments_info(symbol=self.symbol, category=self.category)
        c = r.get('result', {}).get('list', [])[0]

        min_qty = c.get('lotSizeFilter', {}).get('minOrderQty', '0.0')
        qty_decimals = abs(decimal.Decimal(min_qty).as_tuple().exponent)
        price_decimals = int(c.get('priceScale', '4'))
        min_qty = float(min_qty)

        self.log(price_decimals, qty_decimals, min_qty)
        return price_decimals, qty_decimals, min_qty

    def get_price(self):
        """
        Один из способов получения текущей цены
        """
        r = float(self.cl.get_tickers(category=self.category, symbol=self.symbol).get('result').get('list')[0].get('ask1Price'))
        self.log(r)
        return r

    def get_position(self, key : Optional[str] = None):
        """
        Получаю текущую позицию
        :param key:
        :return:
        """
        r = self.cl.get_positions(category=self.category, symbol=self.symbol)
        p = r.get('result', {}).get('list', [])[0]
        qty = float(p.get('size', '0.0'))
        if qty <= 0.0: raise Exception("empty position")

        ret = dict(
            avg_price = float(p.get('avgPrice', '0.0')),
            side = p.get('side'),
            unrel_pnl = float(p.get('unrealisedPnl', '0.0')),
            qty = qty
        )
        ret['rev_side'] = ("Sell", "Buy")[ret['side'] == 'Sell']
        self.log(ret)

        return ret.get(key) if key else ret

    def place_limit_order_by_percent(
            self,
            qty : float = 0.00001,
            side : str = "Sell",
            distance_perc : int = 2,
            order_link_id : Optional[str] = None
    ):
        """
        Установка лимитного ордера по инструменту определенному в конструкторе класса
        в процентах от текущей цены
        в зависимости от направления лимитного ордера цена стопа расчитывается в разные стороны
        """
        curr_price =self.get_price()
        order_price = self.calculate_limit_price_perc(curr_price, side, distance_perc)
        if not order_link_id: order_link_id = f"AzzraelCode_{self.symbol}_{time.time()}"

        args = dict(
            category=self.category,
            symbol=self.symbol,
            side=side.capitalize(),
            orderType="Limit",
            qty=self.floor_qty(qty),
            price=self.floor_price(order_price),
            orderLinkId=order_link_id
        )
        self.log("args", args)

        r = self.cl.place_order(**args)
        self.log("result", r)

        return r

    def place_market_order_by_base(self, qty : float = 0.00001, side : str = "Sell"):
        """
        Размещение рыночного ордера с указанием размера ордера в Базовой Валюте (BTC, XRP, etc)
        :param qty:
        :param side:
        :return:
        """
        args = dict(
            category=self.category,
            symbol=self.symbol,
            side=side.capitalize(),
            orderType="Market",
            qty=self.floor_qty(qty),
            orderLinkId=f"AzzraelCode_{self.symbol}_{time.time()}"
        )
        self.log("args", args)

        r = self.cl.place_order(**args)
        self.log("result", r)

        return r

    def place_market_order_by_quote(self, quote: float = 5.0, side: str = "Sell"):
        """
        Отправка ордера с размером позиции в Котируемой Валюте (USDT напр)
        имеет смысл только для контрактов
        (для спота есть аргумент marketUnit, см. https://youtu.be/e7Np2ICYBzg )
        """
        curr_price = self.get_price()
        qty = self.floor_qty(quote / curr_price)
        if qty < self.min_qty: raise Exception(f"{qty} is to small")

        self.place_market_order_by_base(qty, side)


    def cancel_open_order_by_order_link_id(self, order_link_id):
        """
        Отменяю открытый ордер лимитка/алго
        по кастомному идентификатору
        """
        r = self.cl.cancel_order(category=self.category, symbol = self.symbol, orderLinkId=order_link_id)
        self.log(r)

        return r

    def cancel_all_open_orders(self):
        """
        Отмена всех открытых ордеров (лимитки и алго)
        по секции + инструмент
        """
        r = self.cl.cancel_all_orders(category=self.category, symbol = self.symbol)
        print("* cancel_all_open_orders", r)

    def reverse_position(self):
        """
        Переворот позиции
        :return:
        """
        p = self.get_position()
        return self.place_market_order_by_base(p['qty'] * 2, p['rev_side'])

    def close_position(self):
        """
        Полное закрытие текущей позиции
        """
        args = dict(
            category=self.category,
            symbol=self.symbol,
            side=self.get_position("rev_side"),
            orderType="Market",
            qty=0.0,
            orderLinkId=f"AzzraelCode_{self.symbol}_{time.time()}",
            reduceOnly=True,
            closeOnTrigger=True,
        )
        self.log("args", args)

        r = self.cl.place_order(**args)
        self.log("result", r)

    def place_stop_loss(self, perc : float = 5):
        ...

    def place_take_profit(self, perc : float = 5):
        ...

    def place_conditional_order(self):
        ...

    def place_oco_order(self):
        ...

    def set_leverage(self):
        ...

    def log(self, *args):
        """
        Для удобного вывода из методов класса
        """
        caller = inspect.stack()[1].function
        print(f"* {caller}", self.symbol, "\n\t", args, "\n")

    def _floor(self, value, decimals):
        """
        Для аргументов цены нужно отбросить (округлить вниз)
        до колва знаков заданных в фильтрах цены
        """
        factor = 1 / (10 ** decimals)
        return (value // factor) * factor

    def floor_price(self, value):
        return self._floor(value, self.price_decimals)

    def floor_qty(self, value):
        return self._floor(value, self.qty_decimals)

    def calculate_limit_price_perc(self, price, side : str = "Sell", distance_perc : int = 2):
        """
        Расчет цен для постановки лимитного/алго ордера
        в процентах от заданной цены
        и в зависимости от направления
        :param price: Цена инструмента
        :param side: Sell/Buy
        :param distance_perc: колво процентов, мб отрицательным
        :return:
        """
        return price * (100 + ((-1, 1)[side.lower() == "sell"] * distance_perc)) / 100


def main():
    try:
        f = FuturesOrders()

        # f.place_limit_order_by_percent(f.min_qty, "Sell", 5)
        # f.place_limit_order_by_percent(f.min_qty, "Sell", 10)
        # f.cancel_all_open_orders()

        # order_link_id="AzzraelCodeYT_1"
        # f.place_limit_order_by_percent(f.min_qty, "Buy", 3, order_link_id=order_link_id)
        # f.cancel_open_order_by_order_link_id(order_link_id)

        # f.place_market_order_by_base(f.min_qty, "buy")
        # f.get_position()

        # f.place_market_order_by_quote(1, "sell")
        # f.get_position()

        # f.reverse_position()

        f.close_position()

    except exceptions.InvalidRequestError as e:
        print("ByBit API Request Error", e.status_code, e.message, sep=" | ")
    except exceptions.FailedRequestError as e:
        print("HTTP Request Failed", e.status_code, e.message, sep=" | ")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print('Hola, AzzraelCode YT Subs!')
    main()
