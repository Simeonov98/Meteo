#!/usr/bin python3
import os,freemeteo,dalivali,sinoptik

# plovdiv 
freemeteo.run("https://freemeteo.bg/weather/plovdiv/7-days/list/?gid=728193&language=bulgarian&country=bulgaria")
dalivali.run("https://www.dalivali.bg/?type=daily&location=173")
sinoptik.run("https://www.sinoptik.bg/plovdiv-bulgaria-100728193/10-days/")
# sofia
freemeteo.run("https://freemeteo.bg/weather/sofia/7-days/list/?gid=727011&language=bulgarian&country=bulgaria")
dalivali.run("https://dalivali.bg/?type=daily&location=217")
sinoptik.run("https://www.sinoptik.bg/sofia-bulgaria-100727011/10-days")
# vidin
freemeteo.run("https://freemeteo.bg/weather/vidin/7-days/list/?gid=725905&language=bulgarian&country=bulgaria")
dalivali.run("https://dalivali.bg/?type=daily&location=48")
sinoptik.run("https://www.sinoptik.bg/vidin-bulgaria-100725905/10-days")    