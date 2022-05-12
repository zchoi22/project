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
def normalize_data(data, filename='', save_scaler=False):
    scaler = preprocessing.MinMaxScaler()
    scaler.fit(data.reshape(-1,1))
    if save_scaler:
        filename = 'models\\scalers\\' + filename + "_scaler.gz"
        joblib.dump(scaler, filename)
    return scaler.transform(data.reshape(-1,1)).flatten()

#need to create batches for time steps, 20 time steps, 2 features
def generate_batches(data, timesteps=20):
    return np.array(np.split(data, timesteps))

def create_model(ticker = 'A', timesteps=20):
    features = 5
    timesteps = timesteps
    ticker = ticker

    x_data = np.array([[] for i in range(features)])
    y_data = np.array([])

    print("==== Retrieving Data =====")
    data = stock(ticker, '..\\..\\..\\project\\main\\stock\\historical_data\\', update=True)
    features_x = [data.get_sma(20)[19:].to_numpy(), data.get_data()['Open'][19:].to_numpy(),
                  data.get_data()['High'][19:].to_numpy(), data.get_standard_deviation(20)[19:],
                  data.get_relative_volume(20)[19:]]
    adj_closes = data.get_data()['Adj Close'][19:].to_numpy()

    #making sure we can batch the data later, reduces size of the data to %20
    data_size = adj_closes.shape[0] - (adj_closes.shape[0] % timesteps)
    adj_closes = adj_closes[:data_size]
    for i in range(features):
        features_x[i] = features_x[i][:data_size]

    x_data = np.concatenate((x_data, np.stack(features_x)), axis=1)
    y_data = np.concatenate((y_data, adj_closes))

    print("==== Normalizing Data ====")
    features_x = np.split(x_data.T, features, axis=1)
    for i in range(len(features_x)):
        features_x[i] = normalize_data(features_x[i], save_scaler=True, filename='x' + str(i))
    y_data = normalize_data(y_data, save_scaler=True, filename='y')
    x_data = np.vstack(features_x).T

    print('===== Reformatting Arrays ====')
    x_data, y_data = generate_batches(x_data, timesteps=timesteps), generate_batches(y_data, timesteps=timesteps)

    x_data = x_data.reshape((x_data.shape[1], x_data.shape[0], features))
    y_data = y_data.T

    print(x_data.shape, y_data.shape)

    print('==== Training and Testing=====')
    size = x_data.shape[0] - int(x_data.shape[0]/6)
    x_train, x_test = x_data[:size, :], x_data[size:, :]
    y_train, y_test = y_data[:size, :], y_data[size:, :]

    #timesteps, inputs so should be x, features
    print('==== Training Model ====')
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], features)))
    model.add(Dropout(0.6))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.6))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.6))
    model.add(LSTM(units=50))
    model.add(Dropout(0.6))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(units=1, activation='relu'))
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, batch_size=32, epochs=12, validation_data=(x_test, y_test))

    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test accuracy: ', score)

    print('==== Saving Model =====')
    model.save('models\\model.h5')