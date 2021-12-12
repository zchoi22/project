from stock import stock
from screener import screener as sc

def test():
    screener = sc()
    screener.set_screener('hi', ['hi', 12, 13], ['hi2', 13, 14])
    print(screener.get_screener('hi'))
    print(screener.format_screener('hi'))

if __name__ == '__main__':
    test()
