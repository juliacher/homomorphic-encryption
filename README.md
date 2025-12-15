# Homomorphic Encryption

This repository contains Python implementations and practical examples of different homomorphic encryption schemes.  
It demonstrates how computations can be performed directly on encrypted data and highlights the capabilities and limitations of each approach.

The project includes:
- multiplicative homomorphic encryption with **ElGamal**,
- additive homomorphic encryption with **Paillier**,
- fully homomorphic computation using **Concrete-Numpy**.

---

## Repository Contents

### `el_gamal.py`
Implementation of the **ElGamal encryption scheme**.

This file contains:
- ElGamal key generation,
- encryption and decryption of integers,
- homomorphic multiplication of ciphertexts.

ElGamal supports **multiplicative homomorphism**, meaning that multiplying two ciphertexts corresponds to multiplying the underlying plaintexts.

---

### `el_gamal_tests.py`
Test suite for the ElGamal implementation.

The tests verify:
- correct encryption–decryption (round-trip),
- boundary values for valid messages,
- randomized encryption behavior,
- homomorphic multiplication,
- consistency of homomorphic properties,
- handling of invalid inputs.

Running this file executes all tests and reports whether they pass.

---

### `elgamal_chart.py`
Example application demonstrating **ElGamal in a shopping-cart scenario**.

In this example:
- quantities are encrypted using ElGamal,
- prices remain in plaintext,
- the server cannot compute the total cost homomorphically (due to lack of additive homomorphism),
- the client decrypts the quantities and computes the total locally.

This illustrates how the choice of homomorphic scheme affects system design.

---

### `pailler_chart.py`
Example application demonstrating **Paillier encryption in a shopping-cart scenario**.

This file shows how:
- encrypted quantities can be multiplied by plaintext prices,
- encrypted item costs can be added together homomorphically,
- the server can compute an **encrypted total cost** without learning individual quantities,
- the client decrypts only the final result.

Paillier supports **additive homomorphism** and multiplication by plaintext constants.

---

### `mean.py`
Demonstration of **fully homomorphic encryption (FHE)** using **Concrete-Numpy**.

This file includes:
- computation of the mean of encrypted integers,
- computation of the mean with fixed-point precision (two decimal digits) using integer scaling,
- tests verifying correctness of encrypted computation.

All arithmetic is performed directly on encrypted data and decrypted only at the end.

---

## Requirements

- Python 3.8–3.11
- `phe` library (for Paillier):
  ```bash
  pip install phe
