import random
import math

def evklid(a, b):
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = evklid(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def reverse(number, module):
    gcd, x, y = evklid(number, module)

    if gcd == 1:
        return (x % module + module) % module

    else:
        return -1

def miller(p, q=30):
    if p <= 3:
        raise Exception('Число повинно бути більше 3.')

    if p % 2 == 0:
        return False
    d = p - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for x in range(q):
        a = random.randint(2, p-2)
        b = pow(a, d, p)
        if b == 1 or b == p-1:
            continue
        for x in range(s-1):
            b = (b*b) % p
            if b == p-1:
                break
        else:
            return False
    return True

def primary():
    bits = 256
    while True:
        prim_number = (random.randrange(2 ** (bits - 1), 2 ** bits))
        if not miller(prim_number):
            print(f"{prim_number}")
        else:
            return prim_number

def create_key():
    while True:
        keys = []
        for x in range(4):
            key = primary()
            keys.append(key)
        if keys[0] * keys[1] < keys[2] * keys[3]:
            return keys

def rsa_key_pair(p, q):
    n = p * q
    eler = (p - 1) * (q - 1)
    e = random.randrange(2, eler - 1)
    while math.gcd(e, eler) != 1:
        e = random.randrange(2, eler- 1)
    d = reverse(e, eler) % eler
    return d, n, e

def encode(m, e, n):
    return pow(m, e, n)

def decode(c, d, n):
    return pow(c, d, n)

def sign(m, d, n):
    return  pow(m, d, n)

def check_signature(m, s, e, n):
    return m == pow(s, e, n)

def key_send(k, d, e2, n2, n):
    k2 = encode(k, e2, n2)
    s = sign(k, d, n)
    s2 = encode(s, e2, n2)
    return k2, s2


def receiving_key(key_1, s2, d2, n2, e, n):
    key = decode(key_1, d2, n2)
    s = decode(s2, d2, n2)
    if check_signature(key, s, e, n):
        return True, key
    else:
        return False, 0


keys = create_key()
p, q, p2, q2 = keys[0], keys[1], keys[2], keys[3]

rsa_keys_a = rsa_key_pair(p, q)
e, n, d = rsa_keys_a[0], rsa_keys_a[1], rsa_keys_a[2]

rsa_keys_b = rsa_key_pair(p2, q2)
e2, n2, d2 = rsa_keys_b[0], rsa_keys_b[1], rsa_keys_b[2]

msg = random.randint(0, n)
start_key = random.randint(0, n)
encoded_key, dig_sign = key_send(start_key, d, e2, n2, n)

encoded_msg = encode(msg, e, n)
received_key = receiving_key(encoded_key, dig_sign, d2, n2, e, n)
decoded_msg = decode(encoded_msg, d, n)

print("\nКлючі персонажа - А ")
print(' e -',e,'\n','n -',n,'\n','d -',d,'\n','p -',p,'\n','q -',q,'\n')

print("Ключі персонажа - B ")
print(' e2 -',e2,'\n','n2 -',n2,'\n','d2 -',d2,'\n','p2 -',p2,'\n','q2 -',q2,'\n')

print(' Початковий ключ -', start_key,'\n','Повідомлення -',msg, '\n')


if received_key[0]:
    print('Ключ отримали', received_key,'\n')
if not received_key[0]:
    print('Помилка')
print(' Зашифроване повідомлення -',encoded_msg,'\n','Розшифроване повідомлення',decoded_msg, '\n')
