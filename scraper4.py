from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import date, datetime


options = Options()
options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(
     "https://www.dalivali.bg/?type=daily&location=173"
)

row,dayoftheweek,exdate,tmax,tmin,windspd,winddir,rainchance,rainvolume,cloud,sunrise,sundown,daylen,verbal,humidity,image = ( [] for i in range(16))

today = date.today().strftime("%d/%m/%Y") # dd/mm/YY
print('Todays date is ' + today)
hourMinute = datetime.now()
print(str(hourMinute.hour)+':'+str(hourMinute.minute))

days = driver.find_element(By.CLASS_NAME,'slick-track')
day = days.find_elements(By.CLASS_NAME,'slick-slide')

print(str(len(day))+' days are visible from www.dalivali.bg in the city of Plovdiv')
print('DayOfTheWeek'.ljust(10), ' ','Date'.ljust(10), ' ', 'MinTemp'.ljust(10), ' ', 'MaxTemp'.ljust(10), ' ',
 'WindSpeed'.ljust(10), ' ', 'WindDir'.ljust(10), ' ', 'Humidity'.ljust(10), ' ', 'Decription'.ljust(10), ' ' )

for i in range(0,9):
    dayoftheweek.append(day[i].find_element(By.ID,'title-day1').get_attribute('innerText'))
    exdate.append(day[i].find_element(By.ID,'date1').get_attribute('innerText'))
    tmax.append(day[i].find_element(By.ID,'tNday1').get_attribute('innerText'))
    tmin.append(day[i].find_element(By.ID,'tDday1').get_attribute('innerText'))
    windspd.append(day[i].find_element(By.ID,'info-num-Spwind1').get_attribute('innerText'))
    winddir.append(day[i].find_element(By.ID,'info-num-wind1').get_attribute('innerText'))
    humidity.append(day[i].find_element(By.ID,'info-num-rain1').get_attribute('innerText'))
    verbal.append(day[i].find_element(By.ID,'descr-day1').get_attribute('innerText'))
    #image.append(day[i].find_element(By.ID,'icon-next2').screenshot('./dali'+str(exdate[i])+'.png'))
    image.append(day[i].find_element(By.ID,'icon-next2').get_attribute('src'))
    #image[i].screenshot('./dali/dali'+str(exdate[i])+' '+str(hourMinute.hour)+':'+str(hourMinute.minute)+'.png')

for i in range(0,9):    
    print(image[i])
    print(dayoftheweek[i].ljust(11), ' ',exdate[i].ljust(11), ' ', tmax[i].ljust(11), ' ', tmin[i].ljust(11), ' ',
     windspd[i].ljust(11), ' ', winddir[i].ljust(11), ' ', humidity[i].ljust(11), ' ', verbal[i].ljust(11), ' ' )