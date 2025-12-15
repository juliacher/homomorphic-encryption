import el_gamal     


class Client_EG:
    
    def __init__(self):
        self.public_key = None
        self.private_key = None

    def generate_elgamal_keypair(self):
        self.public_key, self.private_key = el_gamal.generate_elgamal_keypair()

    def encrypt_cart(self, cart):
        if self.public_key is None:
            raise ValueError("Public key not generated.")

        enc_cart = []
        for price, quantity in cart:
            enc_quantity = el_gamal.elgamal_encrypt(self.public_key, quantity)
            enc_cart.append((price, enc_quantity))
        return enc_cart

    def decrypt_and_total(self, enc_cart):
        # decript, compute and return total cost
        if self.private_key is None:
            raise ValueError("Private key not generated.")

        total = 0
        for price, enc_quantity in enc_cart:
            quantity = el_gamal.elgamal_decrypt(self.private_key, enc_quantity)
            total += price * quantity
        return total


class Server_EG:
    # Server cannot compute the sum of costs homomorphically,
    # because the scheme is multiplicatively homomorphic, 
    # so the server simply forwards the encrypted cart
    
    def process_cart(self, enc_cart):
        return enc_cart


def demo_shopping_cart_elgamal():

    cart = [
        (2000, 1),  
        (120,  5),   
        (1999, 3),   
    ]

    client = Client_EG()
    client.generate_elgamal_keypair()
    enc_cart = client.encrypt_cart(cart)

    server = Server_EG()
    enc_cart_processed = server.process_cart(enc_cart)

    total_from_client = client.decrypt_and_total(enc_cart_processed)
    total_plain = sum(price * quantity for price, quantity in cart)

    print(f"Total cost computed by client after decryption (cents): {total_from_client}")
    print(f"Reference plaintext total (cents):                   {total_plain}")

    assert total_from_client == total_plain, \
        "ElGamal shopping cart: decrypted total does not match plaintext reference."


if __name__ == "__main__":
    demo_shopping_cart_elgamal()
