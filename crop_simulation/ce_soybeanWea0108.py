#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jau 08 22:51:09 2018
@author: Darren
This code is for crop simulation model.
Weather part: use data I collected from NASA and use ""weather_excel0107" to generate each point data
all lines of code are programing at one folder and just need to save the simulated results at the other folder
"""

import os, sys
import yaml
import pcse
import pandas as pd
import re
import matplotlib.pyplot as plt

folder = "/Users/Darren/Desktop/DIS_tools/Q3_wofost/crop_simulation/CE1314_13wea1681"
#change path to the folder path
os.chdir(folder)
dir_list = os.listdir(folder) #os.listdir the order of files is no order, I need to use sort to order it
dir_list_xlsx = [f for f in dir_list if f[-4:]=="xlsx"]

dir_list_xlsx.sort (key =lambda x: int(re.sub(r'\D',"",x))) #if I use re.sub, I need to import re
#print (dir_list_xlsx)
#read csv file

for f in dir_list_xlsx:    
    #using modeul to read weather data
    from pcse.fileinput import ExcelWeatherDataProvider
    wdp = ExcelWeatherDataProvider (f)
    #print (wdp)
    
    #define the agromanagement based on the study area
    agro_yaml = """
    - 2013-10-01:
        CropCalendar:
            crop_name: soybean
            variety_name: Soybean_906
            crop_start_date: 2013-10-15
            crop_start_type: sowing
            crop_end_date: 2014-03-15
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
    cropd = YAMLCropDataProvider ("/Users/Darren/Desktop/DIS_tools/Q3_wofost/WOFOST_crop_parameters-master") 
    #cropd.print_crops_varieties ()
    #read soybena crop
    cropd.set_active_crop ('soybean', 'Soybean_906')
    
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
#    from pcse.models import Wofost71_WLP_FD
#    wofsim = Wofost71_WLP_FD (parameters, wdp, agro)
    
    from pcse.models import Wofost71_PP   #potential production
    wofsim = Wofost71_PP (parameters, wdp, agro)
    
    wofsim.run_till_terminate ()
    output = wofsim.get_output ()
    len (output)
    
    #save as xls file using pandas
    df = pd.DataFrame(output)
    df.to_excel("/Users/Darren/Desktop/DIS_tools/Q3_wofost/crop_simulation/result1314/" 
                 + "soy" + str(f) +".xlsx")
    print ("soy" + str(f) + ".xlsx")

"""
#next step is that I need to extract the particular cell from output (row = day, column = TAGP)
and write it into a new excel which row = location, column = TAGP
package: openpyxl
http://wenqiang-china.github.io/2016/05/13/python-opetating-excel/
"""
