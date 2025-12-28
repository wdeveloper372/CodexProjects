import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import pandas_ta as ta
import json
import threading
import time
import queue
from websocket import WebSocketApp
from datetime import datetime

# --- CONFIG ---
API_KEY = "YOUR_FINNHUB_API_KEY"
SYMBOL = "NVDA"

st.set_page_config(layout="wide", page_title="Personal TC2000 Engine")
st.title(f"TC2000 Engine: {SYMBOL} (Relative Timeframe)")

# --- DATA STORAGE ---
if 'data_queue' not in st.session_state:
    st.session_state.data_queue = queue.Queue()

if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close'])

def get_tc2000_id(dt):
    """Mimics TC2000: 9:30-10:00 stub, then snaps to the top of every hour."""
    if dt.hour == 9 and dt.minute >= 30:
        return f"{dt.date()} 09:30"
    else:
        return f"{dt.date()} {dt.hour:02d}:00"

# --- LIVE FEED THREAD ---
if 'ws' not in st.session_state:
    # Capture queue in closure to avoid accessing st.session_state in thread
    q = st.session_state.data_queue
    def on_message(ws, message):
        q.put(message)

    ws = WebSocketApp(f"wss://ws.finnhub.io?token={API_KEY}", on_message=on_message)
    ws.on_open = lambda ws: ws.send(json.dumps({'type':'subscribe','symbol':SYMBOL}))
    threading.Thread(target=ws.run_forever, daemon=True).start()
    st.session_state.ws = True

# --- RENDERER ---
chart_placeholder = st.empty()

while True:
    # Process incoming messages from the queue
    while not st.session_state.data_queue.empty():
        message = st.session_state.data_queue.get()
        data = json.loads(message)
        if data.get('type') == 'trade' and data.get('data'):
            trade = data['data'][-1]
            price, ts = trade['p'], datetime.fromtimestamp(trade['t']/1000)
            cid = get_tc2000_id(ts)
            
            df = st.session_state.history
            if cid not in df.index:
                df.loc[cid] = [price, price, price, price]
            else:
                df.at[cid, 'High'] = max(df.at[cid, 'High'], price)
                df.at[cid, 'Low'] = min(df.at[cid, 'Low'], price)
                df.at[cid, 'Close'] = price
            
            # Calculate Indicators on the custom timeframes
            if len(df) > 20:
                df['EMA9'] = ta.ema(df['Close'], length=9)
                df['SMA20'] = ta.sma(df['Close'], length=20)
            
            st.session_state.history = df

    df = st.session_state.history
    if not df.empty:
        fig = go.Figure()
        # Custom Candles
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], 
                                     low=df['Low'], close=df['Close'], name="TC2000 Bar"))
        # 9 EMA & 20 SMA
        if 'EMA9' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA9'], line=dict(color='#26A69A', width=1.5), name="9 EMA"))
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'], line=dict(color='#EF5350', width=1.5), name="20 SMA"))
            
        fig.update_layout(template="plotly_dark", height=800, xaxis_rangeslider_visible=False)
        chart_placeholder.plotly_chart(fig, use_container_width=True)
    time.sleep(1)