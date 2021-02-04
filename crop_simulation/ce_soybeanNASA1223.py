
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 22:51:09 2018
@author: Darren
This code is for crop simulation model.
Weather part: I list all grids cooradiate infromation and use NASA power to read it in for loop 
All lines of code are programing at one folder and just need to save the simulated results at the other folder
"""

import os, sys
import yaml
import pcse
import pandas as pd
import re
import matplotlib.pyplot as plt

#read csv file
data1 = pd.read_csv ("crop_location02039.csv")

for num, lon, lat in zip (data1.num, data1.lon, data1.lat):    #using zip to package lon and lat  
    #using modeul to read weather data
    from pcse.db import NASAPowerWeatherDataProvider
    wdp = NASAPowerWeatherDataProvider (latitude = lat, longitude = lon)
    #print (wdp)
    
    #define the agromanagement based on the study area
    agro_yaml = """
    - 2002-10-01:
        CropCalendar:
            crop_name: soybean
            variety_name: Soybean_902
            crop_start_date: 2002-10-10
            crop_start_type: sowing
            crop_end_date: 2003-03-31
            crop_end_type: harvest
            max_duration: 200
        TimedEvents: null
        StateEvents: null
        """
    agro = yaml.load(agro_yaml)
    
    #crop parameters have two ways: 
    #using YAML cropdataprovider to find the target crop
    #https://github.com/ajwdewit/WOFOST_crop_parameters (introduction of these parameters)
    from pcse.fileinput import YAMLCropDataProvider
    force_reload=True
    cropd = YAMLCropDataProvider () 
    #cropd.print_crops_varieties ()
    #read soybena crop
    cropd.set_active_crop ('soybean', 'Soybean_902')
    
    # read soil file
    from pcse.fileinput import CABOFileReader
    soildata = CABOFileReader ("soy.soil")
    
    #site parameters
    from pcse.util import WOFOST71SiteDataProvider
    sitedata = WOFOST71SiteDataProvider (WAV = 100, CO2 = 360)
    
    #pack the different sets of parameters
    from pcse.base_classes import ParameterProvider
    parameters = ParameterProvider (cropdata = cropd, soildata = soildata, sitedata = sitedata) #cropdata = cropd
    
    #simulate the crop
    from pcse.models import Wofost71_WLP_FD
    wofsim = Wofost71_WLP_FD (parameters, wdp, agro)
    
    #from pcse.models import Wofost71_PP
    #wofsim = Wofost71_PP (parameters, wdp, agro)

    wofsim.run_till_terminate ()
    output = wofsim.get_output ()
    len (output)
    
    #save as xls file using pandas
    df = pd.DataFrame(output)
    df.to_excel("/Users/Darren/Desktop/DIS_tools/Q3_wofost/crop_simulation/result0203/" 
                 + "soybean" + str(num) +".xlsx")
    print ("soybean" + str(num) + ".xlsx")

"""
#next step is that I need to extract the particular cell from output (row = day, column = TAGP)
and write it into a new excel which row = location, column = TAGP
package: openpyxl
http://wenqiang-china.github.io/2016/05/13/python-opetating-excel/
"""
## create a holder folder and list fiels in the path
#folder = "/Users/Darren/Desktop/DIS_tools/Q3_wofost/crop_simulation/result0203"
##change path to the folder path
#os.chdir(folder)
#dir_list = os.listdir(folder)
#yds =[]
#for dt in dir_list:
#    wb = load_workbook (dt)
#    ws = wb.active
#    yd = ws.cell(row = 183, column = 6).value
#    yds.append (yd)
##print (yds)
##convert list to series and add a column name
#ydsup = pd.Series(yds)
#ydsupcol = ydsup.to_frame("yield")
##print (ydsupcol)
#
##add this series to the existed one (add, insert, append, join, merge)
###https://pandas.pydata.org/pandas-docs/stable/merging.html
#
#data2 = data1.join (ydsupcol)
##print (data2)
#data2.to_csv ("soybeanyield0203.csv")
        
    









