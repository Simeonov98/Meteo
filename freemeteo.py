from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import date, datetime


options = Options()
options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(
    "https://freemeteo.bg/weather/plovdiv/7-days/list/?gid=728193&language=bulgarian&country=bulgaria"
)
row=[]
day=driver.find_elements(By.CLASS_NAME,'day')
title=[]
image=[]
tmin=[]
tmax=[]
text=[]
wind=[]
rain=[]
#print(day[0].find_element(By.CLASS_NAME,'temps').find_elements(By.CSS_SELECTOR,'#content > div.right-col > div.weather-now > div.today.table > div > div > div:nth-child(2) > div.temps > b'))
# text=verbal[::2]


print(len(day))

print(str(datetime.now()).rsplit('.',1)[0])
for i in range(0,7):
    title.append(day[i].find_element(By.CLASS_NAME,'title').find_element(By.TAG_NAME,'span').get_attribute('innerText')) #reaching furhter into the dom (gotta transform text to datetime)
    try:
        tmax.append(day[i].find_element(By.CLASS_NAME,'temps').find_element(By.TAG_NAME,'b').get_attribute('innerText'))
    except NoSuchElementException:
        tmax.append('макс: N/A')
    tmin.append(day[i].find_element(By.CLASS_NAME,'temps').find_element(By.TAG_NAME,'span').get_attribute('innerText'))
    text.append(day[i].find_element(By.CLASS_NAME,'hover').find_element(By.CLASS_NAME,'info').find_element(By.CLASS_NAME,'extra').get_attribute('innerText'))
    wind.append((day[i].find_element(By.CLASS_NAME,'wind').find_element(By.TAG_NAME,'span').get_attribute('class')).rsplit(' ',1)[1])
    rain.append(day[i].find_element(By.CLASS_NAME,'extra').find_element(By.TAG_NAME,'b').text)
    image.append(day[i].find_element(By.CLASS_NAME,'icon').find_element(By.TAG_NAME,'span'))
    image[i].screenshot('/home/simeon/programming/Meteo/freemeteo/'+str(title[i])+' takenAt'+str(datetime.now()).replace(".",":")+'.png')
    # if len(tmax[i])==0:
    #     tmax[i].text="N/A"
 
    print(title[i],tmax[i],tmin[i],text[i],wind[i],rain[i]+' mm')
driver.close()
