from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

url="https://weather.com/weather/tenday/l/dd44ead62bb77ca2b236bca92f752cac528e0114d5f41d1f1c0921136b603e09?unit=m"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

arr=[]
tempsmax=[]
tempsmin=[]
percip=[]
wind=[]
humidity=[]


for x in range(0,14):
    arr.append(doc.find(["details"], id="detailIndex"+str(x)))
    tempsmax.append(arr[x].find("span"))
    tempsmin.append(arr[x].find(["span"], class_="DetailsSummary--lowTempValue--3H-7I"))
    percip.append(arr[x].find(["div"], class_="DetailsSummary--precip--1ecIJ"))
    wind.append(arr[x].find(["span"],class_="Wind--windWrapper--3aqXJ undefined"))
    humidity.append(arr[x].find(["span"],class_="DetailsTable--value--1q_qD"))


    print("According to weather.com the high/low temperatures for " + str(date.today()+timedelta(days=x))+" are "+ tempsmax[x].text+"C/" 
    + tempsmin[x].text+"C" + " and the rain chance is " + percip[x].find("span").text + 
    " with winds " + wind[x].text +" and humidity " + humidity[x].text)
  


