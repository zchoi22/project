#import dependencies
from main.stock.stock import stock
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
import numpy as np
from sklearn import preprocessing
import joblib

#normalizes data using MinMax scaler from sklearn
#has the option to store the scanner for outside access
def normalize_data(data, filename='', save_scaler=False):
    scaler = preprocessing.MinMaxScaler()
    scaler.fit(data.reshape(-1,1))
    if save_scaler:
        filename = 'models\\scalers\\' + filename + "_scaler.gz"
        joblib.dump(scaler, filename)
    return scaler.transform(data.reshape(-1,1)).flatten()

#need to create batches for time steps, 20 time steps, 2 features
#returns a split array with appropriate timesteps
def generate_batches(data, timesteps=20):
    return np.array(np.split(data, timesteps))

#main
def create_model(ticker = 'A', timesteps=20):
    #features is number of inputs
    features = 5
    timesteps = timesteps
    ticker = ticker

    #initial datasets
    x_data = np.array([[] for i in range(features)])
    y_data = np.array([])

    #data retrieval
    print("==== Retrieving Data =====")
    #creates stock object and updates the data
    data = stock(ticker, '..\\..\\..\\project\\main\\stock\\historical_data\\', update=True)
    #using stock class, gets historical data and turns the data into numpy arrays (from pd dataframes)
    features_x = [data.get_sma(20)[19:].to_numpy(), data.get_data()['Open'][19:].to_numpy(),
                  data.get_data()['High'][19:].to_numpy(), data.get_standard_deviation(20)[19:],
                  data.get_relative_volume(20)[19:]]
    #grabs the output data or price using the stock class
    adj_closes = data.get_data()['Adj Close'][19:].to_numpy()

    #making sure we can batch the data later, reduces size of the data to %20
    #checks to see the desired size (needs to be %timesteps=0) and cuts the dataset appropriately
    data_size = adj_closes.shape[0] - (adj_closes.shape[0] % timesteps)
    adj_closes = adj_closes[:data_size]
    for i in range(features):
        features_x[i] = features_x[i][:data_size]

    #after the datasets are cut down, they are concatenated to the initial datasets
    x_data = np.concatenate((x_data, np.stack(features_x)), axis=1)
    y_data = np.concatenate((y_data, adj_closes))

    #data normalization
    print("==== Normalizing Data ====")
    #splits the data in x_data along axis=1 so we can individually normalize the inputs
    features_x = np.split(x_data.T, features, axis=1)
    #for each input, using normalize_data function, min-maxes the data
    for i in range(len(features_x)):
        features_x[i] = normalize_data(features_x[i], save_scaler=True, filename='x' + str(i))
    #normalizing output data
    y_data = normalize_data(y_data, save_scaler=True, filename='y')
    #reconstructs the x_data with normalized inputs
    x_data = np.vstack(features_x).T

    #reformatting arrays
    print('===== Reformatting Arrays ====')
    #batches the data using above function
    x_data, y_data = generate_batches(x_data, timesteps=timesteps), generate_batches(y_data, timesteps=timesteps)

    #reshapes the input data for the neural network
    x_data = x_data.reshape((x_data.shape[1], x_data.shape[0], features))
    y_data = y_data.T

    print('==== Training and Testing=====')
    #splits the data into training and testing datasets
    #since this is an LSTM function, I tried to keep in order
    size = x_data.shape[0] - int(x_data.shape[0]/6)
    x_train, x_test = x_data[:size, :], x_data[size:, :]
    y_train, y_test = y_data[:size, :], y_data[size:, :]

    #timesteps, inputs so should be x, features
    #training model with relu activation and adam optimizer
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

    #fits the data to the training sets created above
    model.fit(x_train, y_train, batch_size=32, epochs=12, validation_data=(x_test, y_test))

    #evaluates the accuracy of the neural network
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test accuracy: ', score)

    #saves the model so predictions can be made outside
    print('==== Saving Model =====')
    model.save('models\\model.h5')