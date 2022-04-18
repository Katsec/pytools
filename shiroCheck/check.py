#!/usr/bin/env python3
# Build by Kat

import subprocess
import threadpool
import sys
import argparse

logo = '''

   ______   _          _______           __
  / __/ /  (_)______  / ___/ /  ___ ____/ /__
 _\ \/ _ \/ / __/ _ \/ /__/ _ \/ -_) __/  '_/
/___/_//_/_/_/  \___/\___/_//_/\__/\__/_/\_\_Kat_v1.0

'''


def wirte_targets(vurl, filename):
    with open(filename, "a+") as f:
        f.write(vurl + "\n" + '-----------' + '\n')
        return vurl

def wirte_key(key, filename):
    with open(filename, "a+") as f:
        f.write(key + "\n")
        return key

# def multithreading(funcname, filename="url.txt", pools=5):
#     works = []
#     with open(filename, "r") as f:
#         for i in f:
#             func_params = [i.rstrip("\n")]
#             works.append((func_params, None))
#     pool = threadpool.ThreadPool(pools)
#     reqs = threadpool.makeRequests(funcname, works)
#     [pool.putRequest(req) for req in reqs]
#     pool.wait()




def exp(u):
    p = subprocess.Popen("java -jar shiro_tool.jar %s" % u
                         , stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)

    while True:
        out = p.stdout.readline().decode("gbk").strip()
        if out == '' and p.poll() != None :
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()
        if 'enter s to skip' in out:
            p.kill()
        if 'use shiro key' in out:
            wirte_key(out,'vuln.txt')
        if 'please enter the number' in out:
            print("[-] 发现存在漏洞！！！！")
            p.kill()
            wirte_targets(u, "vuln.txt")

    print('\n' + "[o] finish")

if __name__ == "__main__":
    print(logo)
    if (len(sys.argv)) < 2:
        print('useage : python' + str(sys.argv[0]) + ' -r url.txt')
    else:
        parser = argparse.ArgumentParser()
        parser.description = 'shiro批量检测'
        parser.add_argument('-r', help="url list to file", type=str, dest='check_file')
        args = parser.parse_args()
        if (args.check_file):
            with open('url.txt', 'r') as f:
                for line in f.readlines():
                    exp(line.strip())