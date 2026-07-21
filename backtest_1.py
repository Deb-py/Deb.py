import pandas as pd, numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import timedelta


#                             ADX

def adx_trend(df):
	df['tr1'] = df['High'] - df['Low']
	df['tr2'] = (df['High'] - df['Close'].shift(1)).abs()
	df['tr3'] = (df['Low'] - df['Close'].shift(1)).abs()
	df['Tr'] = np.maximum(df['tr1'], np.maximum(df['tr2'], df['tr3']))
	
	up = df['High'] - df['High'].shift(1)
	down = df['Low'].shift(1) - df['Low']
	df['+Dm'] = np.where((up > down) & (up > 0), up, 0)
	df['-Dm'] = np.where((down > up) & (down > 0), down, 0)
	
	df['sm_+Dm'] = df['+Dm'].rolling(window = 14).sum()
	df['sm_-Dm'] = df['-Dm'].rolling(window = 14).sum()
	df['sm_Tr'] = df['Tr'].rolling(window = 14).sum()
	
	df['+Di'] = 100*(df['sm_+Dm']/df['sm_Tr'])
	df['-Di'] = 100*(df['sm_-Dm']/df['sm_Tr'])
	
	df['Dx'] = 100*(df['+Di'] - df['-Di']).abs()/(df['+Di'] + df['-Di'])
	
	df['Adx'] = df['Dx'].ewm(alpha = 1/14, adjust = False).mean()
	df['adx_rising'] = df['Adx'] > df['Adx'].shift(1)
	df.drop(columns = ['tr1', 'tr2', 'tr3', 'sm_+Dm', 'sm_-Dm', 'sm_Tr', 'Dx'], errors = 'ignore', inplace = True)
	cond = [
			((df['+Di'] > df['-Di']) & (df['Adx'] > 30)),
			((df['-Di'] > df['+Di']) & (df['Adx'] > 30)),
			((df['Adx'] <= 20))
			]
	df['ADX_Trend'] = np.select(cond, [1, -1, 0], default = np.nan)
	return df

#                     RATE_OF_CHANGE

def roc_trend(df):
	str = 3
	mul = 2
	pd.options.display.float_format = '{:.2f}'.format
	df['pc'] = ((df['Close']/df['Open'])-1)*100
	df['pc_ema'] = df['pc'].ewm(1/str, adjust = False).mean()
	df['pc_sma'] = df['pc'].rolling(window=str).sum()
	
	df['pc_av'] = (((df['Close']/df['Open'])-1)*100).rolling(window = 24).mean()
	
	cond = [
			(df['pc_sma'] > df['pc_av']*mul),
			(df['pc_sma'] < (df['pc_av']*-1)*mul)
			]
	df['ROC_Trend'] = np.select(cond, [1, -1], default = 0)
	return df

#                             EMA

def ema(df):
	ema_ = 9
	wind = 24
	df['Ema9'] = df['Close'].ewm(span=ema_, adjust=False).mean()
	ema = df['Ema9']
	df['buf'] = ((df['High']/df['Low'])-1).rolling(window =wind).mean().clip(lower=0.002, upper=0.005)
	buf = df['buf']
	cond = [
			(df['Close'] > ema*(1+buf)),
			(df['Close'] < ema*(1-buf))
			]
	df['EMA_Trend'] = np.select(cond, [1, -1], default = 0)
	return df

#                        ADX + ROC

def adx_roc(df):
	cond = [
			((df['ROC_Trend'] == 1) & (df['ADX_Trend'] == 1)),
			((df['ROC_Trend'] == 1) & (df['Adx'] > 25)),
			(df['ROC_Trend'] == 1),
			((df['ROC_Trend'] == -1) & (df['ADX_Trend'] == -1)),
			((df['ROC_Trend'] == -1) & (df['Adx'] > 25)),
			(df['ROC_Trend'] == -1),
			((df['ROC_Trend'] == 0) & (df['ADX_Trend'] == 0)),
			((df['ROC_Trend'] == 0) & (df['Adx'] < 25)),
			(df['ROC_Trend'] == 0)
			]
			
	df['Trend'] = np.select(cond, ['ssu', 'su', 'u', 'ssd', 'sd', 'd', 'sss', 'ss', 's'], default = 's')
	return df

