def RC4_initialization(key):
    K = key # "thisisaverylongkey"
    T = []
    S = []

    for i in range(256):
        S.append(i)
        T.append(K[i % len(K)])

    j = 0
    for i in range(256):
        print((j + ord(T[i]) + S[i]) % 256)
        j = (j + S[i] + ord(T[i])) % 256
        S[i], S[j] = S[j], S[i]

    return T, S, K

def RC4_encapsulated(message, key):
    T, S, K = RC4_initialization(key)
    ciphered_message = []
    i, j = 0, 0

    for l in range(len(message)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        if type(message) == str:
            ciphered_message.append(chr(ord(message[l]) ^ S[(S[i] + S[j]) % 256]))
        elif type(message) == list:
            ciphered_message.append(chr(ord(message[l]) ^ S[(S[i] + S[j]) % 256]))

    
    # print(ciphered_message)
    return ciphered_message

    # Let be n a positive integer to get a multiple of 256 - i on each item of the array T.

def arrayT_gen(n):
    if n == 0:
        n = 1
    elif n < 0:
        n = -n
    T = []
    for i in range(256):
        if i > 0:
            T.append(((256 * n) - i) + 1)
        else:
            T.append(((256 * n) - i))
    return T

def key_gen(n):
    T = arrayT_gen(n)
    k = []
    for i in range(len(T)):
        k.append(chr(T[i]))
    return k


key = key_gen(1)

T, S, k = RC4_initialization(key)

print(T)
print(S)