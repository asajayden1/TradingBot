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

# Connect to Alpaca
client = TradingClient(API_KEY, SECRET_KEY, paper=True)

SYMBOL = "AAPL"   # You can change this to any stock you want
QTY = 1           # Number of shares to buy/sell


def get_current_position(symbol):
    """
    Returns how many shares of the symbol you currently hold.
    """
    try:
        position = client.get_open_position(symbol)
        return float(position.qty)
    except Exception:
        return 0  # no position


def place_order(side, qty, symbol):
    """
    Places a market order (BUY or SELL).
    """
    order = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=side,
        time_in_force=TimeInForce.DAY
    )
    client.submit_order(order)
    print(f"ORDER PLACED: {side} {qty} shares of {symbol}")


def run_bot():
    print(f"Fetching prices for {SYMBOL}...")
    prices = get_prices(SYMBOL)

    if len(prices) < 50:
        print("Not enough data to run strategy.")
        return

    shares_held = get_current_position(SYMBOL)
    print(f"Currently holding {shares_held} shares.")

    signal = get_signal(prices, shares_held)
    print(f"Strategy signal: {signal}")

    if signal == "BUY":
        place_order(OrderSide.BUY, QTY, SYMBOL)

    elif signal == "SELL":
        place_order(OrderSide.SELL, QTY, SYMBOL)

    else:
        print("No action taken.")


if __name__ == "__main__":
    run_bot()
