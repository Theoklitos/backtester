import logging
from tqdm import tqdm
from datetime import timedelta
from data_repository import HistoricalDataRepository
from graph_stuff import write_candles_to_html_file
from decimal import *


class Trade:
    def __init__(self, _id, start_time, trade_type, starting_price, current_price=0):
        self.id = _id
        self.start_time = start_time
        self.end_time = None
        self.trade_type = trade_type
        self.status = 'open'
        self.close_reason = None
        self.starting_price = starting_price
        self.current_price = current_price

    def get_profit(self):
        value = None
        if self.trade_type == 'buy':
            value = Decimal(self.current_price) - Decimal(self.starting_price)
        elif self.trade_type == 'sell':
            value = Decimal(self.starting_price) - Decimal(self.current_price)
        pip_position = (10000, 5)
        profit_pips = round(value * pip_position[0], pip_position[1])
        return round(profit_pips, 1)

    def close(self, tick, reason):
        self.status = 'closed'
        self.close_reason = reason
        logging.debug('Trade closed due to {} at {}. Profit: {}'.format(reason, tick.time, self.get_profit()))
        self.end_time = tick.time

    def to_file_string(self):
        if self.status == 'open':
            return 'Must be closed!'

        duration = str(self.end_time - self.start_time)[:-7]
        return 'Trade #{}: opened at {} and closed {} due to "{}". Duration: {}. Start price: {}, end: {}. Profit: {}'\
            .format(self.id, str(self.start_time)[:-6], str(self.end_time)[:-6], self.close_reason, duration,
                    self.starting_price, self.current_price, self.get_profit())

    def __str__(self):
        profit_string = ' Profit: {} pip(s)'.format(self.get_profit()) if self.get_profit() != 0 else ''
        end_time_string = ' and ended at {}'.format(self.end_time) if self.end_time is not None else ''
        return '{} ({}) started at {}{} with starting price: {}, current price: {}.'\
            .format(self.status, self.trade_type, self.start_time, end_time_string, self.starting_price,
                    self.current_price, profit_string)


class Candlestick:
    def __init__(self, instrument, start_time, end_time, period,
                 bid_open, bid_close, bid_high, bid_low, ask_open, ask_close, ask_high, ask_low):
        self.instrument = instrument
        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        self.bid_open = bid_open
        self.bid_close = bid_close
        self.bid_high = bid_high
        self.bid_low = bid_low
        self.ask_open = ask_open
        self.ask_close = ask_close
        self.ask_high = ask_high
        self.ask_low = ask_low

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{} duration({}), from {} to {}: open b({}) a({}), close b({}) a({}), high b({}) a({}), low b({}) a({})'\
            .format(self.instrument, self.period, self.start_time, self.end_time, self.bid_open, self.ask_open,
                    self.bid_close, self.ask_close, self.bid_high, self.ask_high, self.bid_low, self.ask_low)


def _maintain_trades(trades, tick, sl, tp):
    open_trade = list(filter(lambda trade: trade.status == 'open', trades))
    if open_trade:
        open_trade = open_trade[0]
        open_trade.current_price = tick.bid if open_trade.trade_type == 'buy' else tick.ask
        profit = open_trade.get_profit()
        trade_closed = False

        if tick.time.hour > 12:  # close trade if its too late in the date
            open_trade.close(tick, 'time')
            trade_closed = True
        elif profit >= tp:
            open_trade.close(tick, 'TP')
            trade_closed = True
        elif profit <= -sl:
            open_trade.close(tick, 'SL')
            trade_closed = True

        return trade_closed


def are_all_trades_closed(trades):
    return all(trade.status == 'closed' for trade in trades)


def process_ticks_and_apply_strategy(instrument, start_date, end_date, sl, tp, on_new_candle):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
    logging.debug('Starting test for {}...'.format(instrument))

    repository = HistoricalDataRepository('historical-data')
    tick_buffer = []
    candle_buffer = []
    max_candle_buffer_size = 15
    candle_period = timedelta(hours=1)
    trades = []

    for tick in tqdm(repository.tick_iterator(instrument, start_date, end_date)):
        trade_closed = _maintain_trades(trades, tick, sl, tp)

        should_create_new_candle = False

        if len(tick_buffer) > 0:
            if candle_period == timedelta(seconds=1):
                should_create_new_candle = tick.time.second > tick_buffer[-1].time.second
            elif candle_period == timedelta(hours=1):
                should_create_new_candle = tick.time.hour > tick_buffer[-1].time.hour

        if should_create_new_candle:
            # create new candlestick
            start_time = tick_buffer[0].time
            end_time = tick_buffer[-1].time
            bid_open = tick_buffer[0].bid
            ask_open = tick_buffer[0].ask
            bid_close = tick_buffer[-1].bid
            ask_close = tick_buffer[-1].ask
            bid_high = max(tick_buffer, key=lambda t: t.bid).bid
            ask_high = max(tick_buffer, key=lambda t: t.ask).ask
            bid_low = min(tick_buffer, key=lambda t: t.bid).bid
            ask_low = min(tick_buffer, key=lambda t: t.ask).ask
            candlestick = Candlestick(instrument, start_time, end_time, candle_period, bid_open, bid_close, bid_high,
                                      bid_low, ask_open, ask_close, ask_high, ask_low)
            candle_buffer.append(candlestick)
            if len(candle_buffer) > max_candle_buffer_size:
                del candle_buffer[0]

            (should_open_trade, trade_type) = on_new_candle(candle_buffer)  # callback
            if are_all_trades_closed(trades) and should_open_trade and not trade_closed:
                start_time = candle_buffer[-1].end_time
                starting_price = tick.bid if trade_type == 'buy' else tick.ask
                trade_id = len(trades)
                new_trade = Trade(trade_id, start_time, trade_type, starting_price, starting_price)
                trades.append(new_trade)
                logging.debug('Started new trade: {}'.format(new_trade))
                write_candles_to_html_file("C:\\Users\\Takis\\Desktop\\output\\{}.html".format(trade_id), candle_buffer)

            del tick_buffer[:]

        tick_buffer.append(tick)

    logging.info('Done!\n')
    for trade in trades:
        print(trade.to_file_string())
    print("==============================================\n")
    total_pips = sum(trade.get_profit() for trade in trades)
    print('Total profit: {} pips.'.format(total_pips))
