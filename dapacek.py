import requests
from bs4 import BeautifulSoup

def check_da_pa_smallseotools(url):
    try:
        response = requests.get(f"https://smallseotools.com/domain-authority-checker/?q={url}")
        soup = BeautifulSoup(response.content, "html.parser")
        da = soup.find("div", {"class": "da-result"}).find("span").text.strip()
        pa = soup.find("div", {"class": "pa-result"}).find("span").text.strip()
        return f"DA: {da}, PA: {pa}"
    except Exception as e:
        print(f"Error checking DA PA: {e}")
        return None

if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    print(check_da_pa_smallseotools(url))
