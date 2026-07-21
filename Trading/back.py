import pandas as pd
import numpy as np
csv = 'crypto_data/ETH_1h_16Apr21-16Apr26.csv'
df = pd.read_csv(csv)
df = df.iloc[::-1].reset_index(drop = True)
df['Ema50'] = df['Close'].rolling(window=21).mean()
condition = [
            (df['Close'] > df['Ema50']*1.005),
            (df['Close'] < df['Ema50']*0.995)
            ]
choice = ['Up', 'Down']
df['Price_Trend'] = np.select(condition, choice, default='Sideways')
df["X"] = df['Price_Trend'].where(df['Price_Trend'] != 'Sideways')
df['Fake_Trend'] = df['X'].ffill().fillna('NaN')
df['Vol_base'] = df['Volume'].rolling(window=24).mean()
condition = [
                (df['Volume'] >= df['Vol_base']),
                (df['Volume'] <= df['Vol_base'])
                ]
choice = ["High", "Low"]              
df['Volume_Trend'] = np.select(condition, choice, default = 'Null')
condition = [
                #((df['Volume_Trend'] == 'Low') & (df['Price_Trend'] == 'Up')),
#                ((df['Volume_Trend'] == 'Low') & (df['Price_Trend'] == 'Down')),
                ((df['Price_Trend'] == 'Sideways') & (df['Volume_Trend'] == 'High') & (df['Fake_Trend'] == 'Up')),
                ((df['Price_Trend'] == 'Sideways') & (df['Volume_Trend'] == 'High') & (df['Fake_Trend'] == 'Down'))
                ]
choice = [-1,1]#, -1, 1]
df['L&S'] = np.select(condition, choice, default = 0)
balance = 100
del df['X']
df['Roll_sl'] = (df['High'] - df['Low']).rolling(window = 24).mean()*2
tt = 0
st = 0
lt = 0
w = 0
l = 0
balance = 100
open_trades = []
close_trades = []
rr = 2
for i in range(len(df)-1):
    signal = df['L&S'][i]
    if (signal != 0) & (len(open_trades) < 5) & (balance > 0):
        tt += 1
        if signal == 1:
            lt += 1
            sl_dist = df['Roll_sl'][i]
            entry = df['Open'][i+1]
            print(f"Date: {df['Date'][i+1]}")
            print(f"Entry Long: {entry}")  
            sl = entry - sl_dist
            print(f"Sl: {sl}")
            tp = entry + (sl_dist * rr)
            print(f"Tp: {tp}")
        else:
            st += 1
            sl_dist = df['Roll_sl'][i]
            entry = df['Open'][i+1]
            print(f"Date: {df['Date'][i+1]}")
            print(f"Entry Short: {entry}")      
            sl = entry + sl_dist
            print(f"Sl: {sl}")
            tp = entry - (sl_dist * rr)
            print(f"Tp: {tp}")
        margin = balance*0.1
        balance -= margin                  
        open_trades.append({'type':signal, 'sl':sl, 'tp':tp, 'margin':margin})
    if open_trades != 0:
        high = df['High'][i+1]
        low = df['Low'][i+1]
        for j in range(len(open_trades)):
            x = open_trades[j]
            sl = x['sl']
            tp = x['tp']
            signal = x['type']
            margin = x['margin']
            if signal == 1:
                if low <= sl: l += 1; close_trades.append(x)
                if high >= tp: balance += margin*(rr+1); w += 1; close_trades.append(x)
            else:                
                if high >= sl: l += 1; close_trades.append(x)
                if low <= tp: balance+= margin*(rr+1); w += 1; close_trades.append(x)
        for ct in close_trades:
            if ct in open_trades:
                open_trades.remove(ct)
        close_trades = []                 
print(f"Balance: {balance}")
print(f'Win rate: {w/tt*100}')
print(f'Total trades: {tt}')                            