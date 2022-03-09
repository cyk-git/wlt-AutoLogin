import urllib.request
import time
import os
import argparse
import sys
import getpass
import re

# 输入参数
parser = argparse.ArgumentParser(description='USTC wlt auto login script.')
parser.add_argument('-u','--username', help='your wlt username', type=str, default="None")
parser.add_argument('-p','--password', help='your wlt password', type=str, default="None")
parser.add_argument('-t','--type', help='Internet export', type=int, default=0)
args = parser.parse_args()

username = args.username
password = args.password
type = args.type

print("\n")
print("+------------------------------------------------------------------------+")
print("|                             网络通自动登录                             |")
print("+------------------------------------------------------------------------+")

# 如果输入参数有误，重新选择出口
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

# 检查用户名密码正确性, 如果有误，重新输入
while(1):
    data = {'name':username, 'password' : password,'cmd' : 'set', 'type' : type, 'exp' : '0'}
    url = "http://wlt.ustc.edu.cn/cgi-bin/ip"
    data = urllib.parse.urlencode(data).encode('utf8')
    request=urllib.request.Request(url, data)
    reponse=urllib.request.urlopen(request).read()
    reponse_txt=reponse.decode('gb2312')
    if(len(reponse_txt)>1000):
        print("\033[1;32;40mLogin Succeed!\033[0m")
        break
    else:
        print("\033[1;31;43m")
        print("Login Failed!")
        print(re.search("信息：<.*>(.*)<.*>",reponse_txt).group(1))
        print("\033[0m\n")
        username=input("Please enter your wlt username:")
        password=getpass.getpass("(No echo on the screen) Please enter your password:")

system_type=sys.platform
if system_type == "linux":
    ping_cmd = "ping www.baidu.com -i 1 -w 3"
elif system_type == "win32":
    ping_cmd = "ping www.baidu.com"
else:
    print("\033[1;31;43mUnknown system.\033[0m")
    exit()

while 1:
    try:
        exit_code = os.system(ping_cmd)
        if exit_code:
            data = {'name': username, 'password' : password,'cmd' : 'set', 'type' : type, 'exp' : '0'}
            url = "http://wlt.ustc.edu.cn/cgi-bin/ip"
            data = urllib.parse.urlencode(data).encode('utf8')
            request=urllib.request.Request(url, data)
            reponse=urllib.request.urlopen(request).read()
            print("\033[1;32;40mLogin Succeed!\033[0m")
    except Exception:
        print("\033[1;31;43mLogin Failed!\033[0m")
    finally:
        time.sleep(1)
