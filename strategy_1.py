def on_new_candlestick(candles):
    if len(candles) < 14:
        return False, None
    current_time = candles[-1].end_time
    if (current_time.hour < 8) or (current_time.hour > 12):
        return False, None

    number_of_interesting_candles = 0
    for candle in candles:
        if abs(candle.bid_open - candle.bid_close) < 0.002:
            number_of_interesting_candles = number_of_interesting_candles + 1
    trade_type = 'buy' if (candles[-1].bid_open < candles[-1].bid_close) else 'sell'

    return number_of_interesting_candles > 8, trade_type
