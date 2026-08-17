from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import date, datetime
import db,os,hash,operator

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Function to convert number into string
# Switcher is dictionary data type here
def numbers_to_strings(argument):
    switcher = {
        'яну': 1,
        'фев': 2,
        'мар': 3,
        'апр': 4,
        'май': 5,
        'юни': 6,
        'юли': 7,
        'авг': 8,
        'сеп': 9,
        'окт': 10,
        'ное': 11,
        'дек': 12,

    }
 
    # get() method of dictionary data type returns
    # value of passed argument if it is present
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
    return switcher.get(argument, "nothing")
 
# Driver program
# if __name__ == "__main__":
#     argument=0
#     print (numbers_to_strings(argument))


# options = Options()
# options.add_argument('--headless=new')
# options.add_experimental_option("excludeSwitches", ["enable-logging"])




options = FirefoxOptions()
options.add_argument("--headless")





driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)


#  driver = webdriver.Firefox()
driver.get(
    "https://freemeteo.bg/weather/plovdiv/7-days/list/?gid=728193&language=bulgarian&country=bulgaria"
)
day=driver.find_elements(By.CLASS_NAME,'day')
# for i in range(0,7):
     # print(day[i].find_element(By.CLASS_NAME,'icon').find_element(By.TAG_NAME,'span').get_attribute('class'))
db.insertBLOB('4e102a5bf2351b352d823be868214b84','/home/simeon/programming/Meteo/freemeteo/4e102a5bf2351b352d823be868214b84.png')