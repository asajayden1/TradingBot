def moving_average(prices, window):
    """
    Returns the simple moving average for the last `window` prices.
    """
    if len(prices) < window:
        return None
    return sum(prices[-window:]) / window


def get_signal(prices, shares_held):
    """
    Determines whether to BUY, SELL, or HOLD based on moving average crossover.
    
    Rules:
    BUY when 10-day MA crosses ABOVE 50-day MA and you hold 0 shares.
    SELL when 10-day MA crosses BELOW 50-day MA and you hold shares.
    Otherwise HOLD.
    """

    
    if len(prices) < 51:
        return "NOT_ENOUGH_DATA"

    
    ma10 = moving_average(prices, 10)
    ma50 = moving_average(prices, 50)

    
    prev_ma10 = moving_average(prices[:-1], 10)
    prev_ma50 = moving_average(prices[:-1], 50)

    
    if None in (ma10, ma50, prev_ma10, prev_ma50):
        return "NOT_ENOUGH_DATA"

    # buy if 10-day crosses above 50 day
    if prev_ma10 <= prev_ma50 and ma10 > ma50 and shares_held == 0:
        return "BUY"

    # sell if 10-day crosses below 50 day
    if prev_ma10 >= prev_ma50 and ma10 < ma50 and shares_held > 0:
        return "SELL"

    
    return "HOLD"


# test
if __name__ == "__main__":
    # fake price for test s
    example_prices = [1,2,3,4,5] * 20  # 100 data points
    print(get_signal(example_prices, shares_held=0))
