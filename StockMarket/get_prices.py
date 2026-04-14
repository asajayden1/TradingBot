from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

def get_prices(symbol, days=200):
    """
    Fetches historical daily closing prices for a stock.
    Returns a list of floats.
    """

    end = datetime.now()
    start = end - timedelta(days=days)

    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=start,
        end=end
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
    symbol = "AAPL"  # i can change this to other stocks
    prices = get_prices(symbol)

    print("Number of prices:", len(prices))
    print("Most recent prices:", prices[-5:])
