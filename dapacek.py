import requests
from bs4 import BeautifulSoup

def check_da_pa(url):
    try:
        response = requests.get(f"https://www.websiteseochecker.com/bulk-check-page-authority/?url={url}")
        soup = BeautifulSoup(response.content, 'html.parser')
        da_tag = soup.find('input', {'name': 'da'})
        pa_tag = soup.find('input', {'name': 'pa'})
        if da_tag and pa_tag:
            da = da_tag.get('value')
            pa = pa_tag.get('value')
            return f"DA: {da}, PA: {pa}"
        else:
            return "Error: DA PA data not found"
    except Exception as e:
        print(f"Error checking DA PA: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    print(check_da_pa(url))
