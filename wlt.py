import urllib.request
import time
import os
import argparse
import sys


parser = argparse.ArgumentParser(description='USTC wlt auto login script.')
parser.add_argument('username', help='your wlt username', type=str)
parser.add_argument('password', help='your wlt password', type=str)
parser.add_argument('-t','--type', help='Internet export', type=int, default=0)
args = parser.parse_args()

type = args.type
if(type < 1 or type > 9):
    print("""\
    请选择出口：
            1: 教育网出口 (国际, 仅用教育网访问, 适合看文献)
            2: 电信网出口 (国际, 到教育网走教育网)
            3: 联通网出口 (国际, 到教育网走教育网)
            4: 电信网出口 2(国际, 到教育网免费地址走教育网)
            5: 联通网出口 2(国际, 到教育网免费地址走教育网)
            6: 电信网出口 3(国际, 到教育网走教育网, 到联通走联通)
            7: 联通网出口 3(国际, 到教育网走教育网, 到电信走电信)
            8: 教育网国际出口 (国际, 国内使用电信和联通, 国际使用教育网)
            9: 移动测试国际出口 (国际, 无 P2P 或带宽限制)
    注：选择出口 2、3 无法使用的某些电子资源，使用出口 4、5、6 可能可以正常使用""")
    while True:
        type = int(input("[1-9] "))
        if type >= 1 and type <= 9:
            type -= 1
            break

system_type=sys.platform
if system_type == "linux":
    ping_cmd = "ping www.baidu.com -i 1 -w 3"
elif system_type == "win32":
    ping_cmd = "ping www.baidu.com"
else:
    print("Unknown system.")
    exit()

while 1:
    try:
        exit_code = os.system(ping_cmd)
        if exit_code:
            data = {'name':args.username, 'password' : args.password,'cmd' : 'set', 'type' : type, 'exp' : '0'}
            url = "http://wlt.ustc.edu.cn/cgi-bin/ip"
            data = urllib.parse.urlencode(data).encode('utf8')
            request=urllib.request.Request(url, data)
            reponse=urllib.request.urlopen(request).read()
    except Exception:
        print("\033[1;31;43mLogin Failed!\033[0m")
    finally:
        time.sleep(1)