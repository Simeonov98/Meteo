from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import date, datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import hash,db,os,operator
from functools import reduce
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

def run(url):


    options = FirefoxOptions()    
    options.add_argument('--headless')
    #options.add_experimental_option("excludeSwitches", ["enable-logging"])
    drvr = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)

    #"https://www.dalivali.bg/?type=daily&location=173"
    driver.get(
         url
    )

    row,dayoftheweek,exdate,tmax,tmin,windspd,winddir,rainchance,rainvolume,cloud,sunrise,sundown,daylen,verbal,humidity,img,image,forecastDate = ( [] for i in range(18))
    forecastDbStr=[]
    imageDbStr=[]
    imgFollowLink=[]
    formatted=[]

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
        imgFollowLink.append(drvr.find_element(By.TAG_NAME,'svg'))
        temp_imgname='./dalivali/forDate '+str(exdate[i])+' takenAt '+str(datetime.now()).replace(".",":")+'.png'
        imgFollowLink[i].screenshot(temp_imgname)
        hashedImgName=hash.getHash(temp_imgname)
        if(os.path.exists('./dalivali/'+hashedImgName)==False):
            os.rename(temp_imgname,'./dalivali/'+hashedImgName+'.png')

        image_data = hash.convertToBinaryData('./dalivali/'+hashedImgName+'.png')
        imageDbStr.append(hashedImgName)

        forecastDbStr.append(f"INSERT INTO Dalivali (forecastDay, weekday, tmax, tmin, wspd, wdir, humidity, text, cityId, imageId) VALUES ('{forecastDate[i]}','{forecastDate[i].weekday()}','{tmax[i].rstrip('°')}','{tmin[i].rstrip('°')}','{windspd[i].rstrip(' м/с')+' m/s'}','{winddir[i]}','{humidity[i].rstrip('%')}','{verbal[i]}',{5},(SELECT id FROM Image WHERE name = '{hashedImgName}'))")

    imgResources=db.select("SELECT DISTINCT name FROM Image;")
    formatted.append(list(reduce(operator.concat,imgResources)))
    formatted=formatted.pop()
    for img in imageDbStr:
        if img not in formatted:
            db.insertBLOB(img,"/home/simeon/programming/Meteo/dalivali/"+img+".png")

        # img[i].screenshot('./dalivali/forDate '+str(exdate[i])+' takenAt '+str(datetime.now()).replace(".",":")+'.png')
    for i in range(0,9):    
        #print(image[i])
        #print(dayoftheweek[i].ljust(11), ' ',exdate[i].ljust(11), ' ', tmax[i].ljust(11), ' ', tmin[i].ljust(11), ' ',
         #windspd[i].ljust(11), ' ', winddir[i].ljust(11), ' ', humidity[i].ljust(11), ' ', verbal[i].ljust(11), ' ' )
        print(forecastDate[i],forecastDate[i].weekday(),tmax[i].rstrip('°'),tmin[i].rstrip('°'),windspd[i].rstrip(' м/с')+' m/s',winddir[i],humidity[i].rstrip('%'),verbal[i])
    for x in range(len(forecastDbStr)):
        db.push(forecastDbStr[x])
        print('success '+str(x))
    print(imageDbStr) 