from historical_tester import HistoricalTester
import logging
import datetime
import sys

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', stream=sys.stdout)
    tester = HistoricalTester()

    now = datetime.datetime.now()
    strategy_config = {
        'instruments': ['EURCHF-twoyears', 'CADCHF-twoyears', 'EURAUD-twoyears', 'EURCAD-twoyears', 'AUDCHF-twoyears',
                        'EURNZD-twoyears', 'NZDCHF-twoyears', 'CHFJPY-lastyear', 'EURJPY-lastyear'],
        #'instruments': ['EURCHF-edgecase'],
        #'instruments': ['NZDCHF-lastmonth', 'EURNZD-lastmonth', 'EURCHF-lastmonth'],
        'start_date': None,  # e.g. datetime.datetime(2020, 4, 4, 0, 0, 0),
        'end_date': now,
        'sl': 8,
        'tp': 20
    }

    tester.test_strategy_1(strategy_config)
    logging.debug('Main method terminated.')



