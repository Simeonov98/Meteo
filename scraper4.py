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


driver = webdriver.Chrome("./chromedriver", options=options,)
driver.get(
    "https://www.dalivali.bg/?type=daily&location=173"
)
today = date.today()
d1 = today.strftime("%d/%m/%Y") # dd/mm/YY
print(d1)
days=driver.find_element(By.CLASS_NAME,'slick-track')
day=days.find_elements(By.CLASS_NAME,'slick-slide')
print(driver.find_element(By.ID,'title-day1').get_attribute("innerText"))
# print(day[0].find_element(By.TAG_NAME,'li').find_element(By.TAG_NAME,'div').find_element(By.ID,'title-day1').text)
# for i in range(0,9):
    # dayoftheweek.append(day[i].find_element(By.ID,'title-day1').text)
    # print(dayoftheweek[i])
