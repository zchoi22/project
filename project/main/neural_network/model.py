from main.stock.stock import stock

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
import numpy as np
from sklearn import preprocessing
from yahoo_fin.stock_info import tickers_sp500
import joblib

#where input is a 1D np.array and returns a 1D np.array
def normalize_data(data, timesteps=20, save_scaler=False):
    scaler = preprocessing.MaxAbsScaler()
    scaler.fit(data.reshape(-1,1))
    if save_scaler:
        joblib.dump(scaler, 'scaler.gz')
    while data.shape[0]%timesteps != 0:
        data = np.delete(data, -1, axis=0)
    return scaler.transform(data.reshape(-1,1)).flatten()

#need to create batches for time steps, 20 time steps, 2 features
def generate_batches(data, dimensions=1, split=True, timesteps=20):
    while data.shape[0]%timesteps != 0:
        data = np.delete(data, -1, axis=0)
    if dimensions==1 and split:
        return np.array(np.split(data, timesteps))
    elif dimensions==2 and split:
        return np.array(np.vsplit(data, timesteps))
    elif dimensions==1 and not split:
        return data

def main():
    tickers = tickers_sp500()
    features = 2

    x_data = np.array([[] for i in range(features)])
    y_data = np.array([])

    print("==== Retrieving Data =====")
    for ticker in tickers:
        data = stock(ticker, '..\\..\\..\\project\\main\\stock\\historical_data\\').get_data()
        opens = data['Open'].to_numpy()
        highs = data['High'].to_numpy()
        adj_closes = data['Adj Close'].to_numpy()

        x_data = np.concatenate((x_data, np.stack([opens, highs])), axis=1)
        y_data = np.concatenate((y_data, adj_closes))

    print(x_data.shape, y_data.shape)

    print("==== Normalizing Data ====")
    feature1, feature2 = np.split(x_data.T, 2, axis=1)
    feature1, feature2 = generate_batches(feature1, split=False), generate_batches(feature2, split=False)
    y_data = generate_batches(y_data, split=False)

    feature1, feature2 = normalize_data(feature1).tolist(), normalize_data(feature2).tolist()
    y_data = normalize_data(y_data).tolist()

    print('==== Training and Testing=====')
    x_train = np.array([[],[]])
    x_test = np.array([[],[]])
    y_train = np.array([])
    y_test = np.array([])

    for i in range(int(len(y_data)/20)):
        if i%6 != 0:
            x_train = np.concatenate((x_train, np.stack([np.array(feature1[i:i*20-1]), np.array(feature2[i:i*20-1])])), axis=1)
            y_train = np.concatenate((y_train, np.array(y_data[i:i*20-1])))
        else:
            x_test = np.concatenate((x_test, np.stack([np.array(feature1[i:i*20-1]), np.array(feature2[i:i*20-1])])), axis=1)
            y_test = np.concatenate((y_test, np.array(y_data[i:i*20-1])))


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
    model.add(Dropout(0.1))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.1))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.1))
    model.add(LSTM(units=50))
    model.add(Dropout(0.1))
    model.add(Dense(units=1, activation='relu'))
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, batch_size=32, epochs=6, validation_data=(x_test, y_test))

    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test accuracy: ', score)

    print('==== Saving Model =====')
    model.save('models\\model.h5')


if __name__ == '__main__':
    main()