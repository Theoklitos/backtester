import pandas
from datetime import datetime
import plotly.graph_objects as go
import sys


def parser(date_string):
    return datetime.strptime(date_string, '%Y%m%d %X:%f')

data_frame = pandas.read_csv('historical-data//EURCHF-oneday.csv', names=['timestamp', 'bid', 'ask'], usecols=[0, 1, 2],
                             index_col=0, skiprows=1, date_parser=parser)

print(data_frame.index)
sys.exit(1)


#print(data_frame.index) #dtype='datetime64[ns]', name='timestamp', length=152712, freq=None)
#print(data_frame['bid']) #Name: bid, Length: 152712, dtype: float64
#print(data_frame['ask']) #Name: ask, Length: 152712, dtype: float64
#print(len(data_frame))

data_frame = data_frame.resample('1h').ohlc()

#print(data_frame['timestamp'])
#print(len(data_frame))
#print(data_frame)
#print(data_frame['timestamp'])
#print(data_frame['bid']['open'])
#print(data_frame.columns)

fig = go.Figure(data=go.Candlestick(x=data_frame.index,open=data_frame['ask']['open'],high=data_frame['ask']['high'],
                             low=data_frame['ask']['low'], close=data_frame['ask']['close']))
#fig.show()

#fig.write_html("C:\\Users\\Takis\\Desktop\\paw.html")