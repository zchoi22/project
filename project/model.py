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

    print("==== Retrieving Data =====")
    for ticker in tickers:
        b = stock(ticker)
        data = b.get_data()
        for i in range(len(data)):
            x_data.append(data['Open'])
            y_data.append(data['Adj Close'])

    print(x_data[:10], y_data[:10])

    x_data = scaler.fit_transform(np.array(x_data))
    y_data = scaler.fit_transform(np.array(y_data).reshape(-1,1).flatten())

    print('===== Creating Training/Testing Sets ====')
    x_train = []
    x_test = []
    y_train = []
    y_test = []

    for i in range(len(x_data)):
        if i&6:
            x_train.append(x_data[i])
            y_train.append(y_data[i])
        else:
            x_test.append(x_data[i])
            y_test.append(y_data[i])

    print('==== Normalizing Data ====')
    x_test = np.array(x_test)
    y_test = np.array(y_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    x_train = np.array(x_train)
    y_train(np.array(y_train))
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    print('==== Training Model ====')
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(6, 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1, activation='relu'))
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, batch_size=32, epochs=1, validation_data=(x_test, y_test))

    score = model.evaluate(x_test, y_test, verbose='VERBOSE')
    print('Test accuracy: ', score)

    print('==== Saving Model =====')
    model_json = model.to_json()
    with open('..\\program\\model.json', 'w') as json_file:
        json_file.write(model.json)
    model.save_weights('model.h5')


if __name__ == '__main__':
    main()