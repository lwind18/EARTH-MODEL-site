# -*- coding: utf-8 -*-
# Copyright (c) 2004-2014 Alterra, Wageningen-UR
# Allard de Wit (allard.dewit@wur.nl), June 2017
# the goal of this script is to estimate the soybean in Cerrado
#before this script, I need to (1) process growing season LAI from MODIS; (2) collect weather parameters
#since there are two ways to get weather part, I want to use excel to modify my own weather parameters
 
import os
import pcse
import matplotlib.pyplot as plt

#using CABO filereader to read crop parameters 
from pcse.fileinput import CABOFileReader
cropdata = CABOFileReader ("sug0601.crop") 
print (cropdata)

# read soil file
from pcse.fileinput import CABOFileReader
soildata = CABOFileReader ("soildata.soil")
print (soildata)

#site parameters
from pcse.util import WOFOST71SiteDataProvider
sitedata = WOFOST71SiteDataProvider (WAV = 100, CO2 = 360)
print (sitedata)

#pack the different sets of parameters
from pcse.base_classes import ParameterProvider
parameters = ParameterProvider (cropdata = cropdata, soildata = soildata, sitedata = sitedata) #cropdata = cropd

#agromanagement control the start date and end date
#there are two files, one is defalut, the other one is for excel weather data
from pcse.fileinput import YAMLAgroManagementReader
agromanagement = YAMLAgroManagementReader ("sugarbeet_c.agro")
print (agromanagement)

#using modeul to read weather data
from pcse.db import NASAPowerWeatherDataProvider
wdp = NASAPowerWeatherDataProvider (latitude = 52, longitude = 5)
print (wdp)

#from pcse.fileinput import ExcelWeatherDataProvider
#wdp = ExcelWeatherDataProvider ("weather04.xlsx")
#print (wdp)

#simulate the crop
from pcse.models import Wofost71_WLP_FD
wofsim = Wofost71_WLP_FD (parameters, wdp, agromanagement)
wofsim.run_till_terminate ()
output = wofsim.get_output ()
len (output)

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
fig.savefig("sugarbeet.png")

    






