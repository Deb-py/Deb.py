from colorama import Fore, Back, Style, init
init(autoreset=True)
Y = Fore.YELLOW + Style.BRIGHT
R = Fore.RED + Style.BRIGHT
G = Fore.BLUE + Style.BRIGHT
C = Fore.CYAN + Style.BRIGHT
M = Fore.WHITE + Style.BRIGHT
print(f"{Y}⏳Starting please wait...\n")
import json
import os
import requests
import pandas as pd
import time
from datetime import datetime as dati
from datetime import timedelta as ti_de
def get():
    if os.path.exists('coin_dict.json'):
        with open('coin_dict.json', 'r') as f:
            data = json.load(f)
            if time.time() - data['date'] < 30*24*60*60:
                coins = data['coin_info']
                return coins
    try:
        url = "https://min-api.cryptocompare.com/data/all/coinlist"
        raw_data = requests.get(url).json()
        coin_info = {}
        for symbol, det in raw_data['Data'].items():
            ts = det.get('ContentCreatedOn',0)
            if symbol == 'BTC':
                ts = 1268784000
            coin_info[symbol] = int(ts)
        with open('coin_dict.json', 'w') as f:
            json.dump({'coin_info':coin_info, 'date':int(time.time())}, f)
        return coin_info
    except Exception as e:
        print(f"{R}Network issue {e}")
        return {}
def datta(limit, agg, coin_symbol, tim_frm, en_ts, m_con):
    full_data = []
    stop_limit = limit
    sl = limit
    while stop_limit > 0:
        if stop_limit-int(2000/int(agg)) < 0:
            url = f"https://min-api.cryptocompare.com/data/v2/histo{tim_frm}?fsym={coin_symbol}&tsym=USD&limit={int(stop_limit)}&aggregate={agg}&toTs={en_ts}"
            raw_data = requests.get(url).json()
            if not raw_data['Data']['Data']:
                break
            full_data.extend(raw_data['Data']['Data'])
            #print(f"{G}✓{len(full_data)}/{sl} Completed !")
            break
        else:
            url = f"https://min-api.cryptocompare.com/data/v2/histo{tim_frm}?fsym={coin_symbol}&tsym=USD&limit={2000}&aggregate={agg}&toTs={en_ts}"
            raw_data = requests.get(url).json()
            if not raw_data['Data']['Data']:
                break
            full_data.extend(raw_data['Data']['Data'])
            en_ts = raw_data['Data']['Data'][0]['time']-m_con*60
            stop_limit -= len(raw_data['Data']['Data'])
        print(f"{G}✓{len(full_data)}/{sl} Rows Completed !")
    print(f"{G}✓{len(full_data)}/{sl} Rows Completed !")
    return full_data
def data_cleaner(full_data):
    df = pd.DataFrame(full_data)  
    df = df.rename(columns={
    'time':'Date',
    'open':'Open',
    'high':'High',
    'low':'Low',
    'close':'Close',
    'volumefrom':'Volume'
    })
    df['Date'] = pd.to_datetime(df['Date'], unit = 's')
    df = df[df['Close'] > 0]
    df.drop(columns=['volumeto', 'conversionType', 'conversionSymbol'], errors='ignore', inplace=True)
    df.dropna(inplace = True)
    df = df.sort_values(by='Date', ascending=True)
    df = df.reset_index(drop=True)
    return df
def csv_name(c, t, s, e):
    return f"{c}_{t}_{s.strftime('%d%b%y')}-{e.strftime('%d%b%y')}"
m1ing = {
"1m" : ("1", "minute", 1), "5m" : ("5", "minute", 5), "15m" : ("15", "minute", 15), "30m" : ("30", "minute", 30), "1h" : ("1", "hour", 60), "4h" : ("4", "hour", 4*60), "6h" : ("6", "hour", 6*60), "12h" : ("12", "hour", 12*60), "1D" : ("1", "day", 24*60), "7D" : ("7", "day", 7*24*60), "30D" : ("30", "day", 30*24*60)
}
m2ing = {"day" : 24*60, "days" : 24*60, "month" : 30*24*60, "months" : 24*60*30, "year" : 365*60*24, "years" : 24*60*365}
exit = False
while True:  
    try:
        valid_coin = get()
        break
    except Exception as e:
        print(f"{R}Network error !\n{e} ⚠️\n")
        inpu = input(f"{C}1) for retry 2) for exit\n")
        if inpu == "1":
            continue
        else:
            exit = True
            break
