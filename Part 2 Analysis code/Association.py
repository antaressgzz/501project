#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:27:27 2019

@author: Charlotte
"""
import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import matplotlib.pyplot as plt
from pandas import DataFrame
import matplotlib
matplotlib.use('agg') # Write figure to disk instead of displaying (for Windows Subsystem for Linux)

crime_dc = pd.read_csv('../cleaned_data/dc_crime_cleaned.csv')
crime_dc  = crime_dc.drop(columns = ['Unnamed: 0','END_DATE','LATITUDE'
                            ,'LONGITUDE','METHOD'])
crime_dc.head()
crime_dc['DATE'] = crime_dc['START_DATE'].astype(str).str[:10]
crime_dc.head()
crime_dc.drop(['START_DATE'], inplace = True, axis = 1)
crime_dc = crime_dc[['DATE', 'SHIFT', 'OFFENSE','BLOCK']]
crime_dc.head()

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
crime_dc.head(10)
## Only keep block names for association
crime_dc['BLOCK'] = crime_dc['BLOCK'].str.replace(r'.*B','B')
data = crime_dc
data  = data.drop(columns = ['DATE'])
pd.set_option('display.max_rows', 1000, "display.max_columns", 10)



## create rules
data1 = data.values.tolist()
data.to_csv(r'Crimedc_forvis.csv',header=None, index=None)
te = TransactionEncoder()
te_ary = te.fit(data1).transform(data1)
df = pd.DataFrame(te_ary, columns=te.columns_)
## support rules 
frequent_itemsets = apriori(df, min_support=0.01,use_colnames=True)
frequent_itemsets
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x:len(x))
frequent_itemsets[(frequent_itemsets['length']==3) & (frequent_itemsets['support']>=0.0015)].sort_values(by = 'support',ascending=False)



## rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.01)
rules.head(10)
## Top ten rules
sup10 = rules.sort_values(by = 'support',ascending=False)
sup10.head(10)
con10 = rules.sort_values(by = 'confidence',ascending=False)
con10.head(10)
lift10 = rules.sort_values(by = 'lift',ascending=False)
lift10.head(10)


## plot
support=rules.as_matrix(columns=['support'])
confidence=rules.as_matrix(columns=['confidence'])
plt.scatter(support, confidence, alpha=0.5, marker="*")
plt.xlabel('support')
plt.ylabel('confidence') 
plt.show()


# Convert the input into a 2D dictionary
data_map = data.drop(columns = ['BLOCK'])
data_map = data_map.values.tolist()
freqMap = {}
for line in data_map:
  for item in line:
    if not item in freqMap:
      freqMap[item] = {}

    for other_item in line:
      if not other_item in freqMap:
        freqMap[other_item] = {}

      freqMap[item][other_item] = freqMap[item].get(other_item, 0) + 1
      freqMap[other_item][item] = freqMap[other_item].get(item, 0) + 1

df = DataFrame(freqMap).T.fillna(0)
#####
# Create the plot
#####
plt.figure(figsize=(7,7))
plt.pcolormesh(df, edgecolors='black',shading ='flat',cmap = plt.get_cmap('Oranges'))
plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns, rotation = -90)
plt.savefig('plot.png')


 