import os
import sys
import random
import math
import RSAExample.prime_number as prime_number


def main():
    # create a public/private keypair with variable bit key
    bit_key = 16
    print('Making key files...')
    make_key_files('my', bit_key)
    print('Key files made.')


def generate_key(key_size):
    # Creates a public/private key pair with keys that are keySize bits in
    # size. This function may take a while to run.
    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.

    print('Generating p prime...')
    p = prime_number.generate_large_prime(key_size)
    print('Generating q prime...')
    q = prime_number.generate_large_prime(key_size)
    print('Multiplying q * p to get the modulus...')
    n = p * q

    # Step 2: Create a number e that is relatively prime (co-prime) to (p-1)*(q-1).
    print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        # Keep trying random numbers for e until one is valid.
        e = random.randrange(2 ** (key_size - 1), 2 ** key_size)
        if math.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Step 3: Calculate d, the mod inverse of e.
    print('Calculating d that is mod inverse of e...')
    d = find_mod_inverse(e, (p - 1) * (q - 1))

    public_key = (n, e)
    private_key = (n, d)
    print('Public key: modulus and e', public_key)
    print('Private key: modulus and d', private_key)

    return public_key, private_key


def make_key_files(name, key_size):
    # Creates two files 'x_pubkey.txt' and 'x_privkey.txt' (where x is the
    # value in name) with the the n,e and d,e integers written in them,
    # delimited by a comma.
    # Our safety check will prevent us from overwriting our old key files:

    if os.path.exists('{}_pubkey.txt'.format(name)) or os.path.exists('%s_privkey.txt' % name):
        sys.exit(
            'WARNING: The file {}_pubkey.txt or {}_privkey.txt already exists! Use a different name or delete these files and re-run this program.'.format(
                name, name))

    public_key, private_key = generate_key(key_size)
    print()
    print('The public key is a {} and a {} digit number.'.format(len(str(public_key[0])), len(str(public_key[1]))))
    print('Writing public key to file {}_pubkey.txt...'.format(name))
    fo = open('{}_pubkey.txt'.format(name), 'w')
    fo.write('{},{},{}'.format(key_size, public_key[0], public_key[1]))
    fo.close()
    print()
    print('The private key is a {} and a {} digit number.'.format(len(str(public_key[0])), len(str(public_key[1]))))
    print('Writing private key to file {}_privkey.txt...'.format(name))
    fo = open('{}_privkey.txt'.format(name), 'w')
    fo.write('{},{},{}'.format(key_size, private_key[0], private_key[1]))
    fo.close()


def find_mod_inverse(a, m):
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
