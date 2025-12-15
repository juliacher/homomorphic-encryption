
import random
import el_gamal

def simple_encrypt_decrypt(pk, sk):
    m = 5 # original message
    c = el_gamal.elgamal_encrypt(pk, m)
    d = el_gamal.elgamal_decrypt(sk, c)
    assert d == m, "Test failed: simple_encrypt_decrypt"

def boundary_msg_low(pk, sk):
    m = 1
    c = el_gamal.elgamal_encrypt(pk, m)
    d = el_gamal.elgamal_decrypt(sk, c)
    assert d == m, "Test failed: boundary_msg_low: message = 1\nValid message range is 1 ≤ m ≤ p-2"

def boundary_msg_high(pk, sk):
    p = pk.p
    m = p - 2
    c = el_gamal.elgamal_encrypt(pk, m)
    d = el_gamal.elgamal_decrypt(sk, c)
    assert d == m, "Test failed: boundary_msg_high: message = p-2\nValid message range is 1 ≤ m ≤ p-2"

def several_random_calls(pk, sk):
    p = pk.p
    for i in range(5):
        m = random.randrange(1, p - 1)
        c = el_gamal.elgamal_encrypt(pk, m)
        d = el_gamal.elgamal_decrypt(sk, c)
        assert d == m, f"Test failed: several_random_calls: test number {i+1}"

def homomorphic_mult(pk, sk):
    p = pk.p
    m1 = 10
    m2 = 20
    c1 = el_gamal.elgamal_encrypt(pk, m1)
    c2 = el_gamal.elgamal_encrypt(pk, m2)
    c_prod = el_gamal.elgamal_multiply_ciphertexts(pk, c1, c2)
    d_prod = el_gamal.elgamal_decrypt(sk, c_prod)
    assert d_prod == (m1 * m2) % p, "Test failed: homomorphic_mult"

def encrypt_twice(pk):
    # same message encrypted twice should give different ciphertexts
    m = 42
    c1 = el_gamal.elgamal_encrypt(pk, m)
    c2 = el_gamal.elgamal_encrypt(pk, m)
    assert c1 != c2, "Test failed: encrypt_twice: Deterministic encryption!"

def commutativity(pk):
    m1 = 10
    m2 = 20
    c1 = el_gamal.elgamal_encrypt(pk, m1)
    c2 = el_gamal.elgamal_encrypt(pk, m2)
    mult_c1_c2 = el_gamal.elgamal_multiply_ciphertexts(pk, c1, c2)
    mult_c2_c1 = el_gamal.elgamal_multiply_ciphertexts(pk, c2, c1)
    assert mult_c1_c2 == mult_c2_c1, "Test failed: commutativity: ciphertext multiplication not commutative"

def invalid_msg_low(pk):
    try:
        el_gamal.elgamal_encrypt(pk, 0)
        raise AssertionError("Test failed: invalid_msg_low: encrypting 0 did not raise ValueError")
    except ValueError:
        return True

def invalid_msg_high(pk):
    p = pk.p
    try:
        el_gamal.elgamal_encrypt(pk, p - 1)
        raise AssertionError("Test failed: invalid_msg_high: encrypting p-1 did not raise ValueError")
    except ValueError:
        return True
  
def homomorphism_consistency(pk, sk):
    # Check that decrypt product of ciphertexts equal to product of decrypted messages
    m1 = 10
    m2 = 20
    p = pk.p

    c1 = el_gamal.elgamal_encrypt(pk, m1)
    c2 = el_gamal.elgamal_encrypt(pk, m2)

    dec1 = el_gamal.elgamal_decrypt(sk, c1)
    dec2 = el_gamal.elgamal_decrypt(sk, c2)

    c_prod = el_gamal.elgamal_multiply_ciphertexts(pk, c1, c2)
    d_prod = el_gamal.elgamal_decrypt(sk, c_prod) # decrypted product

    prod_of_d = (dec1 * dec2) % p # product of decrypted messages

    assert d_prod == prod_of_d, "Test failed: check_product: consistency check for homomorphism"

def run_tests():
    print("Generating ElGamal keypair...")
    pk, sk = el_gamal.generate_elgamal_keypair()
    p = pk.p
    print(f"Using prime p = {p}")

    tests_passed = 0

    simple_encrypt_decrypt(pk, sk)
    tests_passed += 1

    boundary_msg_low(pk, sk)
    tests_passed += 1

    boundary_msg_high(pk, sk)
    tests_passed += 1

    several_random_calls(pk, sk)
    tests_passed += 1  

    homomorphic_mult(pk, sk)
    tests_passed += 1

    encrypt_twice(pk)
    tests_passed += 1

    commutativity(pk)
    tests_passed += 1

    invalid_msg_low(pk)
    tests_passed += 1

    invalid_msg_high(pk)
    tests_passed += 1

    homomorphism_consistency(pk, sk)
    tests_passed += 1

    print(f"All {tests_passed} tests passed.")


if __name__ == "__main__":
    run_tests()