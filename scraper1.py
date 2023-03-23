from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
url="https://www.sinoptik.bg/plovdiv-bulgaria-100728193/10-days/"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(
     "https://www.sinoptik.bg/plovdiv-bulgaria-100728193/10-days/"
)

days=driver.find_element(By.CLASS_NAME,'wf10dayRightContent')
day=days.find_elements(By.TAG_NAME,'a')