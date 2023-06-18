#!/usr/bin python3
import os,freemeteo,dalivali,sinoptik

# plovdiv 
freemeteo.run("https://freemeteo.bg/weather/plovdiv/7-days/list/?gid=728193&language=bulgarian&country=bulgaria",5)
dalivali.run("https://www.dalivali.bg/?type=daily&location=173",5)
sinoptik.run("https://www.sinoptik.bg/plovdiv-bulgaria-100728193/10-days/",5)
# sofia
freemeteo.run("https://freemeteo.bg/weather/sofia/7-days/list/?gid=727011&language=bulgarian&country=bulgaria",6)
dalivali.run("https://dalivali.bg/?type=daily&location=217",6)
sinoptik.run("https://www.sinoptik.bg/sofia-bulgaria-100727011/10-days",6)
# vidin
freemeteo.run("https://freemeteo.bg/weather/vidin/7-days/list/?gid=725905&language=bulgarian&country=bulgaria",7)
dalivali.run("https://dalivali.bg/?type=daily&location=48",7)
sinoptik.run("https://www.sinoptik.bg/vidin-bulgaria-100725905/10-days",7)    