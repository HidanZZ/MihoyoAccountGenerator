import requests
import time

url_generate = 'https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1'


# print response
def generate():
    response = requests.get(url_generate)
    random = response.json()[0]
    return random


def get_verification(random):
    login, domain = random.split('@')
    c = 0
    while True:
        response = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}')

        if len(response.json()) == 0:
            time.sleep(0.5)
        else:
            return response.json()[0]['subject'][:6]
        print(c)
        c += 1


if __name__ == '__main__':
    test = generate()
    print(test)
    print(get_verification(test))
