from main.stock.stock import stock

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
import numpy as np
import csv
from sklearn import preprocessing
from yahoo_fin.stock_info import tickers_sp500

def main():
    tickers = tickers_sp500()

    x_data = []
    y_data = []
    scaler = preprocessing.StandardScaler()

    for ticker in tickers:
        b = stock(ticker)
        data = b.get_data()
        company_x_data = []
        company_y_data = []
        for i in range(len(data)):
            company_x_data.append(data['Open'])
            company_y_data.append(data['Adj Close'])

    x_train = []
    x_test = []
    y_train = []
    y_test = []

if __name__ == '__main__':
    main()