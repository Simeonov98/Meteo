from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import os,db3
from functools import reduce
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

#https://dalivali.bg/?location=173

from datetime import datetime, timedelta

def get_weekday_datetime(day_name):
    weekdays = ["Понеделник", "Вторник", "Сряда", "Четвъртък", "Петък", "Събота", "Неделя"]
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    days_mapping = {day: i for i, day in enumerate(weekdays)}
    days_mapping["Днес"] = today.weekday()
    days_mapping["Утре"] = (today.weekday() + 1) % 7

    target_weekday = days_mapping.get(day_name, None)
    if target_weekday is None:
        return None  # Invalid input

    # Calculate the difference between today and the target weekday
    days_difference = (target_weekday - today.weekday()) % 7
    target_date = today + timedelta(days=days_difference)

    # Return the datetime object
    return target_date




#converts the day name to a number
def get_weekday_number(day_name):
    weekdays = ["Понеделник", "Вторник", "Сряда", "Четвъртък", "Петък", "Събота", "Неделя"]
    
    today = datetime.now().weekday()  # 0 is monday, 6 is sunday
    
    days_mapping = {day: i for i, day in enumerate(weekdays)}   # { "Понеделник": 0, "Вторник": 1, ... }
    days_mapping["Днес"] = today
    days_mapping["Утре"] = (today + 1) % 7  # if today is sunday (6), tomorrow will be monday (0)
    
    # if day_name is not in the mapping, return None
    return days_mapping.get(day_name, None)

#loads the driver
def loadDriver(url):
    options=FirefoxOptions();
    options.add_argument("--headless");
    driver=webdriver.Firefox(options=options,service=FirefoxService(executable_path=GeckoDriverManager().install()));   
    driver.get(url);
    return driver;

#runs the script
def run(url,cId):
    driver=loadDriver(url);

    row,dayoftheweek,exdate,tmax,tmin,windspd,winddir,rainchance,rainvolume,cloud,sunrise,sundown,daylen,verbal,humidity,img,image,forecastDate =( [] for i in range(18))
    forecastDbStr=[]
   
    hourMinute = datetime.now()
    print(str(hourMinute.hour)+":"+str(hourMinute.minute))
    buttonAccept = driver.find_element(By.CSS_SELECTOR, ".fc-cta-consent");
    buttonAccept.click();
<<<<<<< HEAD
    buttonForecast10 = driver.find_element(By.CSS_SELECTOR, "#content_router > div.global-dalivali > div:nth-child(1) > div:nth-child(2) > div > div.city-weather-content > div.forecast-wrap > div.forecast-box.box-daily");
=======
    driver.implicitly_wait(2)
    buttonForecast10 = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div[2]/div/div[2]/div[3]/div[2]");
>>>>>>> 4f25b3d (implicit wait on dalivali2)
    
    #buttonForecast10.click();
    forecast_rows = buttonForecast10.find_elements(By.CLASS_NAME, "row")

    #print(f"Found {len(forecast_rows)} rows")
    

    #extracts the data from the page
    for i, row in enumerate(forecast_rows[2:]):
        if i>=7:
            break;
        # dayoftheweek.append(row.text.split()[0])
        dayoftheweek.append(row.find_element(By.CLASS_NAME,'day').get_attribute('innerText').split()[0])
        tmin.append(row.find_element(By.CLASS_NAME,'info-data').find_element(By.ID,'temp-today').get_attribute('innerText').split()[0])
        # print(dayoftheweek[i],tmin[i])
        # break
        tmax.append(row.find_element(By.CLASS_NAME,'info-data').find_element(By.ID,'temp-today').get_attribute('innerText').split()[2])
        windspd.append(row.find_element(By.CLASS_NAME,'info-data').find_element(By.ID,'wind-today').get_attribute('innerText')+' m/s')
        winddir.append(row.find_element(By.CLASS_NAME,'info-data').find_element(By.ID,'dr-today').get_attribute('innerText').split())
        humidity.append(row.find_element(By.CLASS_NAME,'info-data').find_element(By.ID,'rain-today').get_attribute('innerText'))
        #print(f"Row {i}: {row.text.split()[0]},windspd: {row.find_element(By.CLASS_NAME,'info-data').find_element(By.ID,'wind-today').get_attribute('innerText')+' м/с'},winddir: {row.find_element(By.CLASS_NAME,'info-data').find_element(By.ID,'dr-today').get_attribute('innerText').split()},tmin: {row.find_element(By.CLASS_NAME,'info-data').find_element(By.ID,'temp-today').get_attribute('innerText').split()[0]},tmax: {row.find_element(By.CLASS_NAME,'info-data').find_element(By.ID,'temp-today').get_attribute('innerText').split()[2]},humidity: {row.find_element(By.CLASS_NAME,'info-data').find_element(By.ID,'rain-today').get_attribute('innerText')}")
        forecastDbStr.append(f"""INSERT INTO "Dalivali" ("forecastDay", weekday, tmax, tmin, wspd, wdir, humidity, "cityId") VALUES ('{get_weekday_datetime(dayoftheweek[i])}','{get_weekday_number(dayoftheweek[i])}','{tmax[i]}','{tmin[i]}','{windspd[i]}','{winddir[i][0]}','{humidity[i]}','{cId}');""")
        # break;
    # print(forecastDbStr)
    
    #pushes the data to the database
    for i in range(len(forecastDbStr)):
        db3.push(forecastDbStr[i]);
        print('success '+str(i));
    driver.quit()

