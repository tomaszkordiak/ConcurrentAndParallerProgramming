import threading
import requests
from bs4 import BeautifulSoup
from lxml import html
import datetime, time
import random


# //*[@id="quote-header-info"]/div[3]/div[1]/div[1]/span[1]
# //*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]
# //*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]
# //*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]


class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self, input_queue,output_queue, **kwargs):
        super(YahooFinancePriceScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self._output_queue = output_queue
        self.start()

    def run(self) -> None:
        while True:
            val = self._input_queue.get()
            if val == 'DONE':
                if self._output_queue is not None:
                    self._output_queue.put('DONE')
                break
            yahooFinancePriceWorker = YahooFinancePriceWorker(symbol=val)
            price = yahooFinancePriceWorker.get_price()
            if self._output_queue is not None:
                output_values = (val, price, datetime.datetime.utcnow())
                self._output_queue.put(output_values)


class YahooFinancePriceWorker():
    def __init__(self, symbol, **kwargs):
        self._symbol = symbol
        base_url = 'https://finance.yahoo.com/quote/'
        self._url = f'{base_url}{self._symbol}'

    def get_price(self):
        time.sleep(20 * random.random())

        r = requests.get(self._url)
        if r.status_code != 200:
            return
        page_contents = html.fromstring(r.text)
        price = page_contents.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/span[1]')[0].text
        if price == 'None':
            price = page_contents.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')[0].text
        print(price)
        return price
