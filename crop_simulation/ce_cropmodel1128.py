# -*- coding: utf-8 -*-
# Copyright (c) 2004-2014 Alterra, Wageningen-UR
# Allard de Wit (allard.dewit@wur.nl), June 2017
# the goal of this script is to estimate the soybean yield in Cerrado
# date: 12/1/2018
#before this script, I need to:
#(1) process growing season LAI from MODIS; 
#(2) collect weather parameters. I prefer to use excel to generate weather parameters
#(3) collect soil parameters
## the program of this script:
#simulate crop yield need crop, soil, weather, and other parameters.
#crop part, I can use YAML to read it, and I need to modify it to fit the study area
#soil part, I used the file from control center, and I also need to modify some parameters
#weather part, I will use excel that means I need to convert raster data to excel with each pixel


import os, sys
import yaml
import pcse
import pandas as pd
import matplotlib.pyplot as plt


#define the agromanagement based on the study area
agro_yaml = """
- 2002-10-01:
    CropCalendar:
        crop_name: soybean
        variety_name: Soybean_906
        crop_start_date: 2002-10-15
        crop_start_type: sowing
        crop_end_date: 2003-03-31
        crop_end_type: harvest
        max_duration: 200
    TimedEvents: null
    StateEvents: null
"""
agro = yaml.load(agro_yaml)


#crop parameters have two ways: (1) using YAMLcropdataprovider, (2) uisng CABOfilereader
#using YAML cropdataprovider to find the target crop
#https://github.com/ajwdewit/WOFOST_crop_parameters (introduction of these parameters)
from pcse.fileinput import YAMLCropDataProvider
force_reload=True
cropd = YAMLCropDataProvider ("/Users/Darren/Desktop/DIS_tools/Q3_wofost/WOFOST_crop_parameters-master") 
cropd.print_crops_varieties ()
#read soybena crop
cropd.set_active_crop ('soybean', 'Soybean_906')
print (cropd)

##using CABO filereader to read crop parameters 
#from pcse.fileinput import CABOFileReader
#cropdata = CABOFileReader ("sug0601.crop") 
#print (cropdata)

# read soil file
from pcse.fileinput import CABOFileReader
soildata = CABOFileReader ("soy.soil")

#site parameters
from pcse.util import WOFOST71SiteDataProvider
sitedata = WOFOST71SiteDataProvider (WAV = 20, CO2 = 500)  #initial WAV=0~100, CO2=300~1400
print (sitedata)

#pack the different sets of parameters
from pcse.base_classes import ParameterProvider
parameters = ParameterProvider (cropdata = cropd, soildata = soildata, sitedata = sitedata) #cropdata = cropd

##using modeul to read weather data
#from pcse.db import NASAPowerWeatherDataProvider
#wdp = NASAPowerWeatherDataProvider (latitude = -2.625, longitude = -43.625)
#print (wdp)

from pcse.fileinput import ExcelWeatherDataProvider
wdp = ExcelWeatherDataProvider ("wea0.xlsx")
print (wdp)

#simulate the crop
#from pcse.models import Wofost71_WLP_FD
#wofsim = Wofost71_WLP_FD (parameters, wdp, agro)

from pcse.models import Wofost71_PP
wofsim = Wofost71_PP (parameters, wdp, agro)

wofsim.run_till_terminate ()
output = wofsim.get_output ()
len (output)

#save as xls file using pandas
df = pd.DataFrame(output)
df.to_excel("soybean02030.xlsx")

#vasulate result using matplotlib
varnames = ["day", "DVS", "TAGP", "LAI", "SM"]
tmp = {}
for var in varnames:
    tmp[var] = [t[var] for t in output]
day = tmp.pop ("day")
fig, axes = plt.subplots(nrows = 2, ncols = 2, figsize = (10, 8))
for var, ax in zip(["DVS", "TAGP", "LAI", "SM"], axes.flatten()):
    ax.plot_date(day, tmp[var], "b-")
    ax.set_title(var)
fig.autofmt_xdate()
fig.savefig("soybean0.png")

    






