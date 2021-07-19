import threading 
import struct
import json
import time
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import tkinter.messagebox

window = tk.Tk()

window.title("网络通自动登录")
window.geometry("300x115")

#构建框架
frame=tk.Frame(window)
frame.pack()

frame_l=tk.Frame(frame)
frame_r=tk.Frame(frame)
frame_l.pack(side='left')
frame_r.pack(side='right')

# 左侧标签
tk.Label(frame_l,text="用户名：").pack()
tk.Label(frame_l,text="密码：").pack()
tk.Label(frame_l,text="刷新间隔：").pack()
tk.Label(frame_l,text="记住密码：").pack()

#读取预设文件
try:
    #获取账号密码存储格式信息
    f=open('config1',mode='rb')
    format=f.read()
    f.close()
    
    #解码出账号、刷新间隔、记住密码、密码
    pack_struct=struct.Struct(format)
    f=open('config2',mode='rb')
    packed_data=f.read()
    unpacked_data=pack_struct.unpack(packed_data)
    my_id=unpacked_data[0].decode()#存储用户名
    my_interval=unpacked_data[1]#存储刷新间隔
    my_remember=unpacked_data[2]#存储记住密码的选项
    my_password=unpacked_data[3].decode()#存储密码
    f.close()
except:
    #文件不存在时，open将抛出异常。这里设置其默认值
    my_id=''
    my_interval=60
    my_remember=False
    my_password=''


# 右侧输入框
var_id = tk.StringVar()#用户名输入框获取变量
var_id.set(my_id)
entry_id=tk.Entry(frame_r,textvariable=var_id)#用户名输入框句柄

var_password = tk.StringVar()#密码输入框获取变量
var_password.set(my_password)
entry_password=tk.Entry(frame_r,textvariable=var_password,show='*')#密码输入框句柄

var_interval = tk.StringVar()#刷新间隔输入框获取变量
var_interval.set(str(my_interval))#注意数字和字符串的转换与检查
frame_interval=tk.Frame(frame_r)#刷新间隔输入框容器
entry_interval=tk.Entry(frame_interval,textvariable=var_interval,width=16)#刷新间隔输入框句柄
lable_min=tk.Label(frame_interval,text="min")

#放置控件
entry_id.pack()
entry_password.pack()
frame_interval.pack()
entry_interval.pack(side="left")
lable_min.pack(side="right")

# 记住密码复选框
frame_remember=tk.Frame(frame_r)
frame_remember.pack()
var_remember = tk.BooleanVar()
var_remember.set(my_remember)
#checkbut_remember=tk.Checkbutton(frame_remember,variable=var_remember,onvalue=1,offvalue=0,state=var_state)
checkbut_remember=tk.Checkbutton(frame_remember,variable=var_remember)
#checkbut_remember.select()
tk.Label(frame_remember,width=17).pack(side='right')
checkbut_remember.pack(side='left')

# 开始/停止按钮
button_text=tk.StringVar()
button_text.set('开始')
do_flag = 0

def fun_start():
    global button_text
    global do_flag
    global my_id
    global my_interval
    global my_remember
    global my_password
    global entry_id
    global entry_interval
    global checkbut_remember
    global entry_password

    if button_text.get() == '开始':
        #屏蔽输入
        entry_id['state']=DISABLED
        entry_interval['state']=DISABLED
        checkbut_remember['state']=DISABLED
        entry_password['state']=DISABLED
        
        try:
            #检查并获取刷新时间间隔输入
            my_interval=int(var_interval.get().strip())
            if my_interval<1:
                raise ValueError
        except:
            #刷新时间间隔输入非法，弹出警告，去掉输入屏蔽
            tk.messagebox.showerror(title='错误!', message='刷新时间间隔输入应为正整数！\n请检查刷新时间间隔输入！')
            entry_id['state']=NORMAL
            entry_interval['state']=NORMAL
            checkbut_remember['state']=NORMAL
            entry_password['state']=NORMAL
        else:
            #刷新时间间隔输入合法，获取其他输入
            my_id=var_id.get()
            my_remember=var_remember.get()
            my_password=var_password.get()

            #存储设置文件
            if my_remember:#记住密码，打包生成二进制数据packed_data
                format=b'%dsi?%ds'%(len(my_id),len(my_password))
                pack_struct=struct.Struct(format)
                packed_data=pack_struct.pack(my_id.encode(),my_interval,my_remember,my_password.encode())
            else :#不记住密码，打包生成二进制数据packed_data
                format=b'%dsi?0s'%(len(my_id))
                pack_struct=struct.Struct(format)
                packed_data=pack_struct.pack(my_id.encode(),my_interval,my_remember,b'')
            #存储格式数据format和二进制数据packed_data
            f=open('config1',mode='wb')
            f.write(format)
            f.close()
            f=open('config2',mode='wb')
            f.write(packed_data)
            f.close()

            #发出执行指令
            do_flag=1
            button_text.set('停止')
        
    else :
        do_flag=0
        button_text.set('开始')
        entry_id['state']=NORMAL
        entry_interval['state']=NORMAL
        checkbut_remember['state']=NORMAL
        entry_password['state']=NORMAL
        

button=tk.Button(window,textvariable=button_text,width=20,command=fun_start)
button.pack()

end_flag=False
def wlt_AutoLogin():
    global do_flag
    global end_flag
    global i
    global test_int
    while not end_flag:
        try:
            if do_flag:
                n=my_interval*60
                #Open browser. Open website. Then check the current url.
                option=webdriver.FirefoxOptions()
                option.add_argument('--headless') # 设置option,使得浏览器在后台运行
                driver = webdriver.Firefox(executable_path="geckodriver.exe",options=option)
                driver.get("http://wlt.ustc.edu.cn/")

                #Login
                WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.NAME, "go")))
                try:
                    driver.find_element(By.NAME, "name").send_keys(my_id)
                    driver.find_element(By.NAME, "password").send_keys(my_password)
                    driver.find_element(By.NAME, "go").click()
                except:
                    pass

                #Choose an export port
                WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.NAME, "setdefault")))
                driver.find_element(By.ID, "t5").click()
                driver.find_element(By.NAME, "go").click()
                
                #Wait and close the browser.
                time.sleep(2)
                driver.close()

                #Wait [my_interval] min
                while(n>0 and (not end_flag) and do_flag):#If end flag =True, stop waiting.
                    time.sleep(0.99)
                    n-=1
        except:
            tk.messagebox.showerror(title='错误!', message='登陆超时！\n可能为用户名、密码错误或者网络问题。')
            driver.close()
            if do_flag:
                button.invoke()           

th_fun=threading.Thread(target=wlt_AutoLogin)
th_fun.start()
window.mainloop()

end_flag=True
th_fun.join()
