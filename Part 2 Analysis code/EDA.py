#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:01:30 2019

@author: kiwi
"""

import pandas as pd
import statistics as st
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium import plugins
from IPython.display import HTML, display
import datetime


#EDA
census = pd.read_csv('../cleaned_data/census_cleaned.csv', sep=',', encoding='latin1')
crime_vm = pd.read_csv('../cleaned_data/crime_VM_cleaned.csv', sep=',', encoding='latin1')

crime_dc = pd.read_csv('../cleaned_data/dc_crime_cleaned.csv', parse_dates=['START_DATE'],sep=',', encoding='latin1')
diabetes = pd.read_csv('../cleaned_data/diabetes_cleaned.csv', sep=',', encoding='latin1')
mob_md = pd.read_csv('../cleaned_data/mob_md_cleaned.csv', sep=',', encoding='latin1')
mob_va = pd.read_csv('../cleaned_data/mob_va_cleaned.csv', sep=',', encoding='latin1')



#           census           #
census.head()
census.columns
census.drop(['Unnamed: 0','Unnamed: 0.1'], inplace = True, axis = 1)
census.describe()



#          crime_vm          #
crime_vm.head()
crime_vm.columns
crime_vm.drop(['Unnamed: 0'], inplace = True, axis = 1)
crime_vm.describe()



#          crime_dc          #
crime_dc['START_DATE'] = pd.to_datetime(crime_dc['START_DATE'], errors='coerce', unit='s')
crime_dc.head()
crime_dc['DATE'] = crime_dc['START_DATE'].astype(str).str[:10]
crime_dc.head()
crime_dc.drop(['START_DATE', 'END_DATE'], inplace = True, axis = 1) #Use date to replace START_DATE and END_DATE
crime_dc.drop(['Unnamed: 0'], inplace = True, axis = 1)

crime_dc.columns
crime_dc = crime_dc[['DATE', 'SHIFT', 'LATITUDE', 'LONGITUDE', 'BLOCK', 'OFFENSE', 'METHOD']]
crime_dc.head()


#Shorten the Block name
crime_dc['BLOCK'] = crime_dc['BLOCK'].str.replace(r'.*B', 'B')
crime_dc['BLOCK'].head()

#Check the most frequent crime block
st.mode(crime_dc['BLOCK'])


#Create a bin for different age group
crime_dc['MONTH'] = crime_dc['DATE'].astype(str).str[0:7]
crime_dc['MONTH']= crime_dc['MONTH'].replace('2016-01', "JAN")
crime_dc['MONTH']= crime_dc['MONTH'].replace('2016-02', "FEB")
crime_dc['MONTH']= crime_dc['MONTH'].replace('2016-03', "MAR")
crime_dc['MONTH']= crime_dc['MONTH'].replace('2016-04', "APR")
crime_dc['MONTH']= crime_dc['MONTH'].replace('2016-05', "MAY")
crime_dc['MONTH']= crime_dc['MONTH'].replace('2016-06', "JUN")

crime_dc['MONTH']= crime_dc['MONTH'].replace('2016-07', "JUL")
crime_dc['MONTH']= crime_dc['MONTH'].replace('2016-08', "AUG")
crime_dc['MONTH']= crime_dc['MONTH'].replace('2016-09', "SEPT")
crime_dc['MONTH']= crime_dc['MONTH'].replace('2016-10', "OCT")
crime_dc['MONTH']= crime_dc['MONTH'].replace('2016-11', "NOV")
crime_dc['MONTH']= crime_dc['MONTH'].replace('2016-12', "DEC")


#Check the crime occurance in each month
crime_dc['MONTH'].value_counts()


#Check the top crime occurance for days
D_NUM = crime_dc['DATE'].value_counts()
D_NUM.head(10)


#MONTH CRIME FREQUENCY VIS
sns.catplot(y='MONTH',
           kind='count',
            height=5, 
            aspect=1.5,
            order=crime_dc.MONTH.value_counts().index,
           data=crime_dc)


#Check the mode for SHIFT
st.mode(crime_dc['SHIFT'])
crime_dc['SHIFT'].value_counts()


#SHIFT VIS
sns.catplot(y='SHIFT',
           kind='count',
            height=5, 
            aspect=1.5,
            order=crime_dc.SHIFT.value_counts().index,
           data=crime_dc)


#Check the mode for OFFENSE
st.mode(crime_dc['OFFENSE'])
crime_dc['OFFENSE'].value_counts()


#OFFENSE VIS
sns.catplot(y='OFFENSE',
           kind='count',
            height=5, 
            aspect=1.5,
            order=crime_dc.OFFENSE.value_counts().index,
           data=crime_dc)


#heat map for crime location
m = folium.Map([38.9072, -77.0369], zoom_start=11)
for index, row in crime_dc.iterrows():
    folium.CircleMarker([row['LATITUDE'], row['LONGITUDE']],
                        radius=15,
                        popup=row['BLOCK'],
                        fill_color="#3db7e4",
                       ).add_to(m)

crimeadd = crime_dc[['LATITUDE', 'LONGITUDE']].as_matrix()
m.add_child(plugins.HeatMap(crimeadd, radius=15))
display(m)
m.save('crime_loc.html')



#          diabetes          #
diabetes.head()
diabetes.columns
diabetes.drop(['Unnamed: 0'], inplace = True, axis = 1)
diabetes.describe()


#           mob_md           #
mob_md.head()
mob_md.columns
mob_md.drop(['Unnamed: 0'], inplace = True, axis = 1)
mob_md.describe()


#           mob_va           #
mob_va.head()
mob_va.columns
mob_va.drop(['Unnamed: 0'], inplace = True, axis = 1)
mob_va.describe()