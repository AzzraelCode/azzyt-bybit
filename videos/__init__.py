from datetime import datetime

import pytz


def ts_dt(time : int, is_ms = True):
    """
    Конвертация Timestamp в Python DateTime
    :param time:
    :param is_ms:
    :return:
    """
    if isinstance(time, str): time = int(time)
    if is_ms: time = int(time / 1000)

    return datetime.fromtimestamp(time, tz=pytz.UTC)