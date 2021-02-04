#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 23:43:36 2018
@author: Darren
This script is for extract yield from simulation and join the yield column to csv file.
"""
import os, sys
import pandas as pd
import re

#read csv file
data1 = pd.read_csv ("weather1314_location.csv")

folder = "/Users/Darren/Desktop/DIS_tools/Q3_wofost/crop_simulation/result1314"
#change path to the folder path
os.chdir(folder)
dir_list = os.listdir(folder) #os.listdir the order of files is no order, I need to use sort to order it
dir_list_xlsx = [f for f in dir_list if f[-4:]=="xlsx"]

dir_list_xlsx.sort (key =lambda x: int(re.sub(r'\D',"",x))) #if I use re.sub, I need to import re
#print (dir_list_xlsx)

yds = [] #create a empty list 
for dt in dir_list_xlsx:
    if dt.endswith ("xlsx"):        
        ws = pd.read_excel(dt)
        yd = ws.iloc[165, 4]  #except row and column name, start from 0 
        yds.append (yd)
    else:
        pass
#print (yds)
#convert list to series and add a column name to the series
ydsup = pd.Series(yds)
ydsupcol = ydsup.to_frame("yield")
print (ydsupcol)

#add this series to the existed one (add, insert, append, join, merge)
##append need to the exsited data is series and data that need to append is also need to be series
##add is two dataframe add
##https://pandas.pydata.org/pandas-docs/stable/merging.html

data2 = data1.join (ydsupcol)
#print (data2)
data2.to_csv ("Soybeanyield131413.csv")

   

    
    
