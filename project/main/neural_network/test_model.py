#test driver for the model visualizer
#creates graph of the desried stock
from main.neural_network.model_visualizer import model_visualizer as mv

test = mv(ticker='ZM')
test.generate_graph()
