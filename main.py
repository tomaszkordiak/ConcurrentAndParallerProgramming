import time
from workers.SleepyWorkers import SleepyWorker
from workers.SquareSumWorkers import SquaredSumWorker


def main():
    calc_start_time = time.time()

    current_workers = []
    for i in range(5):
        maximum_value = (i+1) * 1000000
        squareSumWorker = SquaredSumWorker(maximum_value)
        current_workers.append(squareSumWorker)
        # calculate_sum_squares((i+1) * 1000000)

    for i in range(len(current_workers)):
        current_workers[i].join()

    print('Calculating sum of squares took:'
          , round(time.time() - calc_start_time, 1))

    sleep_start_time = time.time()
    current_workers = []
    for seconds in range(1, 6):
        sleepyWorker = SleepyWorker(seconds)
        current_workers.append(sleepyWorker)
        # sleep_a_little(i)

    print('Sleep took:'
          , round(time.time() - sleep_start_time, 1))

    for i in range(len(current_workers)):
        current_workers[i].join()


if __name__ == '__main__':
    main()

