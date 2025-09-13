import ccxt
import pandas as pd
import ta
import time

# ==== SETUP ====
exchange = ccxt.binance({
    'apiKey': 'your api key',
    'secret': 'your secret key',
    'enableRateLimit': True
})

symbol = 'BTC/USDT'
timeframe = '15m'

# Risk settings
risk_per_trade = 0.01      # 1% of account
stop_loss_pct = 0.02        # 2% below entry
take_profit_pct = 0.04      # 4% above entry

# State
position = None
entry_price = 0.0
pnl = 0.0

# ==== HELPER FUNCTIONS ====
def get_balance():
    balance = exchange.fetch_balance()
    return balance['total']['USDT']

def fetch_data():
    bars = exchange.fetch_ohlcv(symbol, timeframe, limit=100)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return df

def place_order(side, amount):
    order = exchange.create_market_order(symbol, side, amount)
    print(f"{side.upper()} ORDER executed at avg price: {order['average']}")
    return float(order['average'])

# ==== STRATEGY ====
def rsi_strategy(df):
    global position, entry_price, pnl

    df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
    last_rsi = df['rsi'].iloc[-1]
    last_close = df['close'].iloc[-1]

    balance = get_balance()
    risk_amount = balance * risk_per_trade  # $ risk
    trade_amount = risk_amount / last_close # BTC size

    if last_rsi < 30 and position is None:
        entry_price = place_order('buy', trade_amount)
        position = {'side': 'long', 'amount': trade_amount}
        print(f"BUY at {entry_price}, size: {trade_amount:.6f} BTC")

    elif position is not None:
        # Check SL / TP
        stop_price = entry_price * (1 - stop_loss_pct)
        tp_price = entry_price * (1 + take_profit_pct)

        if last_close <= stop_price:
            exit_price = place_order('sell', position['amount'])
            loss = (exit_price - entry_price) * position['amount']
            pnl += loss
            print(f"STOP-LOSS hit at {exit_price} | Loss: {loss:.2f} | Total PnL: {pnl:.2f}")
            position = None

        elif last_close >= tp_price:
            exit_price = place_order('sell', position['amount'])
            profit = (exit_price - entry_price) * position['amount']
            pnl += profit
            print(f"TAKE-PROFIT hit at {exit_price} | Profit: {profit:.2f} | Total PnL: {pnl:.2f}")
            position = None

        elif last_rsi > 70:
            exit_price = place_order('sell', position['amount'])
            profit = (exit_price - entry_price) * position['amount']
            pnl += profit
            print(f"RSI SELL at {exit_price} | Profit: {profit:.2f} | Total PnL: {pnl:.2f}")
            position = None

        else:
            print("HOLD position")

    else:
        print("HOLD (no position)")
