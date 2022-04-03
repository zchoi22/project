from keras.models import load_model
from main.stock.stock import stock
import numpy as np
from main.neural_network.model import normalize_data
import joblib

model = load_model('models\\model.h5')
data = stock('AAPL', '..\\..\\..\\project\\main\\stock\\historical_data\\').get_data()
test_data = np.array([[], []])

opens = normalize_data(data['Open'][-21:-1].to_numpy())
highs = normalize_data(data['High'][-21:-1].to_numpy())
adj_closes = normalize_data(data['Adj Close'][-21:-1].to_numpy(), save_scaler=True)

test_data = np.concatenate((test_data, np.stack([opens, highs])), axis=1)
test_data = np.reshape(test_data.T, (1, 20, 2))
print(test_data.shape)

prediction = model.predict(test_data, verbose = 0)
scaler = joblib.load('scaler.gz')
print(adj_closes)
print(scaler.inverse_transform(adj_closes.reshape(-1,1)))
print(prediction)
print(scaler.inverse_transform(prediction))