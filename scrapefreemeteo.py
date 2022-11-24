from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

url="https://freemeteo.bg/weather/plovdiv/7-days/list/?gid=728193&language=english&country=bulgaria"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
arr=doc.find(["div"], class_="today sevendays")



day=arr.find_all(["div"],class_='day')

for x in range(0, len(day)):
    #print(day[x].find(["div"], class_="title").text)
    #print(day[x].find(["div"], class_="temps").text)
    print(day[x].find(["div"], class_="wind").text)
    print(day[x].find(["div"], class_="pred").find("span").find("script").contents[0])
    #print(day[x].find(["div"], class_="extra").text)
    print("----------------------------")
   # print(day[x].find(["div"], class_="hover").text)