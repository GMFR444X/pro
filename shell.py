import requests
import threading

def check_website(website, output_file):
    try:
        response = requests.get(website)
        status_code = response.status_code
        # Jika status code OK, simpan domain ke dalam file output dan tampilkan pesan berwarna biru di console
        if status_code == 200:
            print(f"\033[94m[GOOD] {website} - Status Code: {status_code}\033[0m")
            with open(output_file, 'a') as f:
                f.write(f"{website} - Status Code: {status_code}\n")
        # Jika status code bukan 200, tampilkan pesan berwarna merah di console
        else:
            print(f"\033[91m[ERROR] {website} - Status Code: {status_code}\033[0m")
    except Exception as e:
        # Jika ada kesalahan, tampilkan pesan berwarna merah di console
        print(f"\033[91m[ERROR] {website} - {e}\033[0m")

def main(websites_file, output_file, num_threads):
    # Buka file domain
    with open(websites_file, 'r') as f:
        websites = f.readlines()

    # Bersihkan daftar domain dari spasi dan baris baru
    websites = [website.strip() for website in websites]

    # Buat thread untuk setiap website
    threads = []
    for website in websites:
        t = threading.Thread(target=check_website, args=(website, output_file))
        threads.append(t)

    # Jalankan semua thread
    for thread in threads:
        thread.start()

    # Tunggu sampai semua thread selesai
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    # Ambil input dari pengguna
    websites_file = input("Input website list: ")
    output_file = "goodshell.txt"
    num_threads = int(input("Threads: "))

    # Panggil fungsi main dengan input dari pengguna
    main(websites_file, output_file, num_threads)