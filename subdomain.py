import requests
from bs4 import BeautifulSoup

def find_subdomains(url):
    try:
        session = requests.Session()
        response = session.get("https://dnsdumpster.com")
        soup = BeautifulSoup(response.content, "html.parser")
        csrfmiddlewaretoken = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]
        
        headers = {
            "Referer": "https://dnsdumpster.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        cookies = {"csrftoken": csrfmiddlewaretoken}
        data = {
            "csrfmiddlewaretoken": csrfmiddlewaretoken,
            "targetip": url
        }
        
        response = session.post("https://dnsdumpster.com", headers=headers, cookies=cookies, data=data)
        soup = BeautifulSoup(response.content, "html.parser")
        
        subdomains = set()
        for td in soup.find_all("td"):
            subdomain = td.text.strip()
            if subdomain.endswith(f".{url}"):
                subdomains.add(subdomain)
        
        return subdomains
    except Exception as e:
        print(f"Error finding subdomains: {e}")
        return set()

if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    print(find_subdomains(url))
