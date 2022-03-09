import urllib.request
import time
import os

while 1:
    try:
        exit_code = os.system("ping www.baidu.com")
        if exit_code:
            data = {'name':'******', 'password' : '******','cmd' : 'set', 'type' : '8', 'exp' : '0'} 
            url = "http://wlt.ustc.edu.cn/cgi-bin/ip"
            data = urllib.parse.urlencode(data).encode('utf8')
            request=urllib.request.Request(url, data)
            reponse=urllib.request.urlopen(request).read()
    except Exception:
        print("\nError!\n")
    finally:
        time.sleep(1)