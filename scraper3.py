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

driver = webdriver.Chrome(".\chromedriver.exe", options=options,)
driver.get(
    "https://www.sinoptik.bg/plovdiv-bulgaria-100728193/10-days/"
)
today = date.today()
d1 = today.strftime("%d/%m/%Y") # dd/mm/YY

days=driver.find_element(By.CLASS_NAME,'wf10dayRightContent')
day=days.find_elements(By.TAG_NAME,'a')
# print(len(day))
print(day[0].find_element(By.XPATH,'/html/body/div[2]/div[2]/div[3]/div[2]/div/div/div[2]/a[1]/span[7]').text)
for i in range(0,9):
    dayoftheweek.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightDay').text)
    exdate.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightDate').text)
    tmax.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightTemp').text)
    tmin.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightTempLow').text)
    winddir.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightWind').get_attribute('title'))
    windspd.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightWind').text)
    rainchance.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightRainValue').text)