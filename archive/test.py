from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import date, datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(
     "https://www.sinoptik.bg/plovdiv-bulgaria-100728193/10-days/"
)
image=[]

days=driver.find_element(By.CLASS_NAME,'wf10dayRightContent')
day=days.find_elements(By.TAG_NAME,'a')

for i in range(0,9):
    
    image.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightImg'))
    image[i].screenshot('./sinoptik/forDate  takenAt '+str(datetime.now()).replace(".",":")+'.png')
    print(str(i),image[i].text)