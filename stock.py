from yahoo_fin.stock_info import get_data, get_live_price, get_stats
from pandas import DataFrame

class stock:

    #inputs = ticker, uses ticker to grab stats
    def __init__(self, ticker):
        self.ticker = ticker
        self.stats = get_stats(ticker)

    #grabs financial data from yahoo finance, pd dataframe with
    #open, close, high, low, and adjclose
    def get_data(self, type):
        return get_data(self.ticker)[type].to_list()

    #returns ticker
    def get_ticker(self):
        return self.ticker

    #return volume
    def get_volume(self):
        return self.get_data('volume')[-1]

    #sets ticker
    def set_ticker(self, ticker):
        self.ticker = ticker

    #gets current price
    def get_live_price(self):
        return get_live_price(self.ticker)

    #gets 52_week_change
    def get_52_week_change(self):
        return self.stats['Value'][1]

    #returns SMA for num_days days
    def get_moving_averages(self, num_days):
        close_prices = self.get_data('close')[(-1*num_days):]
        return sum(close_prices)/num_days

    #returns average volume
    def get_average_volume(self, num_days):
        volumes = self.get_data('volume')[(-1*num_days):]
        return sum(volumes)/num_days

    #returns float
    def get_float(self):
        return self.stats['Value'][11]

    #shares shorted, short ratio, short % of float, short % of shares outstanding
    def get_shares_shorted(self):
        return self.stats['Value'][14], self.stats['Value'][15], self.stats['Value'][16], self.stats['Value'][17]

    #returns return on equity
    def get_return_on_equity(self):
        return self.stats['Value'][34]

    #returns price to book ratio, back value per share / price
    def get_pb(self):
        return self.stats['Value'][48]/self.get_live_price()

    def get_shares_outstanding(self):
        shares_outstanding = self.stats['Value'][9]
        if 'B' in shares_outstanding:
            shares_outstanding = float(shares_outstanding.strip('B')) * 10**9
        elif 'M' in shares_outstanding:
            shares_outstanding = float(shares_outstanding.strip('M')) * 10**6
        return int(shares_outstanding)

    def get_market_cap(self):
        return self.get_shares_outstanding()*self.get_live_price()

    def get_relative_volume(self, num_days):
        return self.get_volume()/self.get_average_volume(num_days)

    