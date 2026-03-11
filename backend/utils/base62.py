import string

CHARACTERS = string.digits + string.ascii_lowercase + string.ascii_uppercase
BASE = len(CHARACTERS)


def encode(num):
    """Encodes a number into a base62 string."""
    if num == 0:
        return CHARACTERS[0]

    result = []
    while num > 0:
        num, rem = divmod(num, BASE)
        result.append(CHARACTERS[rem])

    return ''.join(reversed(result))


def decode(s):
    """Decodes a base62 string back into a number."""
    num = 0
    for char in s:
        num = num * BASE + CHARACTERS.index(char)
    return num