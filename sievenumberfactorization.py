import math as m

# find prime factorization of a number n in O(Log n) time
max_N = 100000000

# every number until max_N
# stores smallest prime factor for every number
list_spf = [0 for i in range(max_N)]


# Calculating SPF (Smallest Prime Factor) till max_N. The Time Complexity : O(n log log n).
def sieve():
    list_spf[1] = 1
    for number in range(2, max_N):

        # Array begint bij 2 deze wordt tot de grote van N
        # Array met grootte van 2 t/m N
        # marking smallest prime factor
        # for every number to be itself.
        list_spf[number] = number
        # print("list - 1", list_spf)

    # delers door 2 worden vervangen door het nummer 2, omdat deze altijd 2 zijn.
    # separately marking spf for every even number as 2
    for number in range(4, max_N, 2):
        list_spf[number] = 2
        # print("list even numbers", list_spf)

    for number in range(3, m.ceil(m.sqrt(max_N))):

        # checking if prime is a prime number
        if list_spf[number] == number:

            # marking SPF for all numbers divisible by prime
            for j in range(number * number, max_N, number):

                # mark list_spf[j] if it is not previously marked
                if list_spf[j] == j:
                    list_spf[j] = number



# A O(log n) function returning prime
# factorization by dividing by smallest
# Krijg de andere factor door het te delen met de kleinste spf
def get_factorization(factoring_number):
    prime_numbers = list()
    while factoring_number != 1:
        prime_numbers.append(list_spf[factoring_number])
        factoring_number = factoring_number // list_spf[factoring_number]

    return prime_numbers


# pre-calculating Smallest Prime Factor
sieve()
N = 42459479
print("prime factorization for", N, " are : ")

# Calling the function
list_of_prime_numbers = get_factorization(N)

#
for i in range(len(list_of_prime_numbers)):
    print(list_of_prime_numbers[i], end=" ")

# Pseudo Code
"""
PrimeFactors[] // A list to store the result

i = 0  // Index in PrimeFactors

while n != 1 :

    // SPF : smallest prime factor
    PrimeFactors[i] = SPF[n]    
    i++ 
    n = n / SPF[n]
"""
