from datetime import datetime, timedelta
import csv
import logging
import os


class HistoricalDataRepository:
    def __init__(self, root_folder):
        self.root_folder = root_folder

    def tick_iterator(self, instrument, start_date, end_date):
        try:
            start_date_string = 'beginning of file' if start_date is None else start_date.strftime('%Y/%m/%d')
            filename = os.path.join(self.root_folder, '{}.csv'.format(instrument))
            logging.debug('Will attempt to read ticks in {}, from {} to {}...'.format(filename, start_date_string,
                                                                                      end_date.strftime('%Y/%m/%d')))
            file = open(filename)
            reader = csv.reader(file)
            should_run = True
            while should_run:
                next(reader, None)  # skip headers
                for row in reader:
                    time = datetime.strptime(row[0], '%Y%m%d %X:%f')  # use https://strftime.org/
                    time = time + timedelta(hours=1)  # this is because das ist Deutschland
                    if start_date is not None and time < start_date:
                        continue
                    bid_price = round(float(row[1]), 6)
                    ask_price = round(float(row[2]), 6)
                    tick = Tick(time, bid_price, ask_price)
                    yield tick
                should_run = False
        except FileNotFoundError as e:
            logging.error(e)


class Tick:
    def __init__(self, time, bid, ask):
        self.time = time
        self.bid = bid
        self.ask = ask

    def to_dict(self):
        return {
            'timestamp': self.time,
            'bid': self.bid,
            'ask': self.ask
        }

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{}: b({}) a({})'.format(str(self.time)[:-4], self.bid, self.ask)


