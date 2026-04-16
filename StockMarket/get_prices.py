from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed

load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# Use IEX feed (free)
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

    # FIX: Use UTC to avoid future timestamps
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)

    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=start,
        end=end,
        feed=DataFeed.IEX  # force free feed
    )

    bars = data_client.get_stock_bars(request)
    df = bars.df

    if df.empty:
        print(f"No data returned for {symbol}. Try a different ticker.")
        return []

    closes = df['close'].tolist()
    return closes


# test
if __name__ == "__main__":
    symbol = "AAPL"
    prices = get_prices(symbol)

    print("Number of prices:", len(prices))
    print("Most recent prices:", prices[-5:])
