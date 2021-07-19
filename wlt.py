import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#Open id.txt. Get id & password
idfile = open('id.txt',)
_id = idfile.readline()
_password = idfile.readline()
idfile.close()

#Open browser. Open website. Then check the current url.
option=webdriver.FirefoxOptions()
option.add_argument('--headless') # 设置option
driver = webdriver.Firefox(executable_path="geckodriver.exe",options=option)
driver.get("http://wlt.ustc.edu.cn/")

#Login
WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.NAME, "go")))
try:
    driver.find_element(By.NAME, "name").send_keys(_id)
    driver.find_element(By.NAME, "password").send_keys(_password)
    driver.find_element(By.NAME, "go").click()
except:
    pass

#Choose an export port
WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.NAME, "setdefault")))
driver.find_element(By.ID, "t5").click()
driver.find_element(By.NAME, "go").click()

time.sleep(2)
driver.close()