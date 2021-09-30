import threading
from sqlalchemy import create_engine
import database
from sqlalchemy.sql import text


class SqliteMasterScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        super(SqliteMasterScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    def run(self):
        while True:
            val = self._input_queue.get()
            if val == 'DONE':
                break
            symbol, price, extracted_time = val
            sqliteWorker = SqliteWorker(symbol, price, extracted_time)
            sqliteWorker.insert_into_db()


class SqliteWorker():
    def __init__(self, symbol, price, extracted_time):
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time
        self._engine = create_engine(f'sqlite:///pythonsqlite.db')

    def _create_insert_query(self):
        SQL = f"""INSERT INTO prices (symbol, price, extracted_time)
         VALUES (:symbol, :price, :extracted_time)"""
        return SQL

    def insert_into_db(self):
        insert_query = self._create_insert_query()

        with self._engine.connect() as conn:
            conn.execute(text(insert_query), {'symbol': self._symbol,
                                              'price': self._price,
                                              'extracted_time': self._extracted_time})
