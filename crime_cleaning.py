import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

desired_width = 600
pd.set_option('display.width', desired_width)

input_file = ['raw_data/virginia.xls', 'raw_data/maryland.xls']

crime_va, crime_maryland = pd.read_excel(input_file[0]), pd.read_excel(input_file[1])

############### drop description rows and columns
crime_va.drop([0, 1, 2, 3, 4, 100, 101], axis=0, inplace=True)
crime_va.drop(['Table 8', 'Unnamed: 5'], axis=1, inplace=True)
crime_maryland.drop([0,1,2,3,4,27, 28,29], axis=0, inplace=True)
crime_maryland.drop(['MARYLAND', 'Unnamed: 5'], axis=1, inplace=True)

############# set column names
columns = ['County', 'Violent', 'Murder_and_nonnegligent_manslaughter',
           'Rape','Robbery', 'Aggravated_assault', 'Property_crime',
           'Burglary', 'Larceny_theft', 'Motor_vehicle_theft', 'Arson', 'Population']
crime_va.columns = columns
crime_maryland.columns = columns

crime_DF = pd.concat([crime_va, crime_maryland], ignore_index=True)


########## clean county name and set index
crime_DF.sort_values(by='County', inplace=True)
## remove if exist
s = ' County Police Department'
for n, c in enumerate(crime_DF.County.values):
    if c.endswith(s):
        crime_DF.County.values[n] = c[:-len(s)]
crime_DF.index = np.arange(len(crime_DF))

### change data store type
crime_DF.iloc[:, 1:] = crime_DF.iloc[:, 1:].astype(np.float)


### calculate crime rate (per 100,000 people)
for c in crime_DF.columns[1:-1]:
    crime_DF.loc[:, c] = crime_DF.loc[:, c] / crime_DF.iloc[:, -1] * 100000



with pd.option_context('display.max_columns', None):
    print(crime_DF.iloc[:, 1:].astype(np.float).describe())
    print(crime_DF.head())

# with pd.option_context('display.max_columns', None):
#     # print(crime_maryland.iloc[:, 1:].astype(np.float).describe())
#     print(crime_maryland.head(6))
#     print(crime_maryland.tail())

# boxplot for population
fig = go.Figure()
fig.add_trace(go.Box(y=crime_DF.Population, name='Population', boxpoints='all', jitter=0.3, pointpos=-1.8))
fig.show()

# The boxplot for population is highly squeezed, population in different counties vary significantly
# we may consider dividing all the counties in the following groups:
# A: population > 20,000
# B: 20,000 >=  population


crime_DF.loc[crime_DF.Population.values <= 20000, 'Pop_Gp'] = 'B'
crime_DF.loc[(crime_DF.Population.values > 20000), 'Pop_Gp'] = 'A'
print('Number of counties in group A:', sum(crime_DF.Population.values > 20000))
print('Number of counties in group B:', sum(crime_DF.Population.values <= 20000))

# check distribution of different violent crime types
fig = go.Figure()
fig.add_trace(go.Box(y=crime_DF.Rape, x=crime_DF.Pop_Gp, name='Rape', boxpoints='all', jitter=0.3, pointpos=-1.8))
fig.add_trace(go.Box(y=crime_DF.Robbery, x=crime_DF.Pop_Gp, name='Robbery', boxpoints='all', jitter=0.3, pointpos=-1.8))
fig.add_trace(go.Box(y=crime_DF.Murder_and_nonnegligent_manslaughter, x=crime_DF.Pop_Gp,
                     name='Murder_and_nonnegligent_manslaughter', boxpoints='all', jitter=0.3, pointpos=-1.8))
fig.add_trace(go.Box(y=crime_DF.Aggravated_assault, x=crime_DF.Pop_Gp,
                     name='Aggravated_assault', boxpoints='all', jitter=0.3, pointpos=-1.8))
fig.update_layout(
    title='Violent crime distribution',
    yaxis_title='crime per 100,000 inhabitant',
    boxmode='group' # group together boxes of the different traces for each value of x
)
fig.show()



# check distribution of different property crime types
fig = go.Figure()
fig.add_trace(go.Box(y=crime_DF.Burglary, x=crime_DF.Pop_Gp, name='Burglary',
                     boxpoints='all', jitter=0.3, pointpos=-1.8))
fig.add_trace(go.Box(y=crime_DF.Larceny_theft, x=crime_DF.Pop_Gp, name='Larceny_theft',
                     boxpoints='all', jitter=0.3, pointpos=-1.8))
fig.add_trace(go.Box(y=crime_DF.Motor_vehicle_theft, x=crime_DF.Pop_Gp, name='Motor_vehicle_theft',
                     boxpoints='all', jitter=0.3, pointpos=-1.8))
fig.update_layout(
    title='Property crime distribution',
    yaxis_title='crime per 100,000 inhabitant',
    boxmode='group' # group together boxes of the different traces for each value of x
)
fig.show()

# bar chart for 10 counties with lowest violent rate and 10 counties with highest violent rate
sorted_by_violent = crime_DF.sort_values(by='Violent').iloc[np.r_[0:10, -10:0]]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=sorted_by_violent.County,
    y=sorted_by_violent.Robbery,
    name='Robbery',
))
fig.add_trace(go.Bar(
    x=sorted_by_violent.County,
    y=sorted_by_violent.Rape,
    name='Rape'
))
fig.add_trace(go.Bar(
    x=sorted_by_violent.County,
    y=sorted_by_violent.Murder_and_nonnegligent_manslaughter,
    name='Murder_and_nonnegligent_manslaughter'
))
fig.add_trace(go.Bar(
    x=sorted_by_violent.County,
    y=sorted_by_violent.Aggravated_assault,
    name='Aggravated_assault'
))
fig.show()

# bar chart for 10 counties with lowest Property_crime rate and 10 counties with highest Property_crime rate

sorted_by_property = crime_DF.sort_values(by='Property_crime').iloc[np.r_[0:10, -10:0]]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=sorted_by_violent.County,
    y=sorted_by_violent.Burglary,
    name='Burglary',
))
fig.add_trace(go.Bar(
    x=sorted_by_violent.County,
    y=sorted_by_violent.Larceny_theft,
    name='Larceny_theft'
))
fig.add_trace(go.Bar(
    x=sorted_by_violent.County,
    y=sorted_by_violent.Motor_vehicle_theft,
    name='Motor_vehicle_theft'
))
fig.show()

# pie chart for violent crime
labels = ['Murder_and_nonnegligent_manslaughter',
           'Rape','Robbery', 'Aggravated_assault']
values = crime_DF.loc[:, labels].mean()
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig.show()