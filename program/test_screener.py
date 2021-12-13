from main.screener.screener import screener as sc
import os

test = sc(False)
test.import_screener('..\\main\\screener\\screeners\\reversal')
print(test.get_settings())
test.run_screener()