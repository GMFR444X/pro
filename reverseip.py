import requests

def find_domains_by_ip(ip):
    try:
        url = f"https://www.yougetsignal.com/tools/web-sites-on-web-server/php/get-web-sites-on-web-server-json.php?remoteAddress={ip}"
        response = requests.get(url)
        data = response.json()

        domains = []
        for site in data["sites"]:
            domains.append(site["domain"])
        
        return domains
    except Exception as e:
        print(f"Error finding domains by IP: {e}")
        return []

if __name__ == "__main__":
    import sys
    ip = sys.argv[1]
    print(find_domains_by_ip(ip))
