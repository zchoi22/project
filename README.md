# Rapstar
***
This project is a Zion Choi property, as licensed under Zion Choi Code Practices.
## Table of Contents
1. [General Info](#general-info)
2. [Usage](#Usage)
3. [Installation](#installation)
4. [Important Files](#Important-Files)
5. [Remaining Bugs/Further Development](#Bugs/Further_Development)

### General Info
The project relies on multiple dependencies outlined in requirements.txt. When using PyCharm, it is recommened that a VirtualEnv is used to create the virtual environemnt.

Currently there are two available main features: finance and screener. The finance feature allows users to behold the wonders of line graphs, presenting a YTD chart of adj. close prices given a ticker. Additionally, there is a support for more advanced graphs, with simple moving averages and other price-related data (opens, highs, lows, and closes). Further features have been added, though not yet connected to the main application. These include google trends data, standard deviations, and relative volumes.

The screener feature allows users to input custom features to a screener relating to the following: price, SMAs, 52 week lows, 52 week highs, etc. The application saves these screener settings to a local csv file, that can be accessed by importing the screeener. 

As of now, there is prediction software implemented using a keras-based neural network. Though the feature exists within the project, it has not yet been connected to the main application. There is a data visualization class to test and optimize the neural network, however, that visualizes prediction vs. actual data.

### Usage
The program is best run in PyCharm. It utilizes three main classes: the stock class, the screener class, and the main.py script for the UI/implementation.

### Installation
How to install:
1. Pull from GitHub to preferable file location.
2. Ideally using PyCharm, open the project and download the appropriate dependencies (referenced in the requirements.txt).
3. Open main.py, and run to start the UI.
4. If run/setup correctly, it should look like the following:

![better run]https://github.com/zchoi22/project/blob/master/start_up.JPG

### Important Files
Here are the following important files:

main.py: run this file for the UI. Edits made here will change the UI.

stock.py: stock class for project. Stock class imports data from Yahoo Finance and exports data to csv files under historical_data folder.

screener.py: screener class for project. Screener class can save screener inputs and imports/exports settings from/to csv files. The format of the screener settings are stored in a Pandas Series. The format of a given setting is as follows:

The first number is the compare value (a compare value of 1 returns a boolean value if the first value is less than the second value, any other value will returna boolean value if the first value is greater than the second value => for intensive purposes, this value is 2)
  The following numbers refer to the value to be compared. For simple moving averages this value will vary, as shown in the screener class (i.e. 0=price, 1=20SMA, 2=50SMA, 3=200SMA) 
  ex. 110 (checks if the given value is less than 10)
  
model.py: houses the neural network.

data_visualization.py: utilizes the model in model.py to visualize data. The data shown is prediction vs. actual prices, graphed by matplotlib.

Test Files: test files are stored under the programs folder, currently there are test files for stock.py and screener.py. Though these test files are not complete, most features are inherently tested within main.py

### Remaining Bugs/Further Development
There are some remaining bugs in the neural network. There are unknown bugs, but they are likely silent errors that may be in the normalization or batching processes of the pre-training part found in model.py.
If you were to collaborate with this project, here are future developments to consider:
1. Add more indicators to both the stock class and screener class. Look at stock.py and screener.py for implementation advice.
2. Add a Twitter sentiment analysis tool, similar to StockTwits.
3. Connect the new features to the main application. These include the prediction software and new features to the stock class outliend above in General Info.
4. Resolve silent errors in the neural network. One known error is in the batching process, where data loss is occuring.
