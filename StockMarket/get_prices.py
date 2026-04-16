from dotenv import load_dotenv
import os
from datetime import date, timedelta

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed

load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# Use the FREE IEX feed
data_client = StockHistoricalDataClient(
    API_KEY,
    SECRET_KEY,
    feed=DataFeed.IEX
)

def get_prices(symbol, days=200):
    """
    Fetches historical daily closing prices for a stock.
    Returns a list of floats.
    """

    # FIX: Use date-only values to avoid future timestamps and timezone drift
    end = date.today()
    start = end - timedelta(days=days)

    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=start.isoformat(),   # date-only, safe
        end=end.isoformat(),       # date-only, safe
        feed=DataFeed.IEX          # force free feed
    )

    bars = data_client.get_stock_bars(request)
    df = bars.df

    if df.empty:
        print(f"No data returned for {symbol}. Try a different ticker.")
        return []

    closes = df["close"].tolist()
    return closes


# test
if __name__ == "__main__":
    symbol = "AAPL"
    prices = get_prices(symbol)

    print("Number of prices:", len(prices))
    print("Most recent prices:", prices[-5:])
