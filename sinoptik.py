from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import date, datetime
import db


options = Options()
options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
url="https://www.sinoptik.bg/plovdiv-bulgaria-100728193/10-days/"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(
     "https://www.sinoptik.bg/plovdiv-bulgaria-100728193/10-days/"
)



verbal=[]
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
image=[]
forecastDate=[]
dbstr=[]

today = date.today()
d1 = today.strftime("%d/%m/%Y") # dd/mm/YY

days=driver.find_element(By.CLASS_NAME,'wf10dayRightContent')
day=days.find_elements(By.TAG_NAME,'a')

for i in range(0,9):
    dayoftheweek.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightDay').text)
    exdate.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightDate').text)
    tmax.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightTemp').text)
    tmin.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightTempLow').text)
    winddir.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightWind').get_attribute('title'))
    windspd.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightWind').text)
    verbal.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightImg').get_attribute('title'))
    image.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightImg'))
    dates=exdate[i].split('.')
    forecastDate.append(datetime(datetime.now().year,int(dates[1]),int(dates[0])))
    image[i].screenshot('./sinoptik/forDate '+str(exdate[i])+' takenAt '+str(datetime.now()).replace(".",":")+'.png')
    print(str(i),forecastDate[i],forecastDate[i].weekday(),tmax[i].rstrip('°'),tmin[i].rstrip('°'),winddir[i],windspd[i],verbal[i])

    #print(str(i),forecastDate[i], forecastDate[i].weekday())
#print(forecastDate)