#https://timber.io/blog/multiprocessing-vs-multithreading-in-python-what-you-need-to-know/
import multiprocessing
import logging
import strategy_1
from tick_processing import process_ticks_and_apply_strategy


class HistoricalTester:
    def __init__(self,):
        self.processes = []

    def test_strategy_1(self, config):
        instruments = config['instruments']
        logging.info('Starting historical tests for instruments: {}...'.format(instruments))
        for instrument in instruments:
            strategy = strategy_1.on_new_candlestick
            sl, tp = config['sl'], config['tp']
            start_date, end_date = config['start_date'], config['end_date']
            process = multiprocessing.Process(target=process_ticks_and_apply_strategy,
                                              args=(instrument, start_date, end_date, sl, tp, strategy))
            process.start()
            self.processes.append(process)

