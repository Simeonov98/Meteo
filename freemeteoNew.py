import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import date, datetime, timedelta
import db3,os,hash,operator
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
 
def degrees_to_direction(degrees):
    """Convert degrees to one of the 8 cardinal directions."""
    directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
    # Normalize degrees to [0, 360)
    degrees = degrees % 360
    # Each direction covers 45 degrees. Offset by 22.5 for center alignment.
    index = int((degrees + 22.5) // 45) % 8
    return directions[index]

def run(url,cId):
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
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)

    #  driver = "https://freemeteo.bg/weather/plovdiv/7-days/list/?gid=728193&language=bulgarian&country=bulgaria"
    driver.get(
        url
    )
    driver.implicitly_wait(3)
    try:
        driver.find_element(By.CLASS_NAME,'fc-button-label').click()
    except:
        pass
#     svg_element = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/section[2]/div/div[1]").find_element(By.CSS_SELECTOR,"svg[data-testid='IcWindIcon']")

# # Get the 'style' attribute as a string
#     style_value = svg_element.get_attribute("style")
#     print(style_value)
#     exit();

    # run the loop for every day and collect the data
    for i in range(3,8):
        day=driver.find_element(By.XPATH,f'/html/body/div[3]/div[2]/section[2]/div/div[{i}]')
        svg=day.find_element(By.CSS_SELECTOR,"svg[data-testid='IcWindIcon']")
        svgg=svg.get_attribute("style")
        located_day=day.get_attribute('innerText')
        degrees=svgg.split("rotate(")[1].split("deg)")[0]
        splitBySpace=located_day.rsplit('\n')
        # Remove empty strings
        splitBySpace = [x for x in splitBySpace if x.strip()]
        if splitBySpace[0] == 'Утре':
            # Example: ['Утре', 'частична заоблаченост.', '29°', '17°', '8 км/ч', '0мм']
            title.append('Утре')
            text.append(splitBySpace[1])
            tmax.append(splitBySpace[2])
            tmin.append(splitBySpace[3])
            wind.append(degrees_to_direction(float(degrees)))
            rain.append(splitBySpace[5])
        else:
            # Example: ['сряда', '10 09', 'частична заоблаченост.', '31°', '19°', '11 км/ч', '0мм']
            title.append(f"{splitBySpace[0]}, {splitBySpace[1]}")
            text.append(splitBySpace[2])
            tmax.append(splitBySpace[3])
            tmin.append(splitBySpace[4])
            wind.append(degrees_to_direction(float(degrees)))
            rain.append(splitBySpace[6])
    for i in range(0,5):
        res=''.join(title[i])
        if res == "Утре":
            tomorrow=datetime.now()+timedelta(days=1)
            parsed_date_tomorrow = datetime(datetime.now().year,datetime.now().month,tomorrow.day)
            #print(parsed_date_tomorrow)
            forecastDate.append(parsed_date_tomorrow)
        else:
            res_list=res.split(', ')
            parsed_date = datetime.strptime(res_list[1], "%d %m")
            parsed_date = parsed_date.replace(year=datetime.now().year)
            #print(parsed_date)
            forecastDate.append(parsed_date)
        print(forecastDate[i],forecastDate[i].weekday(),tmax[i].rstrip('°'),tmin[i].rstrip('°'),text[i],wind[i],rain[i].replace(',','.').rstrip('мм'))
        # forecastDbStr.append(f"""INSERT INTO "Freemeteo" ("forecastDay", weekday, tmax, tmin, text, wdir, rain, "cityId", "imageId") VALUES ('{forecastDate[i]}',{forecastDate[i].weekday()},{tmax[i].rstrip('°')},{tmin[i].rstrip('°')},'{text[i]}','{wind[i]}',{rain[i].replace(',','.').rstrip('мм')},{cId},(SELECT id FROM "Image" WHERE name = '{hashedImgName}'))""");
        forecastDbStr.append(f"""INSERT INTO "Freemeteo" ("forecastDay", weekday, tmax, tmin, text, wdir, rain, "cityId") VALUES ('
                             {forecastDate[i]}',{forecastDate[i].weekday()},{tmax[i].rstrip('°')},{tmin[i].rstrip('°')},'{text[i]}','{wind[i]}',{rain[i].replace(',','.').rstrip('мм')},{cId})""");

    driver.close()
    # exit();
        
  
  
    now1=datetime.now().strftime('%Y-%m-%d %H:%M:%S')



    #print(len(day))
    print("freemeteo")
    print(str(datetime.now()).rsplit('.',1)[0])

        # image.append(day[i].
        #              find_element(By.CLASS_NAME,'icon').
        #              find_element(By.TAG_NAME,'span'))
        # temp_imgname='/home/simeon/programming/Meteo/freemeteo/takenAt.png'
        # image[i].screenshot(temp_imgname)
        # hashedImgName=hash.getHash(temp_imgname)
        # if not os.path.exists('/home/simeon/programming/Meteo/freemeteo/'+hashedImgName):#check in folder if temp_imgname exists
        #     os.rename(temp_imgname,'/home/simeon/programming/Meteo/freemeteo/'+hashedImgName+'.png')

        # # image_data = hash.convertToBinaryData('./freemeteo/'+hashedImgName+'.png')
        # ImageDbStr.append(hashedImgName)


        # argument=title[i].lstrip("0123456789 ")

    # forecastDate.append(datetime(datetime.now().year,numbers_to_strings(argument),int(title[i].rstrip('януфевмарпйюилвгсоктд '))))
    # forecastDbStr.append(f"""INSERT INTO "Freemeteo" ("forecastDay", weekday, tmax, tmin, text, wdir, rain, "cityId", "imageId") VALUES ('{forecastDate[i]}',{forecastDate[i].weekday()},{tmax[i].replace('макс: ','').replace('°C','')},{tmin[i].replace('мин: ','').replace('°C','')},'{text[i]}','{wind[i]}',{rain[i].replace(',','.')},{cId},(SELECT id FROM "Image" WHERE name = '{hashedImgName}'))""");

    #driver.close()
    

    # db3.open_conn()
    # for img in ImageDbStr:
        # db2.insertBLOB(img,"/home/simeon/programming/Meteo/freemeteo/"+img+".png")
    for x in range(len(forecastDbStr)):
        db3.push(forecastDbStr[x])
        print('success '+str(x))
        print(str(datetime.now()).rsplit('.',1)[0])
    print(ImageDbStr)
    # driver.close()
    # db3.close_conn()
