from main.stock.stock import stock

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
import numpy as np
import csv
from sklearn import preprocessing
from yahoo_fin.stock_info import tickers_sp500

#where input is a 1D np.array and returns a 1D np.array
def normalize_data(input):
    scaler = preprocessing.MinMaxScaler()
    return scaler.fit_transform(input.reshape(-1,1)).flatten()

#need to create batches for time steps, 20 time steps, 2 features
def generate_batches(x_data, y_data, *args):
    if args == ():
        while x_data.shape[0]%20 != 0:
            x_data = np.delete(x_data, -1, axis=0)
            y_data = np.delete(y_data, -1, axis=0)
        return np.array(np.vsplit(x_data, 20)), np.array(np.split(y_data, 20))
    else:
        while x_data.shape[0]%args[0] != 0:
            x_data = np.delete(x_data, -1, axis=0)
            y_data = np.delete(y_data, -1, axis=0)
        return np.vsplit(x_data, args[0]), np.split(y_data, args[0])


def main():
    tickers = tickers_sp500()

    x_train = np.array([[],[]])
    x_test = np.array([[],[]])
    y_train = np.array([])
    y_test = np.array([])

    print("==== Retrieving Data =====")
    seed = 0
    for ticker in tickers:
        b = stock(ticker)
        data = b.get_data()
        opens = normalize_data(data['Open'].to_numpy())
        highs = normalize_data(data['High'].to_numpy())
        adj_closes = normalize_data(data['Adj Close'].to_numpy())

        if seed%6 == 0:
            x_test = np.concatenate((x_test, np.stack([opens, highs])), axis=1)
            y_test = np.concatenate((y_test, adj_closes))
        else:
            x_train = np.concatenate((x_train, np.stack([opens, highs])), axis=1)
            y_train = np.concatenate((y_train, adj_closes))

        seed+=1

    x_train = x_train.T
    x_test = x_test.T

    print(x_train.shape, x_test.shape)
    print(y_train.shape, y_test.shape)

    print('===== Reformatting Arrays ====')
    x_test, y_test = generate_batches(x_test, y_test)
    x_train, y_train = generate_batches(x_train, y_train)

    x_test = x_test.reshape((x_test.shape[1], x_test.shape[0], 2))
    y_test = y_test.T

    x_train = x_train.reshape((x_train.shape[1], x_train.shape[0], 2))
    y_train = y_train.T

    print(x_train.shape, x_test.shape)
    print(y_train.shape, y_test.shape)

    #timesteps, inputs so should be x, 2
    print('==== Training Model ====')
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 2)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1, activation='relu'))
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, batch_size=32, epochs=10, validation_data=(x_test, y_test))

    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test accuracy: ', score)

    print('==== Saving Model =====')
    model_json = model.to_json()
    with open('..\\project\\program\\model.json', 'w') as json_file:
        json_file.write(model_json)
    model.save_weights('model.h5')


if __name__ == '__main__':
    main()