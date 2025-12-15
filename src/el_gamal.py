import random
import numpy as np  

PRIME_NUMBER = 7919 # fixed prime number
GENERATOR = 2

class ElGamalPublicKey:
    def __init__(self, p, g, h):
        self.p = p  # prime modulus
        self.g = g  # generator
        self.h = h  # g^(secret exponent) mod p


class ElGamalPrivateKey:
    def __init__(self, p, g, x):
        self.p = p  # prime modulus
        self.g = g  # generator
        self.x = x  # secret exponent

# The function generates private and public keys
def generate_elgamal_keypair():
    p = PRIME_NUMBER        
    g = GENERATOR            
    x = random.randrange(1, p - 1)
    h = pow(g, x, p)
    pk = ElGamalPublicKey(p, g, h)
    sk = ElGamalPrivateKey(p, g, x)
    return pk, sk

# The function encrypts an integer message m using public key pk
def elgamal_encrypt(pk, m):
    p = pk.p
    if not (1 <= m <= p - 2):
        raise ValueError(f"Message {m} out of range [1, {p-2}]")

    y = random.randrange(1, p - 1)
    c1 = pow(pk.g, y, p)
    s = pow(pk.h, y, p)
    c2 = (m * s) % p
    return (c1, c2)

# The function decripts ciphertext (c1, c2) using private key sk
def elgamal_decrypt(sk, ciphertext):
    c1, c2 = ciphertext
    p = sk.p   
    s = pow(c1, sk.x, p) # shared secret
    s_inv = pow(s, p - 2, p)
    m = (c2 * s_inv) % p
    return m


# The function performs Homomorphic 
# multiplication of ciphertexts as follows:
# if cA encrypts mA and cB encrypts mB under the same public key pk
# then return a ciphertext encrypting (mA * mB mod p)
def elgamal_multiply_ciphertexts(pk, cA, cB):  
    p = pk.p
    c1A, c2A = cA
    c1B, c2B = cB
    c1 = (c1A * c1B) % p
    c2 = (c2A * c2B) % p
    return (c1, c2)