while exit != True:
    while True:
        coin_symbol = input(f"{C}Enter coin (e.g. Eth, Btc...) : \nEnter : ").strip().upper()
        if coin_symbol in valid_coin:
            ts_unix = get()[coin_symbol]
            ts_det = dati.fromtimestamp(ts_unix).strftime('%d %B %Y')
            print(f"\n{G}{coin_symbol} found ! 🎉")
            print(f"{G}Data available since : {ts_det}")
            break
        else:
            print(f"\n{R}Don't enter full name like Bitcoin ❌ \nenter Btc ✅\n")
    while True:
        time_look = input(f"\n{C}For lookback (Enter - e.g. 50days, 6months, 1year)\nFor date range YYYY-MM-DD(Enter - e.g. 2020-01-01 to 2025-01-01)\nDon't enter 1.5 years enter 18 months \nEnter : ").lower()
        if "to" in time_look:
            try:
                a, b = time_look.split(" to ")
                st = dati.strptime(a.strip(), "%Y-%m-%d")
                en = dati.strptime(b.strip(), "%Y-%m-%d")
                if en - st == 0:
                    print(f"{R}No Data in 0 day range !")
                    continue
                if en < st:
                    print(f"\n{R}2026-01-01 to 2025-01-01 ❌\n2025-01-01 to 2026-01-01 ✅")
                    continue
                if en > dati.now():
                    print(f"\n{R}I am not a Time traveller 😒")
                    continue
                if int(st.timestamp()) < int(ts_unix):
                    print(f"\n{R}No data before {ts_det}")
                    continue
                else:
                    en_ts = int(en.timestamp())
                    min_ = (en-st).total_seconds()/60
                    mode = True
                    print(f"\n{G}Success ! 🎉")
                    break
            except Exception as e:
                print(f"\n{R}Try as example, \nDon't write this e.g. 2020-1-1 ❌ \ninstead of 2020-01-01 ✅\n{e}")
        else:
            num = ""
            tim = ""
            s = True
            for i in time_look:
                if i.isdigit():
                    if s == True:
                        num += i
                elif i.isalpha():
                    tim += i
                    s = False
            if num != "" and tim != "" and tim in m2ing and int(num) > 0:
                if int(time.time()) - m2ing[tim]*int(num)*60 < int(ts_unix):
                    print(f"\n{R}No data before {ts_det}")
                    continue
                mode = False
                print(f"\n{G}Success ! 🎉")
                break
            else:
                print(f"\n{R}Make your input like e.g.")
    while True:
        timeframe = input(f"\n{C}Choose Timeframe (1m, 2m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 1D, 7D, 30D)\nEnter : ").strip()
        if timeframe in m1ing:
            agg, tim_frm, m_con = m1ing[timeframe]
            print(f"\n{G}Success ! 🎉")
            break
        else:
            print(f"{R}You may Enter 1 m, 1minute, 1d, 1Day instead of 1m or 1D \nWrite exact as options")
    if mode == True:
        limit = min_//m_con
    else:
        limit = (m2ing[tim]*int(num))//m_con
        en_ts = int(dati.now().timestamp())
        en = dati.now()
        st = en - ti_de(minutes = limit * m_con)
    stop_limit = 50000
    if limit > stop_limit:
        print(f"\n{R}Your limit is {stop_limit} lines but you request {limit} line. 🧱\n")
        continue
    try:
        print(f"\n{Y}⏳Data fleaching from API...")
        full_data = datta(limit, agg, coin_symbol, tim_frm, en_ts, m_con)
        df = data_cleaner(full_data)
        if df.empty:
            print(f"\n{R}No Data found ! 🆘")
            continue
        en = df['Date'].iloc[-1]
        st = df['Date'].iloc[0]
        csv_nam = csv_name(coin_symbol, timeframe, st, en)
        print(f"\n{G}{csv_nam}.csv is ready ! 🎉")
        if input(f"\n{C}Enter 'D' to download : ").strip().lower() == 'd':
            if os.path.exists(f'{csv_nam}.csv') == False:
                df.to_csv(f'{csv_nam}.csv', index = False)
                print(f"\n{G}{csv_nam}.csv downloaded successfully ! 🎉\n")
            else:
                print(f"\n{R}{csv_nam}.csv already exist 🚫\n")
        else:
            continue
    except Exception as e:
        print(f'{R}\nERROR "{e}"⚠️\n')
    if input(f"{C}Enter 'Q'/'R' to quit/redo : ").strip().lower() == 'q':
        print(f"\n\n{M}                  - - -P E A C E ✌🏻- - -")
        break