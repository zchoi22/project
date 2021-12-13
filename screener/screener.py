from stock.stock import stock as s
import pandas as pd
import numpy as np
from yahoo_fin.stock_info import tickers_sp500


class screener:

    #initialize with settings (empty), and a reference to the format
    def __init__(self, *args):
        self.settings = pd.Series([np.nan for i in range(7)])
        self.format = {'price': 0, 'volume': 1, '52_week_high': 2, '52_week_low': 3,
                       'moving_average_20': 4, 'moving_average_50' : 5, 'moving_average_200': 6,}
        tickers = tickers_sp500()
        self.tickers = [item.replace(".", "-") for item in tickers]
        if args!=():
            self.filename = args[0]+'.csv'

    #getter for settings
    def get_settings(self):
        return self.settings

    def get_format(self):
        return self.format

    #imports screener from screeener_name.csv, reads in as pd series
    def import_screener(self, screener_name):
        df = pd.read_csv(screener_name+'.csv', index_col = False, header = 0)
        self.settings = df.transpose()[0]

    #sets a specific setting
    def set_settings(self, setting, value):
        if type(setting) is int:
            self.settings[setting] = value
        elif type(setting) is str:
            self.settings[self.format[setting]] = value

    #saves given settings to screener_name.csv
    def save_screener(self, screener_name):
        self.settings.to_csv(screener_name+'.csv', sep = '\t')

    def check_value(self, value1, value2, compare):
        if compare == '1':
            return value1 < value2
        return value1 > value2

    def run_screener(self):
        stocks = []

        for ticker in self.tickers:
           s(ticker, '..\\stock\\historical_data\\', 'check_data')

        for ticker in self.tickers:
            stock = s(ticker, '..\\stock\\historical_data\\')

            if not np.isnan(self.settings[0]):
                if not self.check_value(stock.get_price(), float(str(self.settings[0])[:-1]), str(self.settings[0])[0]):
                    continue

            if not np.isnan(self.settings[1]):
                if not self.check_value(stock.get_volume(), float(str(self.settings[1])[:-1]), str(self.settings[1])[0]):
                    continue

            #RESUME WORK HERE, NEED TO ADD PERCENTS REGARDING VALUES, THEN WORK ON OTHER GUI SCREENER FEATURES
            if not np.isnan(self.settings[2]):
                if not self.check_value(stock.get_52week_high(), 2):
                    continue

            if not np.isnan(self.settings[3]):
                if not self.check_value(stock.get_52week_low(), 3):
                    continue

            if not np.isnan(self.settings[4]):
                if not self.check_value(stock.get_sma_20(), 4):
                    continue

            if not np.isnan(self.settings[5]):
                if not self.check_value(stock.get_sma_50(), 5):
                    continue

            if not np.isnan(self.settings[6]):
                if not self.check_value(stock.get_sma_200(), 6):
                    continue

            stocks.append(ticker)
            print(ticker)

        return stocks