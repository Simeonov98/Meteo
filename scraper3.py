from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
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

driver = webdriver.Chrome("./chromedriver", options=options,)
driver.get(
    "https://www.sinoptik.bg/plovdiv-bulgaria-100728193/10-days/"
)
today = date.today()
d1 = today.strftime("%d/%m/%Y") # dd/mm/YY

days=driver.find_element(By.CLASS_NAME,'wf10dayRightContent')
day=days.find_elements(By.TAG_NAME,'a')
# print(len(day))
# print('stigame do tuk')
# windspdddd=day[0].find_element(By.CLASS_NAME,'wf10dayRightWind')
# print(windspdddd.text)
# rain=day[0].find_elements(locate_with(By.TAG_NAME,'span').near(windspdddd))
# print("2nd checkpoint")
# print(rain.text)
for i in range(0,9):
    dayoftheweek.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightDay').text)
    exdate.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightDate').text)
    tmax.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightTemp').text)
    tmin.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightTempLow').text)
    winddir.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightWind').get_attribute('title'))
    windspd.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightWind').text)
    # rainchance.append(day[i].find_element(By.XPATH,'//*[@id="wf10day"]/div[2]/a[1]/span[7]').get_attribute('text'))
    print(exdate[i],dayoftheweek[i],tmax[i],tmin[i],winddir[i],windspd[i])