import requests
from bs4 import BeautifulSoup

def find_domains_by_ip(ip):
    try:
        response = requests.get(f"https://www.yougetsignal.com/tools/web-sites-on-web-server/php/get-web-sites-on-web-server-json.php", params={'remoteAddress': ip})
        data = response.json()
        domains = [site['domain'] for site in data['sites']]
        return domains
    except Exception as e:
        return f"Error finding domains by IP: {e}"

if __name__ == "__main__":
    import sys
    ip = sys.argv[1]
    print(find_domains_by_ip(ip))
