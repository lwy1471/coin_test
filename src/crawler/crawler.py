from numpy.core.fromnumeric import _all_dispatcher
from pandas.core.frame import DataFrame 
import pandas as pd
from quotation_api import get_tickers, get_ohlcv

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from transform_ohlcv import add_moving_avarage

import datetime
import time


INTERVAL="minute1"
COUNT=20
SLEEP=1
DURATION_SEC=60*60

def save_parquet(df, file_path):
    df.columns = df.columns.astype(str)
    df.to_csv(file_path+'.parquet')

def save_data(df, file_path):
    df.to_csv(file_path+'.csv', mode='a', header=False)

def do_crawl(ticker_list, file_path, sleep):
    with open(file_path+'.csv', 'w', encoding='utf-8') as f:
        f.write('time,code,open,high,low,close,volume\n')
    f.close()



    ohlcv_list = DataFrame(columns=['time','code','open','high','low','close','volume'])
    ### 초반 데이터 20개
    # ticker = "KRW-BTC"
    # ohlcv_list = ohlcv_list.append(get_ohlcv(ticker, interval=INTERVAL, count=20))
    # ohlcv_list['code'] = ticker
    # save_data(ohlcv_list, file_path)
    ###

    start_date = datetime.datetime.now()
    prev = start_date
    while True: 
        delta = datetime.datetime.now() - prev

        during_time = datetime.datetime.now() - start_date
        
        # 1시간 후 종료
        if( during_time.seconds >= DURATION_SEC):
            break
        

        for ticker in ticker_list:
            ohlcv_list = ohlcv_list.append(get_ohlcv(ticker, interval=INTERVAL, count=1))
            ohlcv_list['code'] = ticker
            save_data(ohlcv_list, file_path)

        prev = datetime.datetime.now()
        time.sleep(sleep)



if __name__ == "__main__":


    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    start_date = datetime.datetime.now()

    start_date_str = start_date.strftime("%y%m%d%H%M")
    dir_path = os.path.dirname(os.path.abspath(__file__))+'/data/'
    file_path = dir_path+INTERVAL[:1].upper()+INTERVAL[-1:]+'_count_'+str(COUNT)+'_'+start_date_str

    with open(file_path+'.csv', 'w', encoding='utf-8') as f:
        f.write('time,code,open,high,low,close,volume\n')
    f.close()

    #all_tickers = get_tickers(fiat="KRW")
    all_tickers = ["KRW-BTC"]
    do_crawl(all_tickers, file_path, SLEEP)

    
