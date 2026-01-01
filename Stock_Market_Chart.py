import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
import threading
import time
import queue
from websocket import WebSocketApp
from datetime import datetime

# --- SAFE IMPORT ---
try:
    import pandas_ta as ta
except ImportError:
    ta = None

st.set_page_config(layout="wide", page_title="Multi-Stock TC2000 Engine")

# --- CONFIG & KEY ---
# Use st.secrets["FINNHUB_KEY"] if you set up the toml file!
API_KEY = "YOUR_FINNHUB_API_KEY" 

st.sidebar.title("Settings")
input_symbols = st.sidebar.text_input("Enter Symbols (comma separated)", "NVDA,AAPL")
SYMBOLS = [s.strip().upper() for s in input_symbols.split(",")]

# --- DATA STORAGE ---
if 'data_queues' not in st.session_state:
    st.session_state.data_queues = {sym: queue.Queue() for sym in SYMBOLS}
if 'histories' not in st.session_state:
    st.session_state.histories = {sym: pd.DataFrame(columns=['Open', 'High', 'Low', 'Close']) for sym in SYMBOLS}

def get_tc2000_id(dt):
    if dt.hour == 9 and dt.minute >= 30:
        return f"{dt.date()} 09:30"
    return f"{dt.date()} {dt.hour:02d}:00"

# --- LIVE FEED THREADS ---
if 'threads_started' not in st.session_state:
    def on_message(ws, message):
        data = json.loads(message)
        if data.get('type') == 'trade':
            # Identify which symbol this trade belongs to
            for trade in data['data']:
                s = trade['s']
                if s in st.session_state.data_queues:
                    st.session_state.data_queues[s].put(trade)

    def run_ws():
        ws = WebSocketApp(f"wss://ws.finnhub.io?token={API_KEY}", on_message=on_message)
        ws.on_open = lambda ws: [ws.send(json.dumps({'type':'subscribe','symbol':s})) for s in SYMBOLS]
        ws.run_forever()

    threading.Thread(target=run_ws, daemon=True).start()
    st.session_state.threads_started = True

# --- RENDERER GRID ---
cols = st.columns(len(SYMBOLS))
placeholders = [cols[i].empty() for i in range(len(SYMBOLS))]

while True:
    for i, sym in enumerate(SYMBOLS):
        q = st.session_state.data_queues[sym]
        df = st.session_state.histories[sym]
        
        while not q.empty():
            trade = q.get()
            price, ts = trade['p'], datetime.fromtimestamp(trade['t']/1000)
            cid = get_tc2000_id(ts)
            
            if cid not in df.index:
                df.loc[cid] = [price, price, price, price]
            else:
                df.at[cid, 'High'] = max(df.at[cid, 'High'], price)
                df.at[cid, 'Low'] = min(df.at[cid, 'Low'], price)
                df.at[cid, 'Close'] = price
            
            # Indicators
            if len(df) > 20:
                if ta:
                    df['EMA9'] = df.ta.ema(length=9)
                    df['SMA20'] = df.ta.sma(length=20)
                else:
                    df['EMA9'] = df['Close'].ewm(span=9).mean()
            st.session_state.histories[sym] = df

        # Plotting
        if not df.empty:
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name=sym)])
            if 'EMA9' in df.columns:
                fig.add_trace(go.Scatter(x=df.index, y=df['EMA9'], line=dict(color='cyan', width=1), name="9 EMA"))
            fig.update_layout(template="plotly_dark", height=400, margin=dict(l=10, r=10, t=30, b=10), title=sym, xaxis_rangeslider_visible=False)
            placeholders[i].plotly_chart(fig, use_container_width=True)
            
    time.sleep(1)