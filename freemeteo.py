from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import date, datetime
import db,os,hash,operator
from chromedriver_py import binary_path
from functools import reduce
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


def run(url,cId):

    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)

    #  driver = "https://freemeteo.bg/weather/plovdiv/7-days/list/?gid=728193&language=bulgarian&country=bulgaria"
    driver.get(
        url
    )
    row=[]
    day=driver.find_elements(By.CLASS_NAME,'day')
    title=[]
    image=[]
    tmin=[]
    tmax=[]
    text=[]
    wind=[]
    rain=[]
    forecastDate=[]
    forecastDbStr=[]
    cityDbStr=[]
    ImageDbStr=[]
    formatted=[]
    #print(day[0].find_element(By.CLASS_NAME,'temps').find_elements(By.CSS_SELECTOR,'#content > div.right-col > div.weather-now > div.today.table > div > div > div:nth-child(2) > div.temps > b'))
    # text=verbal[::2]
    now1=datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    #print(len(day))
    print("freemeteo")
    print(str(datetime.now()).rsplit('.',1)[0])
    for i in range(0,7):
        title.append(day[i].
                     find_element(By.CLASS_NAME,'title').
                     find_element(By.TAG_NAME,'span').
                     get_attribute('innerText')) #reaching furhter into the dom (gotta transform text to datetime)
        try:
            tmax.append(day[i].
                        find_element(By.CLASS_NAME,'temps').
                        find_element(By.TAG_NAME,'b').
                        get_attribute('innerText'))
        except NoSuchElementException:
            tmax.append("NULL") #here we append what the DB recognises as N/A or null
        tmin.append(day[i].
                    find_element(By.CLASS_NAME,'temps').
                    find_element(By.TAG_NAME,'span').
                    get_attribute('innerText'))
        text.append(day[i].find_element(By.CLASS_NAME,'hover').
                    find_element(By.CLASS_NAME,'info').
                    find_element(By.CLASS_NAME,'extra').
                    get_attribute('innerText'))
        wind.append((day[i].
                     find_element(By.CLASS_NAME,'wind').
                     find_element(By.TAG_NAME,'span').
                     get_attribute('class')).
                     rsplit(' ',1)[1])
        try:
            rain.append(day[i].
                        find_element(By.CLASS_NAME,'extra').
                        find_element(By.TAG_NAME,'b').
                        get_attribute('innerText'))
        except NoSuchElementException:
            rain.append('N/A')
        image.append(day[i].
                     find_element(By.CLASS_NAME,'icon').
                     find_element(By.TAG_NAME,'span'))
        temp_imgname='/home/simeon/programming/Meteo/freemeteo/takenAt.png'
        image[i].screenshot(temp_imgname)
        hashedImgName=hash.getHash(temp_imgname)
        if not os.path.exists('/home/simeon/programming/Meteo/sinoptik/'+hashedImgName):#check in folder if temp_imgname exists
            os.rename(temp_imgname,'/home/simeon/programming/Meteo/freemeteo/'+hashedImgName+'.png')

        # image_data = hash.convertToBinaryData('./freemeteo/'+hashedImgName+'.png')
        ImageDbStr.append(hashedImgName)


        argument=title[i].lstrip("0123456789 ")
        forecastDate.append(datetime(datetime.now().year,numbers_to_strings(argument),int(title[i].rstrip('януфевмарпйюилвгсоктд '))))
        #print(forecastDate[i],forecastDate[i].weekday(),tmax[i].replace('макс: ','').replace('°C',''),tmin[i].replace('мин: ','').replace('°C',''),text[i],wind[i],rain[i].replace(',','.'))
        #print(i)
        forecastDbStr.append(f"INSERT INTO Freemeteo (forecastDay, weekday, tmax, tmin, text, wdir, rain, cityId, imageId) VALUES ('{forecastDate[i]}',{forecastDate[i].weekday()},{tmax[i].replace('макс: ','').replace('°C','')},{tmin[i].replace('мин: ','').replace('°C','')},'{text[i]}','{wind[i]}',{rain[i].replace(',','.')},{cId},(SELECT id FROM Image WHERE name = '{hashedImgName}'))")

    #driver.close()
    


    for img in ImageDbStr:
        db.insertBLOB(img,"/home/simeon/programming/Meteo/freemeteo/"+img+".png")
    for x in range(len(forecastDbStr)):
        db.push(forecastDbStr[x])
        print('success '+str(x))
        print(str(datetime.now()).rsplit('.',1)[0])
    print(ImageDbStr)
    driver.close()
