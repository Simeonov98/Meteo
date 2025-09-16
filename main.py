#!/usr/bin python3
import os,freemeteoNew,dalivali2,sinoptik

# plovdiv 
freemeteoNew.run("https://freemeteo.bg/weather/plovdiv/7-days/list/?gid=728193&language=bulgarian&country=bulgaria",5)
dalivali2.run("https://dalivali.bg/?location=173",5)
sinoptik.run("https://www.sinoptik.bg/plovdiv-bulgaria-100728193/14-days/",5)
# sofia
freemeteoNew.run("https://freemeteo.bg/weather/sofia/15-days/list/?gid=727011&language=bulgarian&country=bulgaria",6)
dalivali2.run("https://dalivali.bg/?location=217",6)
sinoptik.run("https://www.sinoptik.bg/sofia-bulgaria-100727011/14-days",6)
# vidin
freemeteoNew.run("https://freemeteo.bg/weather/vidin/15-days/list/?gid=725905&language=bulgarian&country=bulgaria",7)
dalivali2.run("https://dalivali.bg/?location=48",7)
sinoptik.run("https://www.sinoptik.bg/vidin-bulgaria-100725905/14-days",7)    
