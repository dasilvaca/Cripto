def get_every_string_of_length(alphabet, length):
    """
    Returns every string of length from alphabet.
    """
    src = alphabet
    n = len(src)
    m = length
    l = [0]*m
    i = 0
    possible_strings = []
    while i < m:
        key = [src[x] for x in l]
        key = "".join(key)
        possible_strings.append(key)
        i = 0
        l[i] += 1
        while (i < m) and l[i] >= n:
            l[i] = 0
            i += 1
            if i < m:
                l[i] += 1
    return possible_strings

# get_every_string_of_length("abcdefghijklmnopqrstuvxyz", 3)


def vigener_decryptions(text, key):
    """
    Decrypts a string using a Vigener cipher.
    """
    text.lower()
    key.lower()
    result = ""
    for i in range(len(text)):
        x = key[i % len(key)]
        x_n = (ord(x) - ord('a')) % 26
        y = text[i]
        y_n = ord(y) - ord('a') % 26
        result += chr(( (y_n - x_n) % 26) + ord('a'))
    return result

print(vigener_decryptions("rijvsuyvjn", "key"))