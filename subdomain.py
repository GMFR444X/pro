import requests
from bs4 import BeautifulSoup

def find_subdomains(url):
    try:
        response = requests.get(f"https://dnsdumpster.com/")
        soup = BeautifulSoup(response.content, 'html.parser')
        csrfmiddlewaretoken = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
        headers = {
            'Referer': 'https://dnsdumpster.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        cookies = {
            'csrftoken': csrfmiddlewaretoken
        }
        data = {
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'targetip': url
        }
        session = requests.Session()
        response = session.post('https://dnsdumpster.com/', headers=headers, cookies=cookies, data=data)
        soup = BeautifulSoup(response.content, 'html.parser')
        subdomains = set()
        for td in soup.find_all('td'):
            subdomain = td.text.strip()
            if subdomain.endswith(f'.{url}'):
                subdomains.add(subdomain)
        return subdomains
    except Exception as e:
        return f"Error finding subdomains: {e}"

if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    print(find_subdomains(url))
