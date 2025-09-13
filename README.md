# Crypto RSI Trading Bot

## 📌 Overview
This bot uses the **Relative Strength Index (RSI)** strategy to trade **BTC/USDT** on the **Binance** exchange via the **ccxt** library.  
It automatically buys or sells based on RSI signals and predefined profit/loss conditions.

---

## ⚙️ How It Works

1. **Connect to Binance** using your API keys via the `ccxt` library.
2. **Fetch market data**: downloads the last 100 candles of 15-minute BTC/USDT price data.
3. **Calculate RSI** using the `ta` technical analysis library.
4. **Trading Logic**:
   - **Buy Signal**:  
     - If RSI < 30  
     - And no current open position  
     - → Buys BTC worth 1% of current USDT balance.
   - **Sell Signals** (if a position is open):  
     - Price drops 2% below entry → Sell (stop loss)  
     - Price rises 4% above entry → Sell (take profit)  
     - RSI > 70 → Sell (overbought condition)
5. **Profit & Loss Tracking**: Each sell logs the profit/loss and adds it to your running `pnl`.

---

## 💸 Effects on Your Binance Account

- Uses **real funds** if real API keys with trading permission are used.
- **Places market orders** automatically for BTC/USDT pair.
- Each trade uses about **1% of your available USDT balance**.
- **Gains or losses will be real** and depend on market movement.
- **Trading fees are not included** in calculations (they still apply).

---

## ⚠️ Warnings

- ❗ This is a **real trading bot** — it can **lose money**.
- ❗ No error handling — API errors or balance issues can break the script.
- ❗ No fee handling — profits may be lower than shown.
- ❗ RSI is not always reliable, especially in trending markets.
- ❗ No `time.sleep()` is added yet — if looped without delays, it can spam trades.
- ❗ Test with **small amounts** or on a **testnet** before using real money.

---

## 🚀 Future Improvements (Optional)
- Add `while True` loop with `time.sleep(900)` (15-min delay).
- Add `try/except` for error handling.
- Add CSV logging of trades.
- Add fee calculation and better position sizing.

---

## ⚡ Requirements

- Python 3.8+
- [ccxt](https://github.com/ccxt/ccxt)
- [ta](https://github.com/bukosabino/ta)
- pandas

Install via:

```bash
pip install ccxt ta pandas
