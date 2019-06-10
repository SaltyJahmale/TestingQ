import timeit
from matplotlib import pyplot
# import numpy as np
from random import randint
from math import gcd
import time

setup = """
from random import randint
from math import gcd
from __main__ import find_period_classical
 """
start = time.time()

def find_period_classical(a, N):
    n = 1
    t = a
    while t != 1:
        t *= a
        t %= N
        n += 1
    return n


def shors_algorithm_classical(N):
    x = randint(0, N) # step one, pick a number bigger 1 smaller N

    if gcd(x, N) != 1:  # If the gcd(m, N) = 1, continue.
        return x, 0, gcd(x, N), N / int(gcd(x, N)) # If you find a factor using gcd, you’ve found a non-trivial factor and are done.

    periode = find_period_classical(x, N)  # step two find the period (Classical bottleneck)
    while periode % 2 != 0 and x ** periode / 2 + 1 % 2 != 0:  # step three and four check if it's an even number otherwise pick another number and check if m ** p/2 != 0 mod N
        periode = find_period_classical(x, N)

    factor_p = gcd(x ** int(periode / 2) + 1, N)  # step five compute the factor
    factor_q = gcd(x ** int(periode / 2) - 1, N)  # step five compute the factor

    return factor_p, factor_q


if __name__ == '__main__':
    print(shors_algorithm_classical(42459479))
    print(time.time() - start)
    # x = ['1','2','3', ]
    # y = ['1','4','9', ]
    #
    # pyplot.plot(x, y)
    # pyplot.show()

    # times = timeit.Timer("find_period_classical", setup=setup)
    # print("Shors_algorithm_classical ran:", times.timeit(number=100), "milliseconds")
    # 2.2091999999973577e-05

    # print('Shor"s algo classic time: {}'.format(min(times)))

    # times = timeit.timeit(setup=setup, stmt=code, number=10000)
    # print(times)
    # print('Shor"s algo classic time: {}'.format(min(times)))
