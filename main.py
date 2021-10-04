import time
from workers.WikiWorker import WikiWorker
from workers.YahooFinanceWorkers import YahooFinancePriceWorker, YahooFinancePriceScheduler
from multiprocessing import Queue
from workers.SqliteWorker import SqliteMasterScheduler


def main():
    symbol_queue = Queue()
    sqlite_queue = Queue()
    scraper_start_time = time.time()

    wikiWorker = WikiWorker()
    yahoo_finance_price_scheduler_threads = []
    for i in range(15):
        yahooFinancePriceScheduler = YahooFinancePriceScheduler(input_queue=symbol_queue, output_queue=sqlite_queue)
        yahoo_finance_price_scheduler_threads.append(yahooFinancePriceScheduler)



    sqlite_scheduler_threads = []
    sqlite_workers = 8

    for i in range(sqlite_workers):
        sqliteScheduler = SqliteMasterScheduler(input_queue=sqlite_queue)
        sqlite_scheduler_threads.append(sqliteScheduler)

    for symbol in wikiWorker.get_sp_500_companies():
        symbol_queue.put(symbol)

    for i in range(len(yahoo_finance_price_scheduler_threads)):
        symbol_queue.put('DONE')

    for i in range(len(yahoo_finance_price_scheduler_threads)):
        yahoo_finance_price_scheduler_threads[i].join()

    print('Extracting time took:', round(time.time() - scraper_start_time, 1))


if __name__ == '__main__':
    main()

