from dotenv import load_dotenv
import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from get_prices import get_prices
from strategy import get_signal

load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# Connect to Alpaca paper trading
client = TradingClient(API_KEY, SECRET_KEY, paper=True)

# Dictionary of companies to trade
# Removed TSLA (too volatile), added GOOGL and META (stable growth)
COMPANIES = {
    "AAPL":  {"name": "Apple",     "qty": 1},
    "MSFT":  {"name": "Microsoft", "qty": 1},
    "NVDA":  {"name": "NVIDIA",    "qty": 1},
    "GOOGL": {"name": "Google",    "qty": 1},
    "META":  {"name": "Meta",      "qty": 1},
    "AMZN":  {"name": "Amazon",    "qty": 1},
}


def get_current_position(symbol):
    """Returns how many shares of the symbol you currently hold."""
    try:
        position = client.get_open_position(symbol)
        return float(position.qty)
    except Exception:
        return 0


def place_order(side, qty, symbol):
    """Places a market order (BUY or SELL) and prints the order ID."""
    order = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=side,
        time_in_force=TimeInForce.DAY
    )
    result = client.submit_order(order)
    print(f"  ORDER PLACED: {side} {qty} share(s) of {symbol} | Order ID: {result.id}")


def run_bot():
    print("=" * 50)
    print("TRADING BOT STARTING")
    print("=" * 50)

    for symbol, info in COMPANIES.items():
        print(f"\n[{symbol}] {info['name']}")

        prices = get_prices(symbol)
        if len(prices) < 51:
            print(f"  Not enough data for {symbol}, skipping.")
            continue

        shares_held = get_current_position(symbol)
        print(f"  Shares held: {shares_held}")

        signal = get_signal(prices, shares_held)
        print(f"  Signal: {signal}")

        qty = info["qty"]
        if signal == "BUY":
            place_order(OrderSide.BUY, qty, symbol)
        elif signal == "SELL":
            place_order(OrderSide.SELL, qty, symbol)
        else:
            print(f"  No action taken.")

    print("\n" + "=" * 50)
    print("TRADING BOT FINISHED")
    print("=" * 50)


if __name__ == "__main__":
    run_bot()