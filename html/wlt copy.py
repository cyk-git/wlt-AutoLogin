import urllib.request
import time
import os

data = {'username':'PB18020691', 'password' : '*********'} 
url = "https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin"
print(url)
data = urllib.parse.urlencode(data).encode('utf8')
request=urllib.request.Request(url, data)
reponse=urllib.request.urlopen(request).read()
fh = open("./jkdk.html","wb")    # 将文件写入到当前目录中
fh.write(reponse)
fh.close()