#                        ROC + EMA

def roc_ema(df):
	cond = [
        ((df['ROC_Trend'] == 0) | (df['EMA_Trend'] == 0)),
        ((df['ROC_Trend'] == 1) | (df['EMA_Trend'] == 1)),
        ((df['ROC_Trend'] == -1) | (df['EMA_Trend'] == -1))
    ]
	df['Trend'] = np.select(cond, [0, 1, -1], default=0)
	return df

#                         SIGNAL 🚥 

def signal(df):
	vol_str = 24
	df['vol_ma'] = df['Volume'].rolling(window=vol_str).mean()
	
	cont = 4
	cond = [
			(df['Trend'].rolling(window=cont).sum() >= cont),
			(df['Trend'].rolling(window=cont).sum() <= -1*cont)
			]
	df['cont'] = np.select(cond, [1, -1], default=np.nan)
	
	df['f_cont'] = df['cont']
	df['f_cont'] = df['f_cont'].ffill().fillna(0)
	
	vol_mul = 1.5
	cond = [
			((df['f_cont'] == -1) & (df['vol_ma'] < df['Volume']*vol_mul) & (df['Trend'] == 0)),
			((df['f_cont'] == 1) & (df['vol_ma'] < df['Volume']*vol_mul) & (df['Trend'] == 0))
			]
	df['Signal'] = np.select(cond, [1, -1], default = 0)
	return df

#                  PROFIT CALCULATE

def profit_cal(df):
    sl_ma = 24
    sl_str = 2
    
    # 1. Volatility Stop Distance
    df['range'] = np.log(df['High'] / df['Low'])
    df['Sl_dist'] = df['range'].rolling(window=sl_ma).mean() * sl_str
    
    # 2. Market Log Returns
    df['market_log_ret'] = np.log(df['Close'] / df['Close'].shift(1))
    
    # 3. Base Position (The 'Always-In' Assumption)
    df['Base_Position'] = df['Signal'].replace(0, np.nan).ffill().fillna(0)
    
    # 4. Vectorized Trade Grouping
    # Every time Signal is 1 or -1, a new trade begins. We tag them with unique IDs.
    df['Trade_ID'] = df['Signal'].replace(0, np.nan).notna().cumsum()
    
    # 5. Track Intra-Trade Drawdown
    df['Raw_Strat_Ret'] = df['Base_Position'].shift(1) * df['market_log_ret']
    df['Trade_Cum_Ret'] = df.groupby('Trade_ID')['Raw_Strat_Ret'].cumsum()
    
    # 6. Stop Loss Trigger
    # If the cumulative return of the trade drops below the allowed distance
    df['SL_Hit'] = df['Trade_Cum_Ret'] < -df['Sl_dist']
    
    # Once SL is hit, lock it as True for the remainder of that Trade_ID
    df['SL_Active'] = df.groupby('Trade_ID')['SL_Hit'].cumsum() > 0
    
    # 7. Real Position Resolution
    # If SL was active on the PREVIOUS bar, you are now flat (0)
    df['Position'] = np.where(df['SL_Active'].shift(1).fillna(False), 0, df['Base_Position'])
    
    # 8. Final Returns
    df['strat_log_ret'] = df['Position'].shift(1) * df['market_log_ret']
    
    # Cap the exact exit bar to perfectly match the Stop Loss distance
    df['strat_log_ret'] = np.where(
        (df['strat_log_ret'] < -df['Sl_dist']), 
        -df['Sl_dist'], 
        df['strat_log_ret']
    )
    
    # 9. Transaction Fees (Only charged on actual state changes)
    fee_pct = 0.001 
    df['trade_event'] = df['Position'].diff().fillna(0).abs().gt(0).astype(int)
    df['strat_log_ret'] = df['strat_log_ret'] - (df['trade_event'] * fee_pct)
    
    # 10. Equity Curve Calculation
    df['cum_log_ret'] = df['strat_log_ret'].cumsum()
    df['equity_curve'] = np.exp(df['cum_log_ret'])
    
    df['peak'] = df['equity_curve'].cummax()
    df['drawdown'] = (df['equity_curve'] - df['peak']) / df['peak']
    
    return df
		
												
#                              PLOT

