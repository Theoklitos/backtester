import plotly.graph_objects as go


def write_candles_to_html_file(filename, candles, title=''):
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

    figure = go.Figure(data=[go.Candlestick(x=dates, open=open_data, high=high_data, low=low_data, close=close_data,
                                            increasing_line_color='white', decreasing_line_color='black')])
    figure.update_layout(title=title)
    figure.write_html(filename)


def write_trades_to_html_file(filename, trades):
    total_pips = 0
    trade_graph_data = {'x': [], 'y': [], 'text': []}
    monthly_status_graph_data = {'x': [], 'y': [], 'text': []}
    current_month = None

    for trade in trades:
        if current_month is None:
            current_month = trade.end_time.strftime("%B %Y")
        if trade.end_time is None:
            continue
        trade_end_month = trade.end_time.strftime("%B %Y")
        if trade_end_month != current_month:
            monthly_status_graph_data['x'].append(current_month)
            monthly_status_graph_data['y'].append(total_pips)
            current_month = trade_end_month

        trade_graph_data['x'].append(trade.start_time)
        trade_graph_data['y'].append(total_pips)
        trade_graph_data['text'].append('{}, started'.format(trade.trade_type))

        if trade.status == 'closed':
            total_pips += trade.get_profit()
            trade_graph_data['x'].append(trade.end_time)
            trade_graph_data['y'].append(total_pips)
            trade_graph_data['text'].append('{}, closed because "{}",'.format(trade.trade_type, trade.close_reason))

    if len(trades) > 0:
        if trades[-1].end_time is None:
            monthly_status_graph_data['x'].append(trades[-2].end_time.strftime("%B %Y"))
        else:
            monthly_status_graph_data['x'].append(trades[-1].end_time.strftime("%B %Y"))
        monthly_status_graph_data['y'].append(total_pips)

    figure = go.Figure()
    figure.add_trace(go.Scatter(x=trade_graph_data['x'], y=trade_graph_data['y'], text=trade_graph_data['text'],
                                mode='lines+markers', name='lines+markers', line_shape='linear'))
    #figure.update_layout(title=title, xaxis_title="Time", yaxis_title="Profit (pips)")
    figure.write_html(filename)

    figure_monthly = go.Figure()
    figure_monthly.add_trace(go.Scatter(x=monthly_status_graph_data['x'], y=monthly_status_graph_data['y'],
                                mode='lines+markers', name='lines+markers', line_shape='linear'))
    figure_monthly.write_html(filename.replace('.html', '_months.html'))
