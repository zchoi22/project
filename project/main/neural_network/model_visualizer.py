import matplotlib.pyplot as plt
from main.stock.stock import stock as s
from main.neural_network.model import create_model
import numpy as np
import joblib
from keras.models import load_model

class model_visualizer:
    def __init__(self, ticker = 'A', timesteps=20):
        create_model(ticker=ticker, timesteps=timesteps)
        self.timesteps = timesteps
        self.data = s(ticker, filepath='..\\..\\..\\project\\main\\stock\\historical_data\\')

    def retrieve_adj_closes(self):
        return self.data.get_data()['Adj Close'][19:]

    def retrieve_features(self):
        output = np.array([[], [], [], [], []])
        features = []

        features.append(self.data.get_sma(20)[19:].to_numpy())
        features.append(self.data.get_data()['Open'][19:].to_numpy())
        features.append(self.data.get_data()['High'][19:].to_numpy())
        features.append(self.data.get_standard_deviation(20)[19:].to_numpy())
        features.append(self.data.get_relative_volume(20)[19:].to_numpy())

        for i in range(len(features)):
            scaler = joblib.load('models\\scalers\\x' + str(i) + '_scaler.gz')
            features[i] = scaler.transform(features[i].reshape(-1,1)).flatten()

        while features[0].shape[0] % self.timesteps != 0:
            for i in range(len(features)):
                features[i] = np.delete(features[i], -1)

        output = np.concatenate((output, np.stack(features)), axis=1).T
        return output

    def retrieve_predictions(self):
        print("==== Loading Predictions ====")
        predictions = []
        features =  self.retrieve_features()

        model = load_model('models\\model.h5')
        scaler = joblib.load('models\\scalers\\y_scaler.gz')

        for i in range(features.shape[0]-self.timesteps):
            prediction = np.reshape(features[i:i+self.timesteps], (1,20,5))
            prediction = model.predict(prediction, verbose = 0)
            predictions.append(scaler.inverse_transform(prediction))
        return [prediction[0] for prediction in predictions]

    def generate_graph(self):
        predictions = self.retrieve_predictions()
        actual = self.retrieve_adj_closes()
        plt.plot([i for i in range(len(predictions))], predictions, label = 'predictions')
        plt.plot([i for i in range(len(actual))], actual, label = 'actual')
        plt.legend()
        plt.show()