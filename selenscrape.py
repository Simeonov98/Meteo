from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(".\chromedriver.exe")
driver.get(
    "https://weather.com/weather/tenday/l/dd44ead62bb77ca2b236bca92f752cac528e0114d5f41d1f1c0921136b603e09?unit=m"
)


maxt=driver.find_elements(By.CLASS_NAME,'DetailsSummary--highTempValue--3Oteu')
mint=driver.find_elements(By.CLASS_NAME, 'DetailsSummary--lowTempValue--3H-7I')
percip=driver.find_elements(By.CLASS_NAME,'DetailsSummary--precip--1ecIJ')
verbal=driver.find_elements(By.CLASS_NAME,'DetailsSummary--extendedData--365A_')

text=verbal[::2]
wind=verbal[1::2]
print("The variable text[0].get_attribute('innerText')", type(text[0].get_attribute('innerText')))

for x in range(0,14):
    print("max temp is " + maxt[x].get_attribute("innerText")
     + ', min temp is '+mint[x].get_attribute("innerText")
     +' the weather is '+ text[x].get_attribute("innerText") 
     +' the chance of rain is '+percip[x].get_attribute("innerText")
     +' the wind direction and speed is '+wind[x].get_attribute("innerText").lstrip("Wind"))


# image=[]
# image = driver.find_elements(By.TAG_NAME, "svg")
# image[0].screenshot("./image.png")

image=[]
image = driver.find_elements(By.TAG_NAME,'By.TAG_NAME, "svg"')
for i in range(0, len(image)):
    image[i].screenshot("./image"+str(i)+".png")


# imgarr=[]
# for i in range(0,14):
#     imgarr.append(driver.find_elements(By.CSS_SELECTOR,'#detailIndex1 > summary > div > div > div.DetailsSummary--condition--24gQw > svg'))
# imgarr[0].screenshot("./img1.png") 

# for i in range(0,13):
#     imgarr[i].screenshot("./img"+str(i)+".png")    
driver.close()