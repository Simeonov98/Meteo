from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date, timedelta
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--headless")
row=[]
dayoftheweek=[]
exdate=[]
tmax=[]
tmin=[]
windspd=[]
winddir=[]
rainchance=[]
rainvolume=[]
cloud=[]
sunrise=[]
sundown=[]
daylen=[]
verbal=[]
humidity=[]

driver = webdriver.Chrome("./chromedriver", options=options,)
driver.get(
    "https://www.dalivali.bg/?type=daily&location=173"
)
today = date.today()
d1 = today.strftime("%d/%m/%Y") # dd/mm/YY
print(d1)
days=driver.find_element(By.CLASS_NAME,'slick-track')
day=days.find_elements(By.CLASS_NAME,'slick-slide')

print(len(day))
for i in range(0,9):
    dayoftheweek.append(day[i].find_element(By.ID,'title-day1').get_attribute('innerText'))
    exdate.append(day[i].find_element(By.ID,'date1').get_attribute('innerText'))
    tmax.append(day[i].find_element(By.ID,'tNday1').get_attribute('innerText'))
    tmin.append(day[i].find_element(By.ID,'tDday1').get_attribute('innerText'))
    windspd.append(day[i].find_element(By.ID,'info-num-Spwind1').get_attribute('innerText'))
    winddir.append(day[i].find_element(By.ID,'info-num-wind1').get_attribute('innerText'))
    humidity.append(day[i].find_element(By.ID,'info-num-rain1').get_attribute('innerText'))
    verbal.append(day[i].find_element(By.ID,'descr-day1').get_attribute('innerText'))
    
    print(dayoftheweek[i],exdate[i],tmax[i],tmin[i],windspd[i],winddir[i],humidity[i],verbal[i])
