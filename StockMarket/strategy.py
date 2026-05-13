from bst import BST


def moving_average(prices, window):
    """Simple moving average over the last `window` prices."""
    if len(prices) < window:
        return None
    return sum(prices[-window:]) / window


def compute_rsi(prices, period=14):
    """
    Computes the Relative Strength Index (RSI).
    RSI > 70 = overbought (avoid buying)
    RSI < 30 = oversold (good buying opportunity)
    """
    if len(prices) < period + 1:
        return None

    gains = []
    losses = []

    for i in range(-period, 0):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    if avg_loss == 0:
        return 100  # fully overbought

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def get_price_position(prices):
    """
    Uses a BST to determine where the current price sits
    relative to the historical range (as a percentage).
    0% = at historical low, 100% = at historical high.
    """
    bst = BST()
    bst.build_from_prices(prices)

    min_price = bst.get_min()
    max_price = bst.get_max()
    current = prices[-1]

    if max_price == min_price:
        return 50.0  # avoid division by zero

    position = (current - min_price) / (max_price - min_price) * 100
    return round(position, 2)


def get_signal(prices, shares_held):
    """
    Determines whether to BUY, SELL, or HOLD.

    Strategy:
    - Uses 10/50-day MA crossover as the primary signal
    - Uses RSI to filter out overbought/oversold conditions
    - Uses BST price position to avoid buying near all-time highs

    BUY when:
      - 10-day MA crosses above 50-day MA
      - RSI is below 70 (not overbought)
      - Current price is not in the top 85% of its historical range
      - No shares currently held

    SELL when:
      - 10-day MA crosses below 50-day MA
      - OR RSI goes above 75 (very overbought — take profit)
      - Shares are currently held
    """
    if len(prices) < 51:
        return "NOT_ENOUGH_DATA"

    ma10 = moving_average(prices, 10)
    ma50 = moving_average(prices, 50)
    prev_ma10 = moving_average(prices[:-1], 10)
    prev_ma50 = moving_average(prices[:-1], 50)

    if None in (ma10, ma50, prev_ma10, prev_ma50):
        return "NOT_ENOUGH_DATA"

    rsi = compute_rsi(prices)
    price_position = get_price_position(prices)

    print(f"  MA10={ma10:.2f} MA50={ma50:.2f} RSI={rsi:.1f} PricePosition={price_position}%")

    # SELL logic
    if shares_held > 0:
        ma_crossdown = prev_ma10 >= prev_ma50 and ma10 < ma50
        rsi_overbought = rsi is not None and rsi > 75
        if ma_crossdown or rsi_overbought:
            return "SELL"

    # BUY logic
    if shares_held == 0:
        ma_crossup = prev_ma10 <= prev_ma50 and ma10 > ma50
        rsi_ok = rsi is None or rsi < 70
        price_not_too_high = price_position < 85
        if ma_crossup and rsi_ok and price_not_too_high:
            return "BUY"

    return "HOLD"


# test
if __name__ == "__main__":
    example_prices = list(range(1, 101))  # 100 rising prices
    signal = get_signal(example_prices, shares_held=0)
    print("Signal:", signal)