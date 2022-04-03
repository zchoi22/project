from pandas_datareader.data import get_data_yahoo as get_data
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, date
yf.pdr_override()


class stock:

    #inputs = ticker, uses ticker to grab stats
    def __init__(self, ticker, filepath='..\\project\\main\\stock\\historical_data\\', update=False):
        self.ticker = ticker.upper()
        self.filepath = filepath+self.ticker+'.csv'
        self.start_date = datetime.now() - timedelta(days=365)
        self.end_date = date.today()
        #if args is empty, will try to set the data by reading from appropriate csv file
        #if there is no csv file, initialization will build a new file then set data to
        #the historical data from that file
        if update==False:
            try:
                self.format_data()
            except:
                self.build_data()
        #if there is a request to update data (from screener or elsewhere), it will
        #update the current data to the current date using datetime and yfinance libraries
        else:
            self.update_data()

    #for a given stock, it will grab YTD data from yfianance and export the data to a csv file
    def build_data(self):
        ticker_data = get_data(self.ticker, self.start_date, self.end_date)
        ticker_data.to_csv(self.filepath)
        self.format_data()

    #sets self.data to the data read from respective csv document, reads in as a PD series
    def format_data(self):
        self.data = pd.read_csv(self.filepath, index_col = 0)

    #method for updating data
    def update_data(self):
        try:
        #if there exists a csv file, will grab the information to determine if an update
        #is needed. Uses datetime to compare last date in respective file to current date to
        #check. If an update is required, new data is appended to the csv file than read in
        #by the format data method
            self.format_data()
            last_date = self.str_to_date(self.data.reset_index()['Date'].iloc[-1])
            end_date = self.end_date
            if datetime.now().weekday() >= 5:
                end_date = datetime.now() - timedelta(days = (end_date.weekday()-4))
            if last_date == end_date:
                print('working')
                pass
            else:
                print(self.ticker + ' updating')
                ticker_data = get_data(self.ticker, last_date, end_date)
                ticker_data.to_csv(self.filepath, mode = 'a', header = False)
        #if there is now csv file to be read, than the method will build a new file
        except:
            print(self.ticker + ' building')
            self.build_data()

    #method to turn string of a date into a datetime object
    def str_to_date(self, date):
        return datetime.strptime(date, '%Y-%m-%d').date()

    #getter for data
    def get_data(self):
        return self.data

    #getter for simple moving averages, returns a PD dataframe with dates and
    #simples moving average
    def get_sma(self, days):
        return round(self.data['Adj Close'].rolling(window=days).mean(), 2)

    #getter for price, in this case we use the adj. close value
    def get_price(self):
        return self.data['Adj Close'][-1]

    #getter for 20SMA using get_sma method
    def get_sma_20(self):
        return self.get_sma(20)[-1]

    #getter for 50SMA using get_sma method
    def get_sma_50(self):
        return self.get_sma(50)[-1]

    #getter for 200SMA using get_sma_method
    def get_sma_200(self):
        return self.get_sma(200)[-1]

    #getter for 52 week low, by finding the minimum
    #value of the data's low column
    def get_52week_low(self):
        return round(min(self.data['Low'][-260:-1]), 2)

    #getter for 52 week high, by finding the maximum
    #value of the data's high column
    def get_52week_high(self):
        return round(max(self.data['High'][-260:-1]), 2)

    #getter for volume, grabs last index of volume column
    def get_volume(self):
        return self.data['Volume'][-1]