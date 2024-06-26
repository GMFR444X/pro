import requests

def find_domains_by_ip(ip):
    try:
        url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
        response = requests.get(url)
        if response.status_code == 200:
            domains = response.text.strip().split("\n")
            return '\n'.join(domains)
        else:
            return f"Error: {response.status_code} - {response.reason}"
    except Exception as e:
        print(f"Error finding domains by IP: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    import sys
    ip = sys.argv[1]
    print(find_domains_by_ip(ip))
