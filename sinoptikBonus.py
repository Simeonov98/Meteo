from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import sys
from selenium.webdriver.common.by import By
from datetime import date, datetime
def pumiq():
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--headless")
    row=[]
    
    verbal=[]
    image=[]
    url="https://www.sinoptik.bg/plovdiv-bulgaria-100728193/10-days/"
    driver = webdriver.Chrome("./chromedriver", options=options,)
    #driver.get(url)
    today = date.today()
    d1 = today.strftime("%d/%m/%Y") # dd/mm/YY
    

    
    for i in range(0,9):
        driver.get(url+str(i))
        verbal.append(driver.find_element(By.CLASS_NAME,'wf10daysNotFullRC').find_element(By.TAG_NAME,'strong').text)
    
    return verbal

    