
import pandas as pd
import numpy as np
import scipy

from datetime import datetime,time,date,timedelta
import matplotlib.pyplot as plt
import sys
# sys.path.append(r"D:\Chien_Folder\Alpha_Chien")
# import F1
import ta
import optuna
from ta.momentum import RSIIndicator
from scipy.signal import butter,lfilter
from datetime import time
from ta.volume import MFIIndicator
from datetime import time,date,timedelta
import sys
from ta.trend import MACD
def resample(df, duration):
    df_ = df.copy()
    df_['Date'] = pd.to_datetime(df_['Date'])
    df_.set_index('Date', inplace=True)
    ohlc_dict = {                                                                                                             
            'Open': 'first',                                                                                                    
            'High': 'max',                                                                                                       
            'Low': 'min',                                                         
            'Close': 'last',                                                                                                    
            'Volume': 'sum'
            }
    df_resample = df_.resample(duration).apply(ohlc_dict)
    df_resample.dropna(inplace=True)
    df_resample.reset_index(inplace=True)
    return df_resample

import sys
sys.path.append(r"E:\1.Finpros\API")
from get_data_vn import get_data_ps,get_data_vn30
df=get_data_vn30(3000)
df['Date']=pd.to_datetime(df['Date'])
df=df[df['Date']>'2017-01-01']
df.reset_index(drop=True, inplace=True)
# df=df[0:1000]
df=df.sort_values(by="Date")
df_vn30=resample(df, '1D')

# df_vn30 = get_vn30(1000)
# df_vn30 = test_live(df_vn30, 1, 'D')
# df_vn30.Date = pd.to_datetime(df_vn30.Date) 
df_vn30 = df_vn30[df_vn30.Date >= pd.to_datetime('2025-06-30')]
df_vn30['gain'] = df_vn30.Close.diff() 
df_vn30.dropna(inplace=True)
df_vn30['total_gain'] = df_vn30.gain.cumsum() 
df_vn30.reset_index(inplace=True)
##
df_vn30.to_csv(r'E:\1.Finpros\Alpha_Chien\My_Pnl\pnl_hc\df_vn30.csv',index=False)