def plot(df):
    # 1. PREP DATA
    # We look at the last 500 hours for a clean, actionable view.
    p_df = df#.tail(500).copy()
    p_df['Date'] = pd.to_datetime(p_df['Date'])
    
    # Visual Shift: We shift the trend by -1 to align the color of the line 
    # with the 'next' move, making the transitions look seamless.
    p_df['Plot_Trend'] = p_df['Trend'].shift(-1)
    
    # High-Contrast Color Palette
    colors = {
        1: '#00FF00',   # Bullish (Green)
        -1: '#FF0000',  # Bearish (Red)
        0: '#0000FF'    # Sideways (Electric Blue)
    }
    
    # 2. THE MULTI-PANE ARCHITECTURE
    fig = make_subplots(
        rows=3, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.02, 
        row_heights=[0.5, 0.2, 0.3],
        subplot_titles=("Price & Signal Analysis", "Momentum & Volatility", "Equity Curve (Growth)")
    )

    # --- ROW 1: PRICE & SIGNALS ---
    # Segmented Trend Line (The "Glow" Logic)
    p_df['trend_change'] = p_df['Plot_Trend'].ne(p_df['Plot_Trend'].shift())
    change_indices = p_df.index[p_df['trend_change']].tolist()
    change_indices.append(p_df.index[-1])

    for i in range(len(change_indices) - 1):
        start_idx = change_indices[i]
        end_idx = change_indices[i+1]
        segment = p_df.loc[start_idx:end_idx]
        current_val = segment['Plot_Trend'].iloc[0]
        line_color = colors.get(current_val, '#2F2F2F')
        
        fig.add_trace(go.Scatter(
            x=segment['Date'], y=segment['Close'],
            mode='lines',
            line=dict(color=line_color, width=3),
            showlegend=False
        ), row=1, col=1)

    # EMA 9 Overlay
    fig.add_trace(go.Scatter(
        x=p_df['Date'], y=p_df['Ema9'], 
        line=dict(color='#FFA500', width=1, dash='dot'),
        name='EMA 9'
    ), row=1, col=1)

    # Signal Markers (Optimized for Colorblind Clarity)
    buys = p_df[p_df['Signal'] == 1]
    sells = p_df[p_df['Signal'] == -1]

    fig.add_trace(go.Scatter(
        x=buys['Date'], y=buys['Low'] * 0.992,
        mode='markers',
        marker=dict(symbol='triangle-up', size=14, color='#00FF00', line=dict(width=1, color='white')),
        name='BUY (Exhaustion)'
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=sells['Date'], y=sells['High'] * 1.008,
        mode='markers',
        marker=dict(symbol='triangle-down', size=14, color='#FF0000', line=dict(width=1, color='white')),
        name='SELL (Distribution)'
    ), row=1, col=1)

    # --- ROW 2: MOMENTUM (ROC) ---
    fig.add_trace(go.Scatter(x=p_df['Date'], y=p_df['pc_sma'], name='ROC Momentum', line=dict(color='white')), row=2, col=1)
    fig.add_trace(go.Scatter(x=p_df['Date'], y=p_df['pc_av']*2, line=dict(color='gray', dash='dash'), name='Upper Band'), row=2, col=1)
    fig.add_trace(go.Scatter(x=p_df['Date'], y=p_df['pc_av']*-2, line=dict(color='gray', dash='dash'), showlegend=False), row=2, col=1)

    # --- ROW 3: THE TRUTH (EQUITY CURVE) ---
    fig.add_trace(go.Scatter(
        x=p_df['Date'], y=p_df['equity_curve'],
        fill='tozeroy',
        name='Equity Multiplier',
        line=dict(color='#FFD700', width=2)
    ), row=3, col=1)

    # Baseline (1.0 = Break Even)
    fig.add_hline(y=1.0, line_dash="dash", line_color="white", row=3, col=1)

    # 3. LAYOUT FINALIZATION
    fig.update_layout(
        template='plotly_dark', 
        height=1000, 
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.show()
    	
csv = 'crypto_data/ETH_1h_16Apr21-16Apr26.csv'
df = pd.read_csv(csv)
df = roc_trend(df)
df = ema(df)
df = roc_ema(df)
df = signal(df)
df = profit_cal(df)
plot(df)