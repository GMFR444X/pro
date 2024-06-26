import requests
from bs4 import BeautifulSoup

def find_subdomains(url):
    try:
        response = requests.get(f"https://crt.sh/?q=%.{url}")
        soup = BeautifulSoup(response.content, 'html.parser')
        subdomains = set()
        for td in soup.find_all('td'):
            subdomain = td.text.strip()
            if subdomain.endswith(f'.{url}'):
                subdomains.add(subdomain)
        return '\n'.join(subdomains)
    except Exception as e:
        print(f"Error finding subdomains: {e}")
        return ""

if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    print(find_subdomains(url))