import os
import sys
import random
import math
import RSAExample.prime_number as prime_number


def main():
    # create a public/private keypair with variable bit key
    bit_key = 16
    print('Making key files...')
    makeKeyFiles('my', bit_key)
    print('Key files made.')


def generateKey(keySize):
    # Creates a public/private key pair with keys that are keySize bits in
    # size. This function may take a while to run.
    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.

    print('Generating p prime...')
    p = prime_number.generateLargePrime(keySize)
    print('Generating q prime...')
    q = prime_number.generateLargePrime(keySize)
    print('Multiplying q * p to get the modulus...')
    n = p * q

    # Step 2: Create a number e that is relatively prime (co-prime) to (p-1)*(q-1).
    print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        # Keep trying random numbers for e until one is valid.
        e = random.randrange(2 ** (keySize - 1), 2 ** keySize)
        if math.gcd(e, (p - 1) * (q - 1)) == 1:

            break

    # Step 3: Calculate d, the mod inverse of e.
    print('Calculating d that is mod inverse of e...')
    d = findModInverse(e, (p - 1) * (q - 1))

    publicKey = (n, e)
    privateKey = (n, d)
    print('Public key: modulus and e', publicKey)
    print('Private key: modulus and d', privateKey)

    return publicKey, privateKey


def makeKeyFiles(name, keySize):
    # Creates two files 'x_pubkey.txt' and 'x_privkey.txt' (where x is the
    # value in name) with the the n,e and d,e integers written in them,
    # delimited by a comma.
    # Our safety check will prevent us from overwriting our old key files:

    if os.path.exists('%s_pubkey.txt' % name) or os.path.exists('%s_privkey.txt' % name):
        sys.exit('WARNING: The file %s_pubkey.txt or %s_privkey.txt already exists! Use a different name or delete these files and re-run this program.' % (name, name))

    publicKey, privateKey = generateKey(keySize)
    print()
    print('The public key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Writing public key to file %s_pubkey.txt...' % name)
    fo = open('%s_pubkey.txt' % name, 'w')
    fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
    fo.close()
    print()
    print('The private key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Writing private key to file %s_privkey.txt...' % name)
    fo = open('%s_privkey.txt' % name, 'w')
    fo.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
    fo.close()


def findModInverse(a, m):
    # Returns the modular inverse of a % m, which is
    # the number x such that a*x % m = 1
    if math.gcd(a, m) != 1:
        return None # no mod inverse if a & m aren't relatively prime

    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


# If makeRsaKeys.py is run (instead of imported as a module) call
# the main() function.


if __name__ == '__main__':
    main()
