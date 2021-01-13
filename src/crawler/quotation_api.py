import datetime
import pandas as pd
import sys

from pyupbit.request_api import _call_public_api


def get_tickers(fiat="ALL"):
    """
    마켓 코드 조회 (업비트에서 거래 가능한 마켓 목록 조회)
    :return:
    """
    try:
        url = "https://api.upbit.com/v1/market/all"
        contents = _call_public_api(url)[0]

        if isinstance(contents, list):
            markets = [x['market'] for x in contents]

            if fiat == "KRW":
                return [x for x in markets if x.startswith("KRW")]
            elif fiat == "BTC":
                return [x for x in markets if x.startswith("BTC")]
            elif fiat == "ETH":
                return [x for x in markets if x.startswith("ETH")]
            elif fiat == "USDT":
                return [x for x in markets if x.startswith("USDT")]
            else:
                return markets

        else:
            return None
    except Exception as x:
        print(x.__class__.__name__)
        return None


def _get_url_ohlcv(interval):
    url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/"
    if interval == "day":
        url += "days"
    elif interval == "minute1":
        url += "minutes/1"
    elif interval == "minute3":
        url += "minutes/3"
    elif interval == "minute5":
        url += "minutes/5"
    elif interval == "minute10":
        url += "minutes/10"
    elif interval == "minute15":
        url += "minutes/15"
    elif interval == "minute30":
        url += "minutes/30"
    elif interval == "minute60":
        url += "minutes/60"
    elif interval == "minute240":
        url += "minutes/240"
    elif interval == "week" or interval == "weeks":
        url += "weeks"
    elif interval == "month":
        url += "months"
    else:
        url += "days"

    return url


def get_ohlcv(ticker="KRW-BTC", interval="day", count=1):
    """
    캔들 조회
    :return:
    """
    try:
        url = _get_url_ohlcv(interval=interval)
        CODE_PREFIX = "CRIX.UPBIT."
        contents = _call_public_api(url, count=count, code=CODE_PREFIX+ticker)[0]
        dt_list = [datetime.datetime.strptime(x['candleDateTimeKst'][:19], "%Y-%m-%dT%H:%M:%S") for x in contents]
        df = pd.DataFrame(contents, columns=['candleDateTimeKst','openingPrice', 'highPrice', 'lowPrice', 'tradePrice',
                                             'candleAccTradeVolume'], index=dt_list)
        df = df.rename(
            columns={"candleDateTimeKst":"time", "openingPrice": "open", "highPrice": "high", "lowPrice": "low", "tradePrice": "close",
                     "candleAccTradeVolume": "volume"})
        return df.iloc[::-1]
    except Exception as x:
        print(x.__class__.__name__)
        print(x)
        return None


def get_daily_ohlcv_from_base(ticker="KRW-BTC", base=0):
    """
    :param ticker:
    :param base:
    :return:
    """
    try:
        df = get_ohlcv(ticker, interval="minute60")
        df = df.resample('24H', base=base).agg(
            {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
        return df
    except Exception as x:
        print(x.__class__.__name__)
        return None


def get_current_price(ticker="KRW-BTC"):
    """
    최종 체결 가격 조회 (현재가)
    :param ticker:
    :return:
    """
    try:
        url = "https://api.upbit.com/v1/ticker"
        contents = _call_public_api(url, markets=ticker)[0]
        if not contents:
            return None

        if isinstance(ticker, list):
            ret = {}
            for content in contents:
                market = content['market']
                price = content['trade_price']
                ret[market] = price
            return ret
        else:
            return contents[0]['trade_price']
    except Exception as x:
        print(x.__class__.__name__)


def get_orderbook(tickers="KRW-BTC"):
    '''
    호가 정보 조회
    :param tickers: 티커 목록을 문자열
    :return:
    '''
    try:
        url = "https://api.upbit.com/v1/orderbook"
        contents = _call_public_api(url, markets=tickers)[0]
        return contents
    except Exception as x:
        print(x.__class__.__name__)
        return None


# if __name__ == "__main__":
#     print(get_tickers())
#     print(get_tickers(fiat="KRW"))
#     # print(get_tickers(fiat="BTC"))
#     # print(get_tickers(fiat="ETH"))
#     # print(get_tickers(fiat="USDT"))

#     print(get_ohlcv("KRW-BTC", interval="minutes1", count=2))
#     # print(get_ohlcv("KRW-BTC", interval="day", count=5))
#     # print(get_ohlcv("KRW-BTC", interval="minute1"))
#     # print(get_ohlcv("KRW-BTC", interval="minute3"))
#     # print(get_ohlcv("KRW-BTC", interval="minute5"))
#     # print(get_ohlcv("KRW-BTC", interval="minute10"))
#     #print(get_ohlcv("KRW-BTC", interval="minute15"))
#     #print(get_ohlcv("KRW-BTC", interval="minute30"))
#     #print(get_ohlcv("KRW-BTC", interval="minute60"))
#     #print(get_ohlcv("KRW-BTC", interval="minute240"))
#     #print(get_ohlcv("KRW-BTC", interval="week"))
#     #print(get_daily_ohlcv_from_base("KRW-BTC", base=9))
#     #print(get_ohlcv("KRW-BTC", interval="day", count=5))

#     #print(get_current_price("KRW-BTC"))
#     #print(get_current_price(["KRW-BTC", "KRW-XRP"]))

#     #print(get_orderbook(tickers=["KRW-BTC"]))
#     #print(get_orderbook(tickers=["KRW-BTC", "KRW-XRP"]))