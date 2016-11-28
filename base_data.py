import random

r = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
     'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
     '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

ron = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def get_random_letter_number(n=16):
    token = []
    for i in range(n):
        token.append(random.choice(r))
    return ''.join(token)


def get_random_number(n=15):
    imei = []
    for i in range(n):
        imei.append(random.choice(ron))
    return ''.join(imei)