import requests
from multiprocessing import Pool
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from colorama import Fore, Style
import argparse

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

rfmlist = [
    "/admin/ckeditor/kcfinder-3.12/upload.php", "/admin/ckeditor/kcfinder/upload.php",
    "/admin/ckeditor/plugins/kcfinder-3.12/upload.php", "/admin/ckeditor/plugins/kcfinder/upload.php","/admin/core/kcfinder/upload.php", "/admin/js/kcfinder-3.12/upload.php", "/admin/js/kcfinder/upload.php", "/admin/plugin/kcfinder-3.12/upload.php", "/admin/plugin/kcfinder/upload.php", "/admin/plugins/kcfinder-3.12/upload.php", "/admin/plugins/kcfinder/upload.php", "/adminpanel/kcfinder-3.12/upload.php", "/adminpanel/kcfinder/upload.php", "/app/webroot/js/kcfinder-3.12/upload.php", "/app/webroot/js/kcfinder/upload.php", "/app/webroot/kcfinder-3.12/upload.php", "/app/webroot/kcfinder/upload.php", "/application/themes/admin/assets/js/kcfinder-3.12/upload.php", "/application/themes/admin/assets/js/kcfinder/upload.php", "/asset/js_ckeditor/kcfinder-3.12/upload.php", "/asset/js_ckeditor/kcfinder/upload.php", "/asset/kcfinder-3.12/upload.php", "/asset/kcfinder/upload.php", "/asset/webadmin/js/kcfinder-3.12/upload.php", "/asset/webadmin/js/kcfinder/upload.php", "/assets/admin/js/kcfinder-3.12/upload.php", "/assets/admin/js/kcfinder/upload.php", "/assets/admin/plugins/kcfinder-3.12/upload.php", "/assets/admin/plugins/kcfinder/upload.php", "/assets/bo/plugin/kcfinder-3.12/upload.php", "/assets/bo/plugin/kcfinder/upload.php", "/assets/ckeditor/kcfinder-3.12/upload.php", "/assets/ckeditor/kcfinder/upload.php", "/assets/ckeditor/plugins/kcfinder-3.12/upload.php", "/assets/ckeditor/plugins/kcfinder/upload.php", "/assets/frontend/js/ckeditor/kcfinder-3.12/upload.php", "/assets/frontend/js/ckeditor/kcfinder/upload.php", "/assets/frontend/js/kcfinder-3.12/upload.php", "/assets/frontend/js/kcfinder/upload.php", "/assets/js/ckeditor/kcfinder-3.12/upload.php", "/assets/js/ckeditor/kcfinder/upload.php", "/assets/js/ckeditor/plugins/kcfinder-3.12/upload.php", "/assets/js/ckeditor/plugins/kcfinder/upload.php", "/assets/js/kcfinder-3.12/upload.php", "/assets/js/kcfinder/upload.php", "/assets/js/mylibs/kcfinder-3.12/upload.php", "/assets/js/mylibs/kcfinder/upload.php", "/assets/js/plugins/ckeditor/plugins/kcfinder-3.12/upload.php", "/assets/js/plugins/ckeditor/plugins/kcfinder/upload.php", "/assets/js/scripts/kcfinder-3.12/upload.php", "/assets/js/scripts/kcfinder/upload.php", "/assets/kcfinder-3.12/upload.php", "/assets/kcfinder/upload.php", "/assets/lib/kcfinder-3.12/upload.php", "/assets/lib/kcfinder/upload.php", "/assets/libs/kcfinder-3.12/upload.php", "/assets/libs/kcfinder/upload.php", "/assets/scripts/kcfinder-3.12/upload.php", "/assets/scripts/kcfinder/upload.php", "/assets/vendor/kcfinder-3.12/upload.php", "/assets/vendor/kcfinder/upload.php", "/assets/vendors/js/kcfinder-3.12/upload.php", "/assets/vendors/js/kcfinder/upload.php", "/assets/vendors/kcfinder-3.12/upload.php", "/assets/vendors/kcfinder/3.12/upload.php", "/assets/vendors/kcfinder/upload.php", "/assets/webadmin/js/kcfinder-3.12/upload.php", "/assets/webadmin/js/kcfinder/upload.php", "/backend/ckeditor/kcfinder-3.12/upload.php", "/backend/ckeditor/kcfinder/upload.php", "/backend/js/kcfinder-3.12/upload.php", "/backend/js/kcfinder/upload.php", "/backend/js/plugins/ckeditor/kcfinder-3.12/upload.php", "/backend/js/plugins/ckeditor/kcfinder/upload.php", "/backend/plugins/kcfinder-3.12/upload.php", "/backend/plugins/kcfinder/upload.php", "/ckeditor/kcfinder-3.12/upload.php", "/ckeditor/kcfinder/upload.php", "/ckeditor/plugins/kcfinder-3.12/upload.php", "/ckeditor/plugins/kcfinder/upload.php", "/component/kcfinder-3.12/upload.php", "/components/kcfinder/upload.php", "/core/scripts/kcfinder-3.12/upload.php", "/core/scripts/kcfinder/upload.php", "/core/scripts/wysiwyg/kcfinder-3.12/upload.php", "/core/scripts/wysiwyg/kcfinder/upload.php", "/inc_admin/plugins/kcfinder-3.12/upload.php", "/inc_admin/plugins/kcfinder/upload.php", "/js/kcfinder-3.12/upload.php", "/js/kcfinder/upload.php", "/js/tinymce/kcfinder-3.12/upload.php", "/js/tinymce/kcfinder/upload.php", "/kcfinder-3.12/upload.php", "/kcfinder/upload.php", "/lib/kcfinder-3.12/upload.php", "/lib/kcfinder/upload.php", "/libs/kcfinder-3.12/upload.php", "/libs/kcfinder/upload.php", "/media/kcfinder-3.12/upload.php", "/media/kcfinder/upload.php", "/my_cms/public/assets/plugins/ckeditor/kcfinder-3.12/upload.php", "/my_cms/public/assets/plugins/ckeditor/kcfinder/upload.php", "/packages/assets/js/kcfinder-3.12/upload.php", "/packages/assets/js/kcfinder/upload.php", "/packages/ckeditor/kcfinder-3.12/upload.php", "/packages/ckeditor/kcfinder/upload.php", "/packages/ckeditor/plugins/kcfinder-3.12/upload.php", "/packages/ckeditor/plugins/kcfinder/upload.php", "/packages/js/kcfinder-3.12/upload.php", "/packages/js/kcfinder/upload.php", "/packages/scripts/kcfinder-3.12/upload.php", "/packages/scripts/kcfinder/upload.php", "/packages/upload/kcfinder-3.12/upload.php", "/packages/upload/kcfinder/upload.php", "/panel/kcfinder-3.12/upload.php", "/panel/kcfinder/upload.php", "/public/ckeditor/kcfinder-3.12/upload.php", "/public/ckeditor/kcfinder/upload.php", "/public/ckeditor/plugins/kcfinder-3.12/upload.php", "/public/ckeditor/plugins/kcfinder/upload.php", "/public/js/kcfinder-3.12/upload.php", "/public/js/kcfinder/upload.php", "/resource/assets/kcfinder-3.12/upload.php", "/resource/assets/kcfinder/upload.php", "/resource/js/kcfinder-3.12/upload.php", "/resource/js/kcfinder/upload.php", "/resource/kcfinder-3.12/upload.php", "/resource/kcfinder/upload.php", "/resources/assets/kcfinder-3.12/upload.php", "/resources/assets/kcfinder/upload.php", "/resources/js/kcfinder-3.12/upload.php", "/resources/js/kcfinder/upload.php", "/resources/kcfinder-3.12/upload.php", "/resources/kcfinder/upload.php", "/resources/vendor/kcfinder-3.12/upload.php", "/resources/vendor/kcfinder/upload.php", "/scripts/js/kcfinder-3.12/upload.php", "/scripts/js/kcfinder/upload.php", "/scripts/kcfinder-3.12/upload.php", "/scripts/kcfinder/upload.php", "/tinymce/kcfinder-3.12/upload.php", "/tinymce/kcfinder/upload.php", "/upload/kcfinder-3.12/upload.php", "/upload/kcfinder/upload.php", "/uploads/kcfinder-3.12/upload.php", "/uploads/kcfinder/upload.php", "/vendor/kcfinder-3.12/upload.php", "/vendor/kcfinder/upload.php", "/webassist/kcfinder-3.12/upload.php", "/webassist/kcfinder/upload.php", "/third_party/kcfinder/upload.php", "/third_party/kcfinder-3.12/upload.php", "/ard/assets/js/kcfinder/upload.php", "/editor/kcfinder/upload.php", "/assets/grocery_crud/texteditor/ckeditor/kcfinder/upload.php", "/assets/text_editor/kcfinder/upload.php", "/assets/js/ckeditor12/kcfinder/upload.php", "/apps/kcfinder/upload.php", "/apps/js/kcfinder/upload.php", "/include/libs/kcfinder-2.54/upload.php", "/vendors/kcfinder/upload.php", "/vendors/js/kcfinder/upload.php", "/ThirdParty/kcfinder/upload.php", "/themes/default/assets/plugins/kcfinder/upload.php
    # Add the rest of your paths here...
]

def rfm(url):
    s = requests.Session()
    pala = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 9 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    for i in rfmlist:
        try:
            r = s.get(f'http://{url}{i}', timeout=7, verify=False, headers=pala)
            if 'alert("Unknown error");' in r.text or "alert('Unknown error');" in r.text:
                print(f'{Fore.YELLOW}[{Fore.WHITE}FOUND{Fore.YELLOW}] {url}{i}')
                with open('result_kcfinder.txt', 'a+') as f:
                    f.write(f'http://{url}{i}\n')
                return True
            else:
                print(f'{Fore.YELLOW}[{Fore.WHITE}NOT FOUND{Fore.YELLOW}] {url}{i}')
        except Exception as e:
            print(f'Error: {e}')

def main(filename, thread_count):
    print("KCFinder Mass Scanner Mass Path")
    with open(filename) as f:
        asu = f.read().splitlines()
    p = Pool(thread_count)
    p.map(rfm, asu)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KCFinder Mass Scanner")
    parser.add_argument("filename", type=str, help="File containing list of websites")
    parser.add_argument("thread_count", type=int, help="Number of threads to use")
    args = parser.parse_args()

    main(args.filename, args.thread_count)