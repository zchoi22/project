# Rapstar
This project is a Zion Choi property, as licensed under Zion Choi Code Practices.

**Section I.** _Setup_
Rapstar, as licensed under Zion Choi Code Practices, requires a virtual environment to execute. If you are using PyCharm, please use a Virtualenv environment for library imports. If not, good luck, buddy. Please refer to the requirements.txt document for the required dependencies.

**Section II.** _Features and Purpose_
Rapstar is a comprehensive UI for stock data analysis. Currently there is are two available feature: there is a Finance feature and a Screener feature. The Finance feature allows users to behold the wonders of line graphs, presenting a YTD chart of adj. close prices given a ticker. Additionally, there is a support for more advanced graphs, with simple moving average, open prices, high & low prices, and close price options. The screener feature allows users to set a screener, import a screener, and run it.

**Section III.** _Files_
main.py: run this file for the UI. Edits made here will change the UI.

stock.py: stock class for project. Stock class imports data from Yahoo Finance and exports data to csv files under historical_data folder.

screener.py: screener class for project. Screener class can save screener inputs and imports/exports settings from/to csv files. The format of the screener settings are stored in a Pandas Series. The format of a given setting is as follows:

The first number is the compare value (a compare value of 1 returns a boolean value if the first value is less than the second value, any other value will returna boolean value if the first value is greater than the second value => for intensive purposes, this value is 2)
  The following numbers refer to the value to be compared. For simple moving averages this value will vary, as shown in the screener class (i.e. 0=price, 1=20SMA, 2=50SMA, 3=200SMA) 
  ex. 110 (checks if the given value is less than 10)

test files: test files are stored under the programs folder
