import threading


class SquaredSumWorker(threading.Thread):
    def __init__(self, n, **kwargs):
        self.n = n
        super(SquaredSumWorker, self).__init__(**kwargs)
        self.start()

    def _calculate_sum_squares(self):
        sum_squares = 0
        for i in range(self.n):
            sum_squares += i ** 2

        print(sum_squares)

    def run(self) -> None:
        self._calculate_sum_squares()