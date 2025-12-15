import numpy as np
import concrete.numpy as cnp

#----mean over a list of six encrypted integers

# calculate mean of 6 numbers
def mean_six_plain(a, b, c, d, e, f):
    return (a + b + c + d + e + f) // 6

# create labels for 6 numbers
def compile_mean_six():
    input_desc = {
        "a": cnp.EncryptedScalar(),
        "b": cnp.EncryptedScalar(),
        "c": cnp.EncryptedScalar(),
        "d": cnp.EncryptedScalar(),
        "e": cnp.EncryptedScalar(),
        "f": cnp.EncryptedScalar(),
    }

    compiler = cnp.Compiler(mean_six_plain, input_desc)
    circuit = compiler.compile()
    return circuit


# tests
def test_mean_six():
    circuit = compile_mean_six()

    # create input
    inputs = {
        "a": 10,
        "b": 20,
        "c": 30,
        "d": 40,
        "e": 50,
        "f": 60,
    }

    encrypted = circuit.encrypt(inputs)
    encrypted_output = circuit.run(encrypted)
    decrypted_output = circuit.decrypt(encrypted_output)

    print("Decrypted mean:", decrypted_output)
    assert decrypted_output == (10 + 20 + 30 + 40 + 50 + 60) // 6

#--------mean with a precision of two decimal digits

def mean_six_scaled_plain(a, b, c, d, e, f):
    # scaled outside the func
    total = a + b + c + d + e + f
    return total // 6  

def compile_mean_six_scaled():
    input_desc = {
        "a": cnp.EncryptedScalar(),
        "b": cnp.EncryptedScalar(),
        "c": cnp.EncryptedScalar(),
        "d": cnp.EncryptedScalar(),
        "e": cnp.EncryptedScalar(),
        "f": cnp.EncryptedScalar(),
    }

    compiler = cnp.Compiler(mean_six_scaled_plain, input_desc)
    circuit = compiler.compile()
    return circuit

def test_mean_six_scaled():
    circuit = compile_mean_six_scaled()

    # scaled by 100
    vals = [1.23, 4.56, 3.78, 2.50, 6.80, 5.10]
    scaled_vals = [int(v * 100) for v in vals]

    inputs = {
        "a": scaled_vals[0],
        "b": scaled_vals[1],
        "c": scaled_vals[2],
        "d": scaled_vals[3],
        "e": scaled_vals[4],
        "f": scaled_vals[5],
    }

    encrypted = circuit.encrypt(inputs)
    encrypted_output = circuit.run(encrypted)
    decrypted_output = circuit.decrypt(encrypted_output)
    # convert back 
    mean_scaled = decrypted_output / 100

    # reference mean
    ref_mean = sum(vals) / 6

    print("Decrypted mean (2 digits precision):", mean_scaled)
    print("Reference plaintext mean:", ref_mean)

    # Allow small rounding differences
    assert abs(mean_scaled - ref_mean) < 0.01



if __name__ == "__main__":
    print("Test mean six:")
    test_mean_six()
    print("\n")
    print("Test mean six scaled:")
    test_mean_six_scaled()
