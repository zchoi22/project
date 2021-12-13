from pandas_datareader.data import get_data_yahoo as get_data
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, date
yf.pdr_override()


class stock:

    #inputs = ticker, uses ticker to grab stats
    def __init__(self, ticker, filepath_start, *args):
        self.ticker = ticker.upper()
        self.filepath = filepath_start+self.ticker+'.csv'
        self.start_date = datetime.now() - timedelta(days=365)
        self.end_date = date.today()
        if args == ():
            try:
                self.format_data()
            except:
                self.build_data()
        else:
            self.update_data()

    def build_data(self):
        ticker_data = get_data(self.ticker, self.start_date, self.end_date)
        ticker_data.to_csv(self.filepath)
        self.format_data()

    def format_data(self):
        self.data = pd.read_csv(self.filepath, index_col = 0)

    def update_data(self):
        try:
            self.format_data()
            last_date = self.str_to_date(self.data.reset_index()['Date'].iloc[-1])
            end_date = self.end_date
            if datetime.now().weekday() >= 5:
                end_date = datetime.now() - timedelta(days = (end_date.weekday()-4))
            if last_date == end_date.date():
                pass
            else:
                ticker_data = get_data(self.ticker, last_date, end_date)
                ticker_data.to_csv(self.filepath, mode = 'a', header = False)
        except:
            self.build_data()

    def str_to_date(self, date):
        return datetime.strptime(date, '%Y-%m-%d').date()

    def get_data(self):
        return self.data

    def get_sma(self, days):
        return round(self.data['Adj Close'].rolling(window=days).mean(), 2)

    def get_price(self):
        return self.data['Adj Close'][-1]

    def get_sma_20(self):
        return self.get_sma(20)[-1]

    def get_sma_50(self):
        return self.get_sma(50)[-1]

    def get_sma_200(self):
        return self.get_sma(200)[-1]

    def get_52week_high(self):
        return round(min(self.data['Low'][-260:-1]), 2)

    def get_52week_low(self):
        return round(max(self.data['High'][-260:-1]), 2)

    def get_volume(self):
        return self.data['Volume'][-1]