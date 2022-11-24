from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])

row=[]
driver = webdriver.Chrome(".\chromedriver.exe", options=options,)
driver.get(
    "https://freemeteo.bg/weather/plovdiv/7-days/list/?gid=728193&language=bulgarian&country=bulgaria"
)

# day=driver.find_elements(By.CSS_SELECTOR,'#content > div.right-col > div.weather-now > div.today.table > div > div > div:nth-child(1)')
day=driver.find_elements(By.CLASS_NAME,'day')
# maxt=driver.find_elements(By.CLASS_NAME,'DetailsSummary--highTempValue--3Oteu')
# mint=driver.find_elements(By.CLASS_NAME, 'DetailsSummary--lowTempValue--3H-7I')
# percip=driver.find_elements(By.CLASS_NAME,'DetailsSummary--precip--1ecIJ')
# verbal=driver.find_elements(By.CLASS_NAME,'DetailsSummary--extendedData--365A_')
title=[]
image=[]
tmin=[]
tmax=[]
text=[]
print(day[0].find_element(By.CLASS_NAME,'temps').find_elements(By.CSS_SELECTOR,'#content > div.right-col > div.weather-now > div.today.table > div > div > div:nth-child(2) > div.temps > b'))
# text=verbal[::2]
# wind=verbal[1::2]
for i in range(0,6):
    title.append(day[i].find_element(By.CLASS_NAME,'title').find_element(By.TAG_NAME,'span')) #reaching furhter into the dom (gotta transform text to datetime)
    tmax.append(day[i].find_element(By.CLASS_NAME,'temps').find_elements(By.CSS_SELECTOR,'#content > div.right-col > div.weather-now > div.today.table > div > div > div:nth-child(2) > div.temps > b'))
    tmin.append(day[i].find_element(By.CLASS_NAME,'temps').find_element(By.TAG_NAME,'span'))
    text.append(day[i].find_element(By.CLASS_NAME,'hover').find_element(By.CLASS_NAME,'info').find_element(By.CLASS_NAME,'extra'))
    image.append(day[i].find_element(By.CLASS_NAME,'icon').find_element(By.TAG_NAME,'span'))
    image[i].screenshot('./icon'+str(title[i].text)+'.png')
    if len(tmax[i])==0:
        tmax[i].text="N/A"
    print(title[i].text+', ')
    print(tmax[i].text+', ')
    print(tmin[i].text+', ')
    print(text[i].text)
print(title)

# for x in range(0,14):
#     print("max temp is " + maxt[x].text
#      + ', min temp is '+mint[x].text
#      +' the weather is '+ text[x].get_attribute("innerText") 
#      +' the chance of rain is '+percip[x].text
#      +' the wind direction and speed is '+wind[x].get_attribute("innerText").lstrip("Wind"))






# image = driver.find_element(By.CLASS_NAME, "DailyContent--Condition--bQKA2")
# image.screenshot("./image.png")
driver.close()
