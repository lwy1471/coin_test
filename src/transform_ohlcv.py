import datetime
from constants import *
import numpy as np

def add_moving_avarage(df):
    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma10'] = df['close'].rolling(window=10).mean()
    df['ma15'] = df['close'].rolling(window=15).mean()
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['ma60'] = df['close'].rolling(window=60).mean()
    return df

def add_volume_ma(df):
    df['vol_ma5'] = df['volume'].rolling(window=5).mean()
    df['vol_ma10'] = df['volume'].rolling(window=10).mean()
    df['vol_ma15'] = df['volume'].rolling(window=15).mean()
    df['vol_ma20'] = df['volume'].rolling(window=20).mean()
    return df

def add_candle_type2(df):
    candle_type = []
    for i in df.index:
        open = df.loc[i, 'open'].to
        cur = df.loc[i, 'close']

        type(open)
        type(cur)

        if open*(1.0+CANDLE_BASE_GAP) <= cur :
            candle_type.append(CANDLE_RED)
        elif open*(1.0-CANDLE_BASE_GAP) >= cur:
            candle_type.append(CANDLE_BLUE)
        else :
            candle_type.append(CANDLE_CROSS)
    #df['cd_type'] = candle_type
    return df

def add_candle_type(df):
    df['gap'] = df['close'].sub(df['open'])
    df['cd_type'] = np.where( \
        df['gap'] >= 0, CANDLE_RED, \
        np.where( df['gap'] < 0, CANDLE_BLUE, CANDLE_CROSS)
    )
    return df

