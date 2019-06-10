import timeit
import time

start = time.time()
setup = """from __main__ import prime_factors"""

def prime_factors(n):
    i = 2
    prime_factors_list = []
    while i <= n:
        if (n % i) == 0:
            prime_factors_list.append(i)
            n = n / i
        else:
            i = i + 1
    return prime_factors_list

if __name__ == '__main__':
    print(prime_factors(42459479))
    print(start)
    print(time.time())
    end = time.time() - start
    print(end)

    # times = timeit.Timer("prime_factors(15)", setup=setup)
    # print("Prime_factors ran:", times.timeit(number=100), "milliseconds")
    # 9.445400000002158e-05 milliseconds vs 1.9209999999603156e-06 milliseconds
    # print('Shor"s algo classic time: {}'.format(min(times)))
