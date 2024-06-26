import requests

def check_wordpress_logins(file_path):
    results = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                site, username, password = line.strip().split('|')
                login_result = try_login(site, username, password)
                results.append(login_result)
    except Exception as e:
        print(f"Error checking WordPress logins: {e}")
    return '\n'.join(results)

def try_login(site, username, password):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        session = requests.Session()
        response = session.get(site, headers=headers, timeout=10)

        if response.status_code == 200 or response.status_code == 403 or 'Powered by WordPress' in response.text or '/wp-login.php' in response.text:
            login_data = {
                'log': username,
                'pwd': password
            }
            login_response = session.post(site, headers=headers, data=login_data, timeout=10)

            if 'wp-admin/profile.php' in login_response.text or 'Found' in login_response.text or '/wp-admin' in login_response.text:
                return f"{site}#{username}@{password} - Success"
            else:
                return f"{site}#{username}@{password} - Failed"
        else:
            return f"{site}#{username}@{password} - Not a WordPress site or inaccessible"
    except Exception as e:
        return f"{site}#{username}@{password} - Error: {str(e)}"

if __name__ == "__main__":
    import sys
    file_id = sys.argv[1]
    print(check_wordpress_logins(file_id))
