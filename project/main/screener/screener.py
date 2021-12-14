from project.main.stock.stock import stock as s
import pandas as pd
import numpy as np
from yahoo_fin.stock_info import tickers_sp500

#screener class, refer to README.md for further details
class screener:

    #initialize with settings (empty), a request for update (boolean), and an optional filename
    def __init__(self, update, *args):
        self.settings = pd.Series([np.nan for i in range(7)])
        self.format = {'price': 0, 'volume': 1, '52_week_high': 2, '52_week_low': 3,
                       'moving_average_20': 4, 'moving_average_50' : 5, 'moving_average_200': 6,}
        tickers = tickers_sp500()
        self.tickers = [item.replace(".", "-") for item in tickers]
        self.update = update
        if args!=():
            self.filename = args[0]+'.csv'
            self.import_screener(self.filename)

    #getter for settings
    def get_settings(self):
        return self.settings

    #getter for format => refers to the dictionary for setting options
    def get_format(self):
        return self.format

    #imports screener from screeener_name.csv, reads in as pd series
    def import_screener(self, screener_name):
        self.settings = pd.read_csv(screener_name, header=None,squeeze=True)

    #sets a specific setting
    def set_settings(self, setting, value):
        if type(setting) is int:
            self.settings[setting] = value
        elif type(setting) is str:
            self.settings[self.format[setting]] = value

    #saves given settings to screener_name.csv
    def save_screener(self, screener_name):
        self.settings.to_csv(screener_name+'.csv', header=None, index=False)

    #checks the compare value, and uses it to compare the two values
    #a compare value of 1 checks if value1 is less than value2, anything
    #else checks the opposite. Refer to README.md for further details.
    def check_value(self, value1, value2, compare):
        if compare == '1':
            return value1 < value2
        return value1 > value2

    #gets the values to compare for smas, 0=price, 1=20SMA, 2=50SMA, 3=200SMA
    #refers to simple moving averages, please refer to README.md for further detail
    def sma_setting_to_value(self, setting, stock):
        values = list(setting)
        for i in range(len(values)):
            if values[i] == '0':
                values[i] = stock.get_price()
            elif values[i] == '1':
                values[i] = stock.get_sma_20()
            elif values[i] == '2':
                values[i] = stock.get_sma_50()
            elif values[i] == '3':
                values[i] = stock.get_sma_200()
        return values[0], values[1]

    #runs the screener, stores appropriate tickers into stocks list, and prints them
    def run_screener(self):
        stocks = []

        #if an update was requested when initialized, updates each stock in the S&P 500
        if self.update:
            for ticker in self.tickers:
               s(ticker, 'update_data')

        #for each ticker, checks the screener settings and uses compare values to check if
        #a specified stock matches the requirements
        for ticker in self.tickers:
            stock = s(ticker)

            if not np.isnan(self.settings[0]):
                temp_val1, temp_val2 = stock.get_price(), float(str(self.settings[0])[1:])
                if not self.check_value(temp_val1, temp_val2, str(self.settings[0])[0]):
                    continue

            if not np.isnan(self.settings[1]):
                temp_val1, temp_val2 = stock.get_volume(), float(str(self.settings[1])[1:])
                if not self.check_value(temp_val1, temp_val2, str(self.settings[1])[0]):
                    continue

            if not np.isnan(self.settings[2]):
                temp_val1, temp_val2 = stock.get_price(), stock.get_52week_high()*(100-float(str(self.settings[2])[1:]))/100
                if not self.check_value(temp_val1, temp_val2, str(self.settings[2])[0]):
                    continue

            if not np.isnan(self.settings[3]):
                temp_val1, temp_val2 = stock.get_price(), stock.get_52week_low()*(100+float(str(self.settings[3])[1:]))/100
                if not self.check_value(temp_val1, temp_val2, str(self.settings[3])[0]):
                    continue

            if not np.isnan(self.settings[4]):
                temp_val1, temp_val2 = self.sma_setting_to_value(str(self.settings[4])[1:], stock)
                if not self.check_value(temp_val1, temp_val2, str(self.settings[4])[0]):
                    continue

            if not np.isnan(self.settings[5]):
                temp_val1, temp_val2 = self.sma_setting_to_value(str(self.settings[5])[1:], stock)
                if not self.check_value(temp_val1, temp_val2, str(self.settings[5])[0]):
                    continue

            if not np.isnan(self.settings[6]):
                temp_val1, temp_val2 = self.sma_setting_to_value(str(self.settings[6])[1:], stock)
                if not self.check_value(temp_val1, temp_val2, str(self.settings[6])[0]):
                    continue

            stocks.append(ticker)
            print(ticker)

        #returns list of stocks, though useless now, can provide foundation for further UI
        #implementation
        return stocks