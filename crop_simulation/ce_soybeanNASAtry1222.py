
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 22:51:09 2018
@author: Darren
this code is for using pandas to read weather location and then I will use it into crop simulation model
"""

import os, sys
import yaml
import pcse
import pandas as pd
import matplotlib.pyplot as plt

#read csv file
data = pd.read_csv ("weather.csv")

#create lon and lat variables 
lon = data.iloc [:, 0].values
lat = data.iloc [:, 1].values

for x in lon:
    for y in lat:        
        #using modeul to read weather data
        from pcse.db import NASAPowerWeatherDataProvider
        wdp = NASAPowerWeatherDataProvider (latitude = y, longitude = x)
        print (wdp)
        
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
        cropd.print_crops_varieties ()
        #read soybena crop
        cropd.set_active_crop ('soybean', 'Soybean_902')
        print (cropd)
        
        # read soil file
        from pcse.fileinput import CABOFileReader
        soildata = CABOFileReader ("soy.soil")
        
        #site parameters
        from pcse.util import WOFOST71SiteDataProvider
        sitedata = WOFOST71SiteDataProvider (WAV = 100, CO2 = 360)
        print (sitedata)
        
        #pack the different sets of parameters
        from pcse.base_classes import ParameterProvider
        parameters = ParameterProvider (cropdata = cropd, soildata = soildata, sitedata = sitedata) #cropdata = cropd
        
        #simulate the crop
        from pcse.models import Wofost71_WLP_FD
        wofsim = Wofost71_WLP_FD (parameters, wdp, agro)
        wofsim.run_till_terminate ()
        output = wofsim.get_output ()
        len (output)
        
        #save as xls file using pandas
        df = pd.DataFrame(output)
        df.to_excel("soybean0203.xlsx")







