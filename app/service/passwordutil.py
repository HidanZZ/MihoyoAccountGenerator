import random

length = 15


def get_pass():
    password = []
    count = 0
    word = ''
    while count < length:
        rand = random.randint(0, 3)
        if rand == 0:
            b = int(random.randint(97, 123))
            password.append(b)
        elif rand == 1:
            b = random.randint(65, 91)
            password.append(b)
        elif rand == 2:
            b = random.randint(48, 58)
            password.append(b)
        # elif rand == 3:
        #     r = random.randint(0, 2)
        #     if r == 0:
        #         b = random.randint(33, 48)
        #         password.append(b)
        #     elif r == 1:
        #         b = random.randint(91, 97)
        #         password.append(b)
        #     elif r == 2:
        #         b = random.randint(123, 126)
        #         password.append(b)
        count += 1
        word = "".join([chr(c) for c in password])
    return word
