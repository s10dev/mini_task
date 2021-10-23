import requests
import time


class PriceException(Exception):
    def __init__(self, obj):
        self.obj = obj
        super().__init__()


class Binance:
    def __init__(self, ticker):
        self.api_request = f'https://api.binance.com/api/v3/trades?symbol={ticker}&limit=1'

    def get_price(self):
        '''Parse price from API response'''
        response = requests.get(self.api_request)
        try:
            result = response.json()[0]['price']
        except IndexError:
            return -1
        return int(float(result))

    def __sub__(self, other):
        self_price, other_price = self.get_price(), other.get_price()
        if self_price == -1:
            raise PriceException(self)
        elif other_price == -1:
            raise PriceException(other)
        else:
            return abs(self_price - other_price)


class Ftx(Binance):
    def __init__(self, ticker):
        self.api_request = f'https://ftx.com/api/markets/{ticker}/trades?limit=1'

    def get_price(self):
        '''Parse price from API response'''
        response = requests.get(self.api_request)
        try:
            result = response.json()['result'][0]['price']
        except IndexError:
            return -1
        return int(result)


# Setup
data = {}
with open('setup.txt', 'r') as f:
    for line in f:
        temp = line.split('=')
        data[temp[0]] = temp[1].rstrip()     

binance = Binance(data['binance_ticker'])
ftx = Ftx(data['ftx_ticker'])

# main loop
while True:
    try:
        result = abs(binance - ftx)
        if result >= int(data['size']):
            print(f'Do smth to make profit, cuz difference is bigger than {data["size"]}')
        print(result)
    except PriceException as e:
        print(f'Unable to get price from {e.obj.__class__.__name__}')
    except KeyError as e:
        print(f'Bad API response. The ticker name is probably incorrect')
    time.sleep(0.25)
