from historical_tester import HistoricalTester
import logging
import datetime

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
    tester = HistoricalTester()

    now = datetime.datetime.now()
    strategy_config = {
        'instruments': ['EURCHF'],
        'start_date': None,  # e.g. datetime.datetime(2020, 4, 4, 0, 0, 0),
        'end_date': now,
        'sl': 7,
        'tp': 15
    }

    tester.test_strategy_1(strategy_config)
    logging.debug('Main method terminated.')



