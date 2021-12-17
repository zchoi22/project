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
Rapstar, as licensed under Zion Choi Code Practices, requires a virtual environment to execute. If you are using PyCharm, please use a Virtualenv environment for library imports. If not, good luck, buddy. Please refer to the requirements.txt document for the required dependencies.

Rapstar is a comprehensive UI for stock data analysis. Currently there are two available main features: finance and screener. The finance feature allows users to behold the wonders of line graphs, presenting a YTD chart of adj. close prices given a ticker. Additionally, there is a support for more advanced graphs, with simple moving averages and other price-related data (opens, highs, lows, and closes).

The screener feature allows users to input custom features to a screener relating to the following: price, SMAs, 52 week lows, 52 week highs, etc. The application saves these screener settings to a local csv file, that can be accessed by importing the screeener. 

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

Test Files: test files are stored under the programs folder, currently there are test files for stock.py and screener.py. Though these test files are not complete, most features are inherently tested within main.py

### Remaining Bugs/Further Development
Currently there are no known bugs.
If you were to collaborate with this project, here are future developments to consider:
1. Create a neural network model (with keras or theanos) to provide users a predicting tool for stocks.
2. Add more indicators to both the stock class and screener class. Look at stock.py and screener.py for implementation advice.
3. Add a Twitter sentiment analysis tool, similar to StockTwits.
