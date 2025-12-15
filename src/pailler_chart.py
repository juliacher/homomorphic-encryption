import phe as paillier
import numpy as np

class Client:
    def __init__(self):
        self.public_key = None
        self.private_key = None

    def generate_paillier_keypair(self):
        self.public_key, self.private_key = paillier.generate_paillier_keypair()

    def encrypt_cart(self, cart):
        if self.public_key is None:
            raise ValueError("Public key not generated. Call generate_paillier_keypair() first.")

        encrypted_cart = []
        for price, quantity in cart:
            enc_quantity = self.public_key.encrypt(quantity)
            encrypted_cart.append((price, enc_quantity))
        return encrypted_cart
    
    def decrypt_total(self, enc_total):
        if self.private_key is None:
            raise ValueError("Private key not generated. Call generate_paillier_keypair() first.")

        total = self.private_key.decrypt(enc_total)
        return total
    

class Server:

    def compute_encrypted_total(self, encrypted_cart, public_key):
        
        enc_total = public_key.encrypt(0)

        for price, enc_quantity in encrypted_cart:
            enc_item_cost = enc_quantity * price
            enc_total = enc_total + enc_item_cost

        return enc_total
    

def demo_shopping_cart():

    cart = [
        (2000, 1),   
        (120, 5),    
        (1999, 3),   
    ]

    # Client setup and encrypt
    client = Client()
    client.generate_paillier_keypair()
    encrypted_cart = client.encrypt_cart(cart)

    # Server computes encrypted total
    server = Server()
    enc_total = server.compute_encrypted_total(encrypted_cart, client.public_key)

    # Client decrypts total
    total_plain = client.decrypt_total(enc_total)

    # Validate: compute total in plaintext
    total_plain_ref = sum(price * quantity for price, quantity in cart)

    print(f"Decrypted total cost (cents): {total_plain}")
    print(f"Reference total cost (cents): {total_plain_ref}")
    assert total_plain == total_plain_ref, "Encrypted and plaintext totals do not match!"


if __name__ == "__main__":
    demo_shopping_cart()