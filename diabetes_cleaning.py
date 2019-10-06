import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

desired_width = 600
pd.set_option('display.width', desired_width)

input_file = 'raw_data/DiabetesVA.csv'

diabetes_va = pd.read_csv(input_file)

############### drop description rows and columns
diabetes_va.columns = diabetes_va.iloc[1].values
diabetes_va.drop([0, 1, 136], axis=0, inplace=True)
diabetes_va.drop(['State', 'CountyFIPS', 'Lower Limit', ' Upper Limit'], axis=1, inplace=True)
######################################

with pd.option_context('display.max_columns', None):
    print(diabetes_va)
    print(diabetes_va.iloc[:, 1:].astype(np.float).describe())

############### we drop all cities in va and rename counties to match the crime data
s1 = 'County'
s2 = 'City'
for c in diabetes_va.County.values:
    if c.endswith(s2):
        diabetes_va.drop(diabetes_va.index[diabetes_va['County'] == c], axis=0, inplace=True)
    elif c.endswith(s1):
        diabetes_va.loc[diabetes_va.index[diabetes_va['County'] == c], 'County'] = c[:-7]

diabetes_va.index = np.arange(len(diabetes_va))
diabetes_va.iloc[:, 1:] = diabetes_va.iloc[:, 1:].astype(np.float)
######################################

# boxplot for Percentage
fig = go.Figure()
fig.add_trace(go.Box(y=diabetes_va.Percentage, name='Percentage', notched=True,
                     boxpoints='all',jitter=0.3,pointpos=-1.8))
fig.show()