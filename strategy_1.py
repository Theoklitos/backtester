def on_new_candlestick(candles):
    if len(candles) < 14:
        return False, None, None

    # current_time = candles[-1].end_time
    # if (current_time.hour < 8) or (current_time.hour > 11):
    #    return False, None, None

    # candles need to be within a certain range
    upper_bound = max(candles, key=lambda x: x.bid_high).bid_high
    lower_bound = min(candles, key=lambda x: x.bid_low).bid_low
    difference = abs(upper_bound - lower_bound)
    if 'JPY' in candles[0].instrument:
        difference_in_pips = round(difference * 100, 1)
    else:
        difference_in_pips = round(difference * 10000, 1)
    if difference_in_pips > 30:
        return False, None, None

    number_of_bull_candles = 0
    number_of_bear_candles = 0
    for candle in candles:
        if candle.bid_close > candle.bid_open:
            number_of_bull_candles += 1
        else:
            number_of_bear_candles += 1

    trade_type = None
    if number_of_bull_candles >= 9:
        trade_type = 'sell'
    elif number_of_bear_candles >= 9:
        trade_type = 'buy'

    debug_info = {}
    if trade_type is not None:
        debug_info['text'] = 'Margin is {} pips, from |{} - {}| = {}'.format(difference_in_pips,
                                                                             upper_bound, lower_bound,
                                                                             difference_in_pips)

    return trade_type is not None, trade_type, debug_info
