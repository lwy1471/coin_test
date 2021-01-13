import os
import numpy
import pandas as pd
import time
from pprint import pprint
from transform_ohlcv import *
from crawler.quotation_api import *

## csv로 테스트용
def get_df_from_csv(file_path):
    return pd.read_csv(file_path, encoding='utf-8', delimiter=',')

## 구매 조건 확인 함수
def buy_condition(cur, last):
    global CURRENT_STATUS
    if  last['cd_type'] == CANDLE_RED and \
        last[BASE_MOVING_AVERAGE] < last['close'] and \
        last['close'] <= cur['close'] \
        :
        return True

    return False

## 판매 조건 확인 함수
def sell_condition(cur, last, sell_counter):
    global CURRENT_MAX
    global BUYING_MONEY

    if  last['close'] <= BUYING_MONEY or \
        sell_counter >= 3 and \
        cur['cd_type'] == CANDLE_BLUE \
        :
        return True
    return False


def buy(cur):
    global MY_PAPER_MONEY
    global MY_COIN
    global BUYING_MONEY
    
    MY_COIN = (MY_PAPER_MONEY*0.9995) / cur['close']
    MY_PAPER_MONEY = 0
    BUYING_MONEY = cur['close']

def sell(cur):
    global MY_PAPER_MONEY
    global MY_COIN

    MY_PAPER_MONEY = MY_COIN * cur['close'] * 0.9995
    MY_COIN = 0


def sell_status():
    global CURRENT_STATUS
    CURRENT_STATUS = STATUS_SELLING



def init_status():
    global CURRENT_STATUS
    global CURRENT_MAX
    global MY_PAPER_MONEY
    global BUYING_MONEY
    global BUYING_COUNT


    CURRENT_STATUS = INIT_STATUS_CURRENT_STATUS
    CURRENT_MAX = INIT_STATUS_CURRENT_MAX
    BUYING_MONEY = 0
    BUYING_COUNT = 0



def changeDate(df_value):
    return datetime.datetime.strptime(df_value, "%Y-%m-%dT%H:%M:%S")

def get_old_list():
    old_list = pd.DataFrame(columns=['time','code','open','high','low','close','volume'])
    old_list = old_list.append(get_ohlcv(TICKER, interval=INTERVAL, count=LIST_COUNT))
    old_list['code'] = TICKER

    old_list = add_moving_avarage(old_list)
    old_list = add_volume_ma(old_list)
    old_list = add_candle_type(old_list)
    return old_list

def pick_one(df):
    dict = df.tail(1).to_dict('list')
    for key in dict.keys():
        dict[key] = dict[key][0]
    return dict

def pick_last_one(df):
    dict = df.tail(2).head(1).to_dict('list')
    for key in dict.keys():
        dict[key] = dict[key][0]
    return dict
        

### CONFIG
INTERVAL="minute1"
LIST_COUNT=80
SLEEP=1
DURATION_SEC=60*60*2
TICKER="KRW-BTC"
SLEEP=3
BASE_MOVING_AVERAGE='ma60'
####

### STATUS
CURRENT_STATUS = INIT_STATUS_CURRENT_STATUS
CURRENT_MAX = INIT_STATUS_CURRENT_MAX
MY_PAPER_MONEY = INIT_MY_PAPER_MONEY
MY_COIN = 0
BUYING_MONEY = 0
BUYING_COUNT = 0
###


if __name__ == "__main__":
    init_status()
    
    old_list = pd.DataFrame(columns=['time','code','open','high','low','close','volume'])
    ### 초반 데이터 20개
    old_list = get_old_list()
    ###
    last_row = pick_last_one(old_list)
    #print(last_row)

    start_date = datetime.datetime.now()
    print('start at: '+ str(start_date))
    prev = start_date
    while(True):
        current_time = datetime.datetime.now()
        during_time = current_time - start_date
        if( during_time.seconds >= DURATION_SEC):
            break
        
        cur = get_ohlcv(TICKER, interval=INTERVAL, count=1)
        cur = add_candle_type(cur)
        cur_row = pick_one(cur)
        current_price = cur_row['close']

        # print('Last Order type: '+last_row['cd_type'] + ', ma20: '+ str(last_row['ma20'])+', cur: '+str(cur_row['close']))
        # print('gap: '+str( cur_row['close'] - last_row['ma20'] ))

        ### strategy
        if( CURRENT_STATUS == STATUS_NEUTRAL ):
            if( buy_condition(cur_row, last_row) ):
                CURRENT_STATUS = STATUS_BUYING
                CURRENT_MAX == last_row['close']
                buy(cur_row)

                print('buying: '+ str(current_price) + ', at: ' + cur_row['time'][:19])
                pprint('paper money: '+ str(MY_PAPER_MONEY)+', coin: '+str(MY_COIN))

        elif( CURRENT_STATUS == STATUS_BUYING ):
            pprint('max: ' + str(CURRENT_MAX))

            old_list = get_old_list()
            old_list = add_candle_type(old_list)
            mask = (old_list.cd_type == CANDLE_BLUE)
            old_count = old_list.tail(BUYING_COUNT+1)['cd_type'].str.count(CANDLE_BLUE).sum()

            if ( sell_condition(cur_row, last_row, old_count) ):
                
                sell(cur_row)

                print('selling: '+ str(current_price) + ', at: ' + cur_row['time'][:19] + ', profit: '+ str(current_price-BUYING_MONEY))
                pprint('paper money: '+ str(MY_PAPER_MONEY)+', coin: '+str(MY_COIN))
                sell_status()
            else :
                if( CURRENT_MAX <= current_price ) :
                    CURRENT_MAX = current_price
        else:
            if(current_price <= last_row[BASE_MOVING_AVERAGE] ):
                init_status()
        ###

        last_interval = datetime.datetime.strptime(cur_row['time'], "%Y-%m-%dT%H:%M:%S%z")

        if( prev.minute != last_interval.minute ):
            if (CURRENT_STATUS == STATUS_BUYING):
                BUYING_COUNT = BUYING_COUNT + 1
                print('get new list, staus: '+CURRENT_STATUS+', Buying count: '+str(BUYING_COUNT))
            else :
                print('get new list, staus: '+CURRENT_STATUS)
            old_list = get_old_list()
            last_row = pick_last_one(old_list)
            #print(last_row)
            prev = datetime.datetime.now()


        time.sleep(SLEEP)

    print('endtime: ' + str(datetime.datetime.now()))
    profit = MY_PAPER_MONEY - INIT_MY_PAPER_MONEY
    profit_margin = MY_PAPER_MONEY / INIT_MY_PAPER_MONEY * 100
    print('profit: ' + str(profit) + ' margin: ' + str(profit_margin) )


