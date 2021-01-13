
import pyupbit
print(pyupbit.Upbit)

tickers = pyupbit.get_tickers()
print(tickers)

price = pyupbit.get_current_price("KRW-XRP")
print(price)


df = pyupbit.get_ohlcv("KRW-BTC", interval="second")
print(df)

import requests

url = "https://api.upbit.com/v1/candles/minutes/1"

querystring = {"market":"KRW-BTC","count":"1"}

response = requests.request("GET", url, params=querystring)

print(response.text)


orderbook = pyupbit.get_orderbook("KRW-BTC")
print(orderbook)

import pandas as pd

data = pd.read_csv("D:/PROJECT/coin_trading/src/upbit_key.csv")

for row in data.itertuples():
    accesskey = row.accesskey
    secretkey = row.secretkey


upbit = pyupbit.Upbit(accesskey, secretkey)
print(upbit.get_balances())


import requests

url = "https://api.upbit.com/v1/candles/minutes/1"

querystring = {"market":"KRW-BTC","count":"1"}

response = requests.request("GET", url, params=querystring)
df = pd.read_json(response.text)
df.tail()

pythonDf = pyupbit.get_ohlcv("KRW-BTC", interval="minute1")
pythonDf = pythonDf[pythonDf['volume']!=0]
ma5 = pythonDf['close'].rolling(window=5).mean()
pythonDf.insert(len(pythonDf.columns), "MA5", ma5)
pythonDf.tail()


import requests

url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-BTC&count=1"


querystring = {"market":"KRW-BTC","count":"1"}

response = requests.request("GET", url, params=querystring)
df = pd.read_json(response.text)
df.tail()
df.columns

import datetime

def get_ohlcv(ticker="KRW-BTC", interval="day", count=200):
    """
    캔들 조회
    :return:
    """
    try:
        url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-BTC&count=1"
        #contents = _call_public_api(url, market=ticker, count=count)[0]
        contents = requests.request("GET", url)
        print(contents.text)
        dt_list = [datetime.datetime.strptime(x['candleDateTimeKst'], "%Y-%m-%dT%H:%M:%S") for x in contents]
        print(dt_list)
        df = pd.DataFrame(contents, columns=['openingPrice', 'highPrice', 'lowPrice', 'tradePrice',
                                             'candleAccTradeVolume'],
                          index=dt_list)

        df = df.rename(
            columns={"openingPrice": "open", "highPrice": "high", "lowPrice": "low", "tradePrice": "close",
                     "candleAccTradeVolume": "volume"})
        return df.iloc[::-1]
    except Exception as x:
        print(x)
        return None


df = get_ohlcv()



def requests_retry_session(retries=5, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    """

    :param retries:
    :param backoff_factor:
    :param status_forcelist:
    :param session:
    :return:
    """
    s = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    return s


import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

kwargs = {
    "market":"KRW-BTC", "count":"1", "code":"CRIX.UPBIT.KRW-BTC"
}

url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/days"
resp = requests_retry_session().get(url, params=kwargs)
resp.json()


