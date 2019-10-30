# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 19:16:22 2019

@author: jiabx
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotly.offline import plot
from sklearn import linear_model
import statsmodels.api as sm
from scipy import stats

## Read in and print the head of the combined_cleaned file
df = pd.read_csv('combined_cleaned.csv')
print("The head of original dataset:", "\n", df.head(), "\n")
print("The shape of original dataset:", df.shape, "\n")

## Check columns
for col in df.columns:
    print(col)

## Remove missing values
df = df.dropna()

## Response variable: 

#####################################################################
########### Fit the MLR models for each crime variables  ############
#####################################################################
df_basic = df.drop(columns=['Violent', 'County', 'State', 'Murder_and_nonnegligent_manslaughter', 
                            'Rape', 'Robbery', 'Aggravated_assault', 'Property_crime', 'Burglary',
                            'Larceny_theft', 'Motor_vehicle_theft', 'Arson'])

df_related = df.drop(columns=['County', 'State'])
    
X = df_basic
Y = df["Violent"]

# with statsmodels
def reg_test(X, Y):
    X = sm.add_constant(X) # adding a constant
     
    model = sm.OLS(Y, X).fit()
    predictions = model.predict(X) 
     
    print_model = model.summary()
#    print(predictions)
    print(print_model)
reg_test(X, df["Violent"])
reg_test(X, df["Murder_and_nonnegligent_manslaughter"])
reg_test(X, df["Rape"])
reg_test(X, df["Robbery"])
reg_test(X, df["Aggravated_assault"])
reg_test(X, df["Property_crime"])
reg_test(X, df["Burglary"])
reg_test(X, df["Larceny_theft"])
reg_test(X, df["Motor_vehicle_theft"])
reg_test(X, df["Arson"])


#####################################################################
###################### Correation Analysis  #########################
#####################################################################
corr_matrix = df.corr()
corr_matrix = pd.DataFrame(corr_matrix)
#corr_matrix.to_csv("./corr_matrix.csv", sep=',',index=False)

## Heatmap
plt.matshow(df.corr(), fignum = plt.figure(figsize=(19, 15)).number)
plt.xticks(range(len(df_related.columns)), df_related.columns, fontsize=14, rotation=90)
plt.yticks(range(len(df_related.columns)), df_related.columns, fontsize=14)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
#plt.title('Correlation Matrix for Crime Data', fontsize=16)
plt.show()

#####################################################################
###################### independent sample t-tests  ##################
#####################################################################

MD = df[(df['State'] == 'MD')]
VA = df[(df['State'] == 'VA')]


def ttest(x): 
    print(x)
    print(stats.ttest_ind(MD[x], VA[x], equal_var = False))

ttest("Violent")
ttest("Murder_and_nonnegligent_manslaughter")
ttest("Rape")
ttest("Robbery")
ttest("Aggravated_assault")
ttest("Property_crime")
ttest("Burglary")
ttest("Larceny_theft")
ttest("Motor_vehicle_theft")
ttest("Arson")

