import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

desired_width = 600
pd.set_option('display.width', desired_width)

input_file = ['raw_data/DiabetesVA.csv', 'raw_data/DiabetesMD.csv']

diabetes_va, diabetes_md = pd.read_csv(input_file[0]), pd.read_csv(input_file[1])

############### drop description rows and columns
diabetes_va.columns = diabetes_va.iloc[1].values
diabetes_va.drop([0, 1, 136], axis=0, inplace=True)
diabetes_va.drop(['State', 'CountyFIPS', 'Lower Limit', ' Upper Limit'], axis=1, inplace=True)
diabetes_md.columns = diabetes_md.iloc[1].values
diabetes_md.drop([0, 1, 26], axis=0, inplace=True)
diabetes_md.drop(['State', 'CountyFIPS', 'Lower Limit', ' Upper Limit'], axis=1, inplace=True)
diabetes_DF = pd.concat([diabetes_va, diabetes_md], ignore_index=True)
######################################

# with pd.option_context('display.max_columns', None):
#     print(diabetes_DF)
#     print(diabetes_DF.iloc[:, 1:].astype(np.float).describe())
#
# with pd.option_context('display.max_columns', None):
#     print(diabetes_md)
#     print(diabetes_md.iloc[:, 1:].astype(np.float).describe())

############### we rename counties to match the crime data and only keep county data.
s1 = 'County'
s2 = 'City'
for c in diabetes_DF.County.values:
    if c.endswith(s1):
        diabetes_DF.loc[diabetes_DF.index[diabetes_DF['County'] == c], 'County'] = c[:-7]
    elif c.endswith(s2):
        diabetes_DF.drop(diabetes_DF.index[diabetes_DF['County'] == c], axis=0, inplace=True)
############### missing values
print('Missing values:', np.where(pd.isnull(diabetes_DF)))

############### Reassign index
diabetes_DF.index = np.arange(len(diabetes_DF))

# histogram for distribution of diabetes percentage in VA
fig = px.histogram(diabetes_DF, x="Percentage",nbins=20)
fig.update_layout(
    title='Diabetes Distribution Histogram',
    yaxis_title='Percentage'
)
fig.show()


diabetes_DF.to_csv('cleaned_data/disbetes_cleaned.csv')

# boxplot for Percentage
# fig = go.Figure()
# fig.add_trace(go.Box(y=diabetes_DF.Percentage, name='Percentage', notched=True,
#                      boxpoints='all', jitter=0.3, pointpos=-1.8))
# fig.show()