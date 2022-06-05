#!/usr/bin/env python3
# Build by Kat

import json
import nmap
from IPy import IP
import os
from threadPool import ThreadPool

logo = '''
                  _____                 
                 / ____|                
 _ __ ___  _ __ | (___   ___ __ _ _ __  
| '_ ` _ \| '_ \ \___ \ / __/ _` | '_ \ 
| | | | | | | | |____) | (_| (_| | | | |
|_| |_| |_|_| |_|_____/ \___\__,_|_| |_|Kat_v1.0
'''


# 根据输入IP格式生成扫描IP列表
def get_ip_list(ip):
    print(ip)
    ip_list_tmp = []

    def iptonum(x):
        return sum([256 ** j * int(i)
                    for j, i in enumerate(x.split('.')[::-1])])

    def numtoip(x):
        return '.'.join(
            [str(int(x / (256 ** i) % 256)) for i in range(0, -1, -1)])

    # 兼容IP范围
    if '-' in ip:
        ip_range = ip[ip.rfind('.') + 1:].split('-')
        ip_start = iptonum(ip_range[0])
        ip_end = iptonum(ip_range[1])
        ip_count = ip_end - ip_start
        if ip_count >= 0 and ip_count <= 255:
            for ip_num in range(ip_start, ip_end + 1):
                ip_list_tmp.append(ip[:ip.rfind('.')] + '.' + numtoip(ip_num))
        else:
            print('IP format error' + ip)
    # 兼容IP段
    elif '/' in ip:
        ip = IP(ip, make_net=1)
        for i in ip:
            ip_list_tmp.append(i)
    # 兼容单个IP格式
    else:
        ip_split = ip.split('.')
        net = len(ip_split)
        if net == 2:
            for b in range(1, 255):
                for c in range(1, 255):
                    ip = "%s.%s.%d.%d" % (ip_split[0], ip_split[1], b, c)
                    ip_list_tmp.append(ip)
        elif net == 3:
            for c in range(1, 255):
                ip = "%s.%s.%s.%d" % (
                    ip_split[0], ip_split[1], ip_split[2], c)
                ip_list_tmp.append(ip)
        elif net == 4:
            ip_list_tmp.append(ip)
        else:
            print("IP format error" + ip)
    return ip_list_tmp



# 调用masscan
def portscan():
    ports = []
    print('masscan -iL scan_ip.txt -p 1-65535 -oJ masscan.json --rate 1000')
    os.system('masscan -iL scan_ip.txt -p 1-65535 -oJ masscan.json --rate 1000')
    # 提取json文件中的端口
    with open('masscan.json', 'r+') as f:
        for line in f:
            if line.startswith('{ '):
                temp = json.loads(line)
                temp1 = temp["ports"][0]
                ports.append(str(temp1["port"]) + '|' + temp["ip"])
    return ports


# 调用nmap识别服务
def NmapScan(scan_ip_port, data):
    nm = nmap.PortScanner()
    try:
        scan_ip_port = scan_ip_port.split('|')
        ret = nm.scan(scan_ip_port[1], scan_ip_port[0], arguments='-Pn,-sV')
        service_name = ret['scan'][scan_ip_port[1]]['tcp'][int(scan_ip_port[0])]['name']
        print('[*]主机 ' + scan_ip_port[1] + ' 的 ' + str(scan_ip_port[0]) + ' 端口服务为：' + service_name)
        with open('nmap_result.txt', 'a+') as f:
            f.write(scan_ip_port[1]+':'+ scan_ip_port[0] + ':' + service_name + '\n')
        with open('result.txt', 'a+') as f:
            f.write('http://' + scan_ip_port[1] + ':' + scan_ip_port[0] + '\n')
    except Exception as e:
        print(e)
        pass

def main():
    try:
        with open('ip.txt','r') as f:
            ip = ''
            for line in f.readlines():
                final_ip = line.strip('\n')
                for i in get_ip_list(final_ip):
                    # print(i)
                    ip += str(i).strip() + '\n'
        with open('scan_ip.txt', 'w+') as ff:
            ff.write(ip)
        items = portscan()  # 进行masscan跑端口
        dataList = {}
        for i in items:
            i = i.split('|')
            if i[1] not in dataList:
                dataList[str(i[1])] = []
            dataList[str(i[1])].append(i[0])
        for i in dataList:
            if len(dataList[i]) >= 50:
                for port in dataList[i]:
                    items.remove(str(port) + '|' + str(i))  # 删除超过50个端口的
        data = []
        pool = ThreadPool(20, 1000)
        pool.start(NmapScan, items, data, )
    except Exception as e:
        print(e)
        print('Ip.Txt A Certain Line Format Error')
        pass

if __name__ == '__main__':
    print(logo)
    main()
