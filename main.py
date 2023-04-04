import os,freemeteo,dalivali,sinoptik

freemeteo.run("https://freemeteo.bg/weather/plovdiv/7-days/list/?gid=728193&language=bulgarian&country=bulgaria")
dalivali.run("https://www.dalivali.bg/?type=daily&location=173")
sinoptik.run("https://www.sinoptik.bg/plovdiv-bulgaria-100728193/10-days/")