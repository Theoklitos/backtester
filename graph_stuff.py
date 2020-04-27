import plotly.graph_objects as go


def write_candles_to_html_file(filename, candles):
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    dates = []

    for candle in candles:
        dates.append(candle.start_time)
        open_data.append(candle.bid_open)
        high_data.append(candle.bid_high)
        low_data.append(candle.bid_low)
        close_data.append(candle.bid_close)

    fig = go.Figure(data=[go.Candlestick(x=dates, open=open_data, high=high_data, low=low_data, close=close_data,
                                         increasing_line_color='white', decreasing_line_color='black')])

    fig.write_html(filename)
