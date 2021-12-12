from stock import stock
import csv

class screener:

    def __int__(self, **screener):
        screeners = {'market_cap':[None, None], 'average_volume':[None, None], 'relative_volume':[None, None],
                            'price': [None, None], '20-SMA': [None, None]}
        for key, value in screener.items():
            screeners[key] = value

    def get_screener(self, screener_name):
        with open('settings.csv', 'r', newline = '') as csvfile:
            reader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
            for row in reader:
                if row[0] == screener_name:
                    return row
            return False

    def set_screener(self, screener_name, *settings):
        with open('settings.csv', 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([screener_name, [setting for setting in settings]])

    def format_screener(self, screener_name):
        active = self.get_screener(screener_name)
        if active == False:
            return active
        screener = {}
        settings = list(active[1].split(']'))
        print(settings)
        for setting in active[1]:
            screener[setting[0]] = [setting[0:]]
        return screener

    def search_market_cap(self, ):
        print(2)

    def run_screener(self):
        print(2)
