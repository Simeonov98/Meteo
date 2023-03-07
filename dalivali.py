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
drvr=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(
     "https://www.dalivali.bg/?type=daily&location=173"
)

row,dayoftheweek,exdate,tmax,tmin,windspd,winddir,rainchance,rainvolume,cloud,sunrise,sundown,daylen,verbal,humidity,img,image,forecastDate = ( [] for i in range(18))

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
    tmax.append(day[i].find_element(By.ID,'tDday1').get_attribute('innerText'))
    tmin.append(day[i].find_element(By.ID,'tNday1').get_attribute('innerText'))
    windspd.append(day[i].find_element(By.ID,'info-num-Spwind1').get_attribute('innerText'))
    winddir.append(day[i].find_element(By.ID,'info-num-wind1').get_attribute('innerText'))
    humidity.append(day[i].find_element(By.ID,'info-num-rain1').get_attribute('innerText'))
    verbal.append(day[i].find_element(By.ID,'descr-day1').get_attribute('innerText'))
    dates=exdate[i].split('.')
    forecastDate.append(datetime(int(dates[2]),int(dates[1]),int(dates[0])))

    img.append(day[i].find_element(By.ID,'icon-next2').get_attribute('src'))
 
    drvr.get(img[i])
    drvr.find_element(By.TAG_NAME,'svg').screenshot('./dalivali/forDate '+str(exdate[i])+' takenAt '+str(datetime.now()).replace(".",":")+'.png')
    # img[i].screenshot('./dalivali/forDate '+str(exdate[i])+' takenAt '+str(datetime.now()).replace(".",":")+'.png')
for i in range(0,9):    
    #print(image[i])
    #print(dayoftheweek[i].ljust(11), ' ',exdate[i].ljust(11), ' ', tmax[i].ljust(11), ' ', tmin[i].ljust(11), ' ',
     #windspd[i].ljust(11), ' ', winddir[i].ljust(11), ' ', humidity[i].ljust(11), ' ', verbal[i].ljust(11), ' ' )
    print(forecastDate[i],forecastDate[i].weekday(),tmax[i].rstrip('°'),tmin[i].rstrip('°'),windspd[i].rstrip(' м/с')+' m/s',winddir[i],humidity[i].rstrip('%'),verbal[i])
    