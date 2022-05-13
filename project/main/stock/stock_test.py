#test driver for stock class

#import the stock class as s
from main.stock.stock import stock as s

#create a stock object
test = s('AAPL', filepath = '..\\stock\\historical_data\\')
# data = test.get_sma(20)[18:]
# features_x = data.to_numpy()
# print(features_x.shape)
# features_x = features_x.squeeze()
# print(features_x.shape)

#testing new features, google trends,
#standard deviation and relative volume
print(test.get_google_trends())
print(test.get_standard_deviation(20)[19:])
print(test.get_relative_volume(20)[19:])
