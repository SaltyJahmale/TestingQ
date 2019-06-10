import math
import random

def find_mod_inverse(a, m):
   # Returns the modular inverse of a % m, which is
   # the number x such that a*x % m = 1
   if math.gcd(a, m) != 1:
       return None  # no mod inverse if a & m aren't relatively prime

   # Calculate using the Extended Euclidean Algorithm:
   u1, u2, u3 = 1, 0, a
   v1, v2, v3 = 0, 1, m
   while v3 != 0:
       q = u3 // v3  # // is the integer division operator
       v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
   return u1 % m

if __name__ == '__main__':
    print('set p prime...')
    p = 13

    print('set q prime...')
    q = 17

    print('Multiplying q * p to get the modulus...')
    n = p * q

    # while True:
    #     print('Calculating e')
    #     e = random.randrange(1, 250)
    #     if math.gcd(e, (p - 1) * (q - 1)) == 1:
    #         print(e)
    #         break

    # E is public available
    print('E the public key is freely available...')
    e = 23

    print('Calculating d that is mod inverse of e...')
    d = find_mod_inverse(e, (p - 1) * (q - 1))

    print('Now D the private key is available ', d)
    print('RSA key is broken with these steps')
