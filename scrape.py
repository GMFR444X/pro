import requests

# List of URLs to fetch proxies from
urls = [
    "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxyscan.io/api/proxy?format=json&type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://proxy-daily.com/api/proxylist?apikey=your_api_key",
    "https://api.getproxylist.com/proxy",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://getproxylist.com/proxy",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxydocker.com/api/proxies?apiKey=your_api_key&protocol=https",
    "https://proxy-daily.com/api/proxylist?apikey=your_api_key",
    "https://www.proxyscan.io/api/proxy?format=json&type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://proxy11.com/api/proxy.json",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.socks-proxy.net/api/proxy?format=json&type=https",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://proxy11.com/api/proxy.json",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxyscan.io/api/proxy?format=json&type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://proxy-daily.com/api/proxylist?apikey=your_api_key",
    "https://api.getproxylist.com/proxy",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://getproxylist.com/proxy",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxydocker.com/api/proxies?apiKey=your_api_key&protocol=https",
    "https://proxy-daily.com/api/proxylist?apikey=your_api_key",
    "https://www.proxyscan.io/api/proxy?format=json&type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://proxy11.com/api/proxy.json",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.socks-proxy.net/api/proxy?format=json&type=https",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://proxy11.com/api/proxy.json"
]

# Function to fetch proxies from URLs
def fetch_proxies(urls):
    proxies = []

    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.text.split('\n')
                proxies.extend(data)
        except Exception as e:
            print(f"Failed to fetch proxies from {url}: {e}")

    return proxies

# Fetch proxies from URLs
all_proxies = fetch_proxies(urls)

# Remove duplicate proxies
unique_proxies = list(set(all_proxies))

# Save proxies to file
with open('proxy.txt', 'w') as file:
    for proxy in unique_proxies:
        file.write(proxy + '\n')

print("Proxies have been saved to proxy.txt")