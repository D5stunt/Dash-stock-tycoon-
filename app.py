import streamlit as st
import pandas as pd

st.set_page_config(page_title='Dash Stock Tycoon V12', page_icon='📈', layout='centered')
STOCKS = {'AAPL': ('Apple', 175.0), 'TSLA': ('Tesla', 250.0), 'NVDA': ('NVIDIA', 120.0), 'MSFT': ('Microsoft', 350.0), 'AMZN': ('Amazon', 180.0), 'GOOGL': ('Alphabet', 160.0), 'META': ('Meta', 300.0), 'AMD': ('AMD', 140.0)}
if 'cash' not in st.session_state:
    st.session_state.cash = 150.0
    st.session_state.positions = {}
    st.session_state.day = 1
    st.session_state.prices = {k: v[1] for k,v in STOCKS.items()}
    st.session_state.message = 'Welcome! All prices and money are simulated.'

st.title('📈 Dash Stock Tycoon V12')
st.caption('Python Edition • Fake money • Offline simulated prices • No real trades')
positions = st.session_state.positions
prices = st.session_state.prices
value = sum(p['units'] * max(0., p['basis'] + p['mult'] * (prices[k] - p['basis'])) for k,p in positions.items())
net = st.session_state.cash + value
c1,c2,c3 = st.columns(3)
c1.metric('Cash', f'${st.session_state.cash:,.2f}')
c2.metric('Portfolio', f'${value:,.2f}')
c3.metric('Net worth', f'${net:,.2f}')
st.progress(min(1., max(0., net / 1000)))
st.write(f'**Goal:** $1,000 | **Trading day:** {st.session_state.day}')
st.subheader('Market (demo prices)')
st.dataframe(pd.DataFrame([{'Symbol': k, 'Company': v[0], 'Price ($)': round(prices[k], 2)} for k,v in STOCKS.items()]), hide_index=True, use_container_width=True)

symbol = st.selectbox('Choose stock', list(STOCKS), format_func=lambda x: f'{x} — {STOCKS[x][0]}')
qty = st.number_input('Shares', min_value=0.01, value=0.1, step=0.01, format='%.2f')
mult = st.selectbox('Multiplier (applies to price movement after buying)', [1,2,5,10], format_func=lambda x: f'{x}×')

def buy():
    price = prices[symbol]
    cost = price * qty
    if symbol in positions and positions[symbol]['mult'] != mult:
        st.session_state.message = 'Sell your existing position before changing its multiplier.'
    elif cost > st.session_state.cash + 1e-8:
        st.session_state.message = 'Not enough fake cash.'
    else:
        if symbol not in positions:
            positions[symbol] = {'units': 0.0, 'basis': price, 'mult': mult}
        p = positions[symbol]
        p['basis'] = (p['basis'] * p['units'] + price * qty) / (p['units'] + qty)
        p['units'] += qty
        st.session_state.cash -= cost
        st.session_state.message = f'Bought {qty:.2f} {symbol} shares (simulated).'

def sell():
    if symbol not in positions or positions[symbol]['units'] + 1e-8 < qty:
        st.session_state.message = 'You do not own enough shares.'
        return
    p = positions[symbol]
    # Leveraged position payoff: basis + multiplier * price movement, floored at zero.
    payout_per_share = max(0., p['basis'] + p['mult'] * (prices[symbol] - p['basis']))
    st.session_state.cash += payout_per_share * qty
    p['units'] -= qty
    if p['units'] < 1e-8:
        del positions[symbol]
    st.session_state.message = f'Sold {qty:.2f} {symbol} shares for ${payout_per_share * qty:.2f} fake dollars.'

left, right = st.columns(2)
left.button('🟢 Buy', on_click=buy, use_container_width=True)
right.button('🔴 Sell', on_click=sell, use_container_width=True)
st.info(st.session_state.message)
st.caption('Multipliers affect simulated sell value. Portfolio summary below includes leveraged value.')
if positions:
    st.subheader('Your positions')
    rows=[]
    for k,p in positions.items():
        unit_value=max(0., p['basis']+p['mult']*(prices[k]-p['basis']))
        rows.append({'Stock':k,'Shares':round(p['units'],4),'Multiplier':f"{p['mult']}×",'Value ($)':round(p['units']*unit_value,2)})
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
else:
    st.write('No stocks owned yet. Buy a fraction of a share to start!')

st.subheader('Market controls')
if st.button('⏭ Next simulated trading day', use_container_width=True):
    import random
    for k in prices:
        prices[k] = max(0.01, prices[k] * (1 + random.uniform(-0.06, 0.06)))
    st.session_state.day += 1
    st.rerun()
if st.button('🔄 Reset game', use_container_width=True):
    for k in ['cash','positions','day','prices','message']:
        del st.session_state[k]
    st.rerun()
st.caption('Educational simulation only. No live quotes, real accounts, or real-money trading. Session progress may reset when the app restarts.')
