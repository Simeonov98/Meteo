import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import date, datetime
import db,hash,os,operator
from functools import reduce
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
def numbers_to_strings(argument):
    switcher = {
        'Януари': 1,
        'Февруари': 2,
        'Март': 3,
        'Април': 4,
        'Май': 5,
        'Юни': 6,
        'Юли': 7,
        'Август': 8,
        'Септември': 9,
        'Октовмри': 10,
        'Ноември': 11,
        'Декември': 12,

    }
 
    # get() method of dictionary data type returns
    # value of passed argument if it is present
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
    return switcher.get(argument, "nothing")
def run(url,cId):
    options = FirefoxOptions()
    options.add_argument("--headless")
    #url="https://www.sinoptik.bg/plovdiv-bulgaria-100728193/10-days/"
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)
    driver.get(
         url
    )
    try:
        driver.find_element(By.ID,'didomi-notice-agree-button').click()
    except:
        pass

    verbal=[]
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
    image=[]
    forecastDate=[]
    forecastDbStr=[]
    imageDbStr=[]
    formatted=[]

    today = date.today()
    d1 = today.strftime("%d/%m/%Y") # dd/mm/YY

    days=driver.find_element(By.CLASS_NAME,'wf14dayRightContent')
    # days.screenshot('./sinoptik/wholepage.png')
    day=days.find_elements(By.TAG_NAME,'a')
    print("sinoptik")

    for i in range(0,7):
        # dayoftheweek.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightDay').get_attribute('innerHTML'))
        exdate.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightDate').get_attribute('innerHTML'))
        tmax.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightTemp').text)
        tmin.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightTempLow').text)
        winddir.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightWind').get_attribute('title'))
        windspd.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightWind').text)
        verbal.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightImg').get_attribute('title'))

        image.append(day[i].find_element(By.CLASS_NAME,'wf10dayRightImg'))
        temp_imgname='/home/simeon/programming/Meteo/sinoptik/forDate '+str(exdate[i])+' takenAt '+'.png'
        image[i].screenshot(temp_imgname)
        hashedImgName=hash.getHash(temp_imgname)
        if not os.path.exists('/home/simeon/programming/Meteo/sinoptik/'+hashedImgName):
            os.rename(temp_imgname,'/home/simeon/programming/Meteo/sinoptik/'+hashedImgName+'.png')
        # image_data=hash.convertToBinaryData('./sinoptik/'+hashedImgName+'.png')
        imageDbStr.append(hashedImgName)
        # print(exdate[i])
        dates=exdate[i].split()
        month=numbers_to_strings(exdate[i].split()[1]) # we have the month!!!
        
       
        
        forecastDate.append(datetime(datetime.now().year,int(month),int(dates[0])))
        # image[i].screenshot('./sinoptik/forDate '+str(exdate[i])+' takenAt '+str(datetime.now()).replace(".",":")+'.png')
        #print(str(i),forecastDate[i],forecastDate[i].weekday(),tmax[i].rstrip('°'),tmin[i].rstrip('°'),winddir[i],windspd[i],verbal[i])
        forecastDbStr.append(f"INSERT INTO Sinoptik (forecastDate, weekday, tmax, tmin, wdir, wspd, text, cityId, imageId) VALUES ('{forecastDate[i]}','{forecastDate[i].weekday()}','{tmax[i].rstrip('°')}','{tmin[i].rstrip('°')}','{winddir[i]}','{windspd[i]}','{verbal[i]}',{cId},(SELECT id FROM Image WHERE name = '{hashedImgName}'))");
        #print(str(i),forecastDate[i], forecastDate[i].weekday())
    #print(forecastDate)

    for img in imageDbStr:
        db.insertBLOB(img,"/home/simeon/programming/Meteo/sinoptik/"+img+".png")

    for x in range(len(forecastDbStr)):
        db.push(forecastDbStr[x])
        print('success '+ str(x))
        print(str(datetime.now()).rsplit('.',1)[0])
    print(imageDbStr)
    driver.close()
