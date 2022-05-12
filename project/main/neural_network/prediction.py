from keras.models import load_model
from main.stock.stock import stock
import numpy as np
import joblib

model = load_model('models\\model.h5')
data = stock('A', '..\\..\\..\\project\\main\\stock\\historical_data\\')
test_data = np.array([[], [], []])

scaler1 = joblib.load('models\\scalers\\y_scaler.gz')
scaler2 = joblib.load('models\\scalers\\x0_scaler.gz')
scaler3 = joblib.load('models\\scalers\\x1_scaler.gz')
scaler4 = joblib.load('models\\scalers\\x2_scaler.gz')

opens = scaler2.transform((data.get_data()['Open'][-100:-80].to_numpy()).reshape(-1,1)).flatten()
highs = scaler3.transform((data.get_data()['High'][-100:-80].to_numpy()).reshape(-1,1)).flatten()
smas = scaler4.transform((data.get_sma(20)[-100:-80].to_numpy()).reshape(-1,1)).flatten()
adj_closes = data.get_data()['Adj Close'][-99:-79].to_numpy()
ac = scaler1.transform((adj_closes).reshape(-1,1)).flatten()

print(opens.shape, highs.shape, smas.shape)

print(np.stack([opens, highs, smas]).shape)
test_data = np.concatenate((test_data, np.stack([opens, highs, smas])), axis=1).T
test_data = np.array(np.split(test_data, 20))
test_data = np.reshape(test_data.T, (1, 20, 3))

print(test_data.shape)

prediction = model.predict(test_data, verbose = 0)


#print(scaler1.inverse_transform(adj_closes.reshape(-1,1)))
print(ac)
print(prediction)
print(adj_closes)
print(scaler1.inverse_transform(prediction))