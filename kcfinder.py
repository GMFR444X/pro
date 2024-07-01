import requests
from multiprocessing import Pool
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from colorama import Fore, Style
import argparse

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def load_paths():
    with open('path.txt') as f:
        return f.read().splitlines()

rfmlist = load_paths()

def rfm(url):
    s = requests.Session()
    pala = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 9 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    for i in rfmlist:
        try:
            r = s.get(f'http://{url}{i}', timeout=7, verify=False, headers=pala)
            if 'alert("Unknown error");' in r.text or "alert('Unknown error');" in r.text:
                print(f'{Fore.YELLOW}[{Fore.WHITE}FOUND{Fore.YELLOW}] {url}{i}')
                with open('result_kcfinder.txt', 'a+') as f:
                    f.write(f'http://{url}{i}\n')
                return True
            else:
                print(f'{Fore.YELLOW}[{Fore.WHITE}NOT FOUND{Fore.YELLOW}] {url}{i}')
        except Exception as e:
            print(f'Error: {e}')

def main(filename, thread_count):
    print("KCFinder Mass Scanner Mass Path")
    with open(filename) as f:
        asu = f.read().splitlines()
    p = Pool(thread_count)
    p.map(rfm, asu)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KCFinder Mass Scanner")
    parser.add_argument("filename", type=str, help="File containing list of websites")
    parser.add_argument("thread_count", type=int, help="Number of threads to use")
    args = parser.parse_args()

    main(args.filename, args.thread_count)
