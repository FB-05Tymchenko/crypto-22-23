import random
import math


class RSA:
    def __init__(self, p: int, q: int):
        self.p = p
        self.q = q
        self.e, self.n, self.d = self.generate_rsa(self.p, self.q)

    def extended_euclid(self, first_num: int, second_num: int) -> (int, int, int):
        if second_num == 0:
            return first_num, 1, 0
        d, x, y = self.extended_euclid(second_num, first_num % second_num)
        return d, y, x - (first_num // second_num) * y

    def inverse_mod(self, first_num: int, second_num: int) -> int:
        return self.extended_euclid(first_num, second_num)[1]

    def generate_rsa(self, first_key: int, second_key: int) -> (int, int, int):
        n = first_key * second_key
        phi = (first_key - 1) * (second_key - 1)
        e = random.randrange(2, phi - 1)
        while math.gcd(e, phi) != 1:
            e = random.randrange(2, phi - 1)
        d = self.inverse_mod(e, phi) % phi
        return d, n, e


class Client:
    def __init__(self, p: int, q: int):
        self.RSA = RSA(p, q)

    @staticmethod
    def encryption(msg: int, e: int, n: int) -> int:
        return pow(msg, e, n)

    @staticmethod
    def decryption(encrypted_msg: int, d: int, n: int) -> int:
        return pow(encrypted_msg, d, n)

    @staticmethod
    def signature(sign: int, d: int, n: int) -> int:
        return pow(sign, d, n)

    @staticmethod
    def authentication(msg, sign, e, n) -> int:
        return msg == pow(sign, e, n)

    @staticmethod
    def final_authentication(sign: int, e: int, n: int) -> int:
        return pow(sign, e, n)

    def send_key(self, msg: int, e1: int, n1: int) -> (int, int):
        encrypt_msg = self.encryption(msg, e1, n1)
        sign = self.signature(msg, self.RSA.d, self.RSA.n)
        encrypt_sign = self.encryption(sign, e1, n1)

        return encrypt_msg, encrypt_sign

    def receive_key(self, encrypt_msg: int, encrypt_sign: int, e: int, n: int) -> int:
        msg = self.decryption(encrypt_msg, self.RSA.d, self.RSA.n)
        sign = self.decryption(encrypt_sign, self.RSA.d, self.RSA.n)

        if self.authentication(msg, sign, e, n):
            print('Key matched!')
            return msg
        else:
            print('Key did not match!')


def is_probably_prime(num: int, count: int = 10) -> bool:
    if num in (2, 3):
        return True
    if num == 1 or num % 2 == 0:
        return False

    s = num - 1
    r = 0
    while s % 2 == 0:
        s //= 2
        r += 1

    for _ in range(count):
        a = random.randint(2, num - 2)
        x = pow(a, s, num)
        if x == 1:
            continue
        for _ in range(r):
            if x == num - 1:
                break
            x = (x * x) % num
        else:
            return False
    return True


def generate_prime(bit_len: int) -> int:
    while True:
        number = (random.randrange(2 ** (bit_len - 1), 2 ** bit_len))
        if is_probably_prime(number):
            return number


def generate_key() -> (int, int, int, int):
    while True:
        keys = []
        for i in range(0, 4):
            key = generate_prime(256)
            keys.append(key)
        if keys[0] * keys[1] < keys[2] * keys[3]:
            return keys[0], keys[1], keys[2], keys[3]


p_0, q_0, p_1, q_1 = generate_key()
first_cli = Client(p_0, q_0)
second_cli = Client(p_1, q_1)
message, message_sign = first_cli.send_key(14, second_cli.RSA.e, second_cli.RSA.n)
result = second_cli.receive_key(message + 1, message_sign, first_cli.RSA.e, first_cli.RSA.n)
print(f"Combination for A:\np:{p_0}\nq:{q_0}")

print(f"Combination for B:\np:{p_1}\nq:{q_1}")

print("------Keys for A:------")
print(f"d:{first_cli.RSA.d}\nn:{first_cli.RSA.n}\ne:{first_cli.RSA.e}")

print("------Keys for B:------")
print(f"d:{second_cli.RSA.d}\nn:{second_cli.RSA.n}\ne:{second_cli.RSA.e}")
print(f'Message - {result}')

server_n = 'A06EC901529E1BB7FA176A6D1954345BCE0185880956652EAD17A758B85316C1'
server_e = '10001'
test_message_hex = '81B'
sign = '5E39E7BDD920C73D0F953B0DEDD7F52C660A29A97FC11BF6C447390CB4ED974F'
encrypted_msg = '63F45557833DD49F83DD9573C9F07D9438DBE7CD1471C14D924A9F2C50A77BE8'

server_n_int = int(server_n, base=16)
server_e_int = int(server_e, base=16)
test_message = int(test_message_hex, base=16)
sign_int = int(sign, base=16)
encrypted_int = int(encrypted_msg, base=16)

print("Encryption:", Client.encryption(test_message, server_e_int, server_n_int))
print(Client.authentication(test_message, sign_int, server_e_int, server_n_int))

