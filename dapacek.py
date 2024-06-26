import requests
from bs4 import BeautifulSoup

def check_da_pa(url):
    try:
        response = requests.get(f"https://www.websiteseochecker.com/bulk-check-page-authority/?url={url}")
        soup = BeautifulSoup(response.content, 'html.parser')
        da = soup.find('input', {'name': 'da'}).get('value')
        pa = soup.find('input', {'name': 'pa'}).get('value')
        return f"DA: {da}, PA: {pa}"
    except Exception as e:
        print(f"Error checking DA PA: {e}")
        return ""

if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    print(check_da_pa(url))