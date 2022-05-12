from main.stock.stock import stock as s

test = s('AAPL', filepath = '..\\stock\\historical_data\\')
# data = test.get_sma(20)[18:]
# features_x = data.to_numpy()
# print(features_x.shape)
# features_x = features_x.squeeze()
# print(features_x.shape)

print(test.get_google_trends())
print(test.get_standard_deviation(20)[19:])
print(test.get_relative_volume(20)[19:])
