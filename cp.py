import requests
import sys

def check_login(url, username, password):
    login_url = f"{url}/login/?user={username}&pass={password}"
    try:
        response = requests.get(login_url)
        if "Login Successful" in response.text:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

def main(file_path, duration):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    good_logins = []

    for line in lines:
        parts = line.strip().split('|')
        if len(parts) != 3:
            print(f"Invalid format: {line.strip()}")
            continue

        url, username, password = parts
        if check_login(url, username, password):
            good_logins.append(f"{url}|{username}|{password}")
            print(f"Login successful: {url}")

    if good_logins:
        with open('good.txt', 'w') as good_file:
            good_file.write("\n".join(good_logins))
        print("Successful logins saved to good.txt")
    else:
        print("No successful logins found.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python cp.py <file_path> <duration>")
        sys.exit(1)

    file_path = sys.argv[1]
    duration = int(sys.argv[2])
    main(file_path, duration)
