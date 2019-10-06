import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

desired_width = 600
pd.set_option('display.width', desired_width)

input_file = 'raw_data/virginia.xls'

crime_va = pd.read_excel(input_file)

############### drop description rows and columns
crime_va.drop([0,1,2,3,4,100,101], axis=0, inplace=True)
crime_va.drop(['Table 8', 'Unnamed: 5'], axis=1, inplace=True)

############# set column names
columns = ['County', 'Violent', 'Murder_and_nonnegligent_manslaughter',
           'Rape','Robbery', 'Aggravated_assault', 'Property_crime',
           'Burglary', 'Larceny_theft', 'Motor_vehicle_theft', 'Arson', 'Population']
crime_va.columns = columns


########## clean county name and set index
crime_va.sort_values(by='County', inplace=True)
## remove if exist
s = ' County Police Department'
for n, c in enumerate(crime_va.County.values):
    if c.endswith(s):
        crime_va.County.values[n] = c[:-len(s)]
crime_va.index = np.arange(len(crime_va))

### change data store type
crime_va.iloc[:, 1:] = crime_va.iloc[:, 1:].astype(np.float)


### calculate crime rate (per 100,000 people)
for c in crime_va.columns[1:-1]:
    crime_va.loc[:, c] = crime_va.loc[:, c] / crime_va.iloc[:, -1] * 100000



with pd.option_context('display.max_columns', None):
    print(crime_va.iloc[:, 1:].astype(np.float).describe())
    print(crime_va.head())

# boxplot for population
fig = go.Figure()
fig.add_trace(go.Box(y=crime_va.Population, name='Population', boxpoints='all',jitter=0.3,pointpos=-1.8))
fig.show()

# The boxplot for population is highly squeezed, population in different counties vary significantly
# we may consider dividing all the counties in the following groups:
# A: population > 20,000
# B: 20,000 >=  population


crime_va.loc[crime_va.Population.values<=20000, 'Pop_Gp'] = 'B'
crime_va.loc[(crime_va.Population.values>20000), 'Pop_Gp'] = 'A'
print('Number of counties in group A:', sum(crime_va.Population.values>20000))
print('Number of counties in group B:', sum(crime_va.Population.values<=20000))

# check distribution of different violent crime types
fig = go.Figure()
fig.add_trace(go.Box(y=crime_va.Rape, x=crime_va.Pop_Gp, name='Rape', boxpoints='all',jitter=0.3,pointpos=-1.8))
fig.add_trace(go.Box(y=crime_va.Robbery, x=crime_va.Pop_Gp, name='Robbery',boxpoints='all',jitter=0.3,pointpos=-1.8))
fig.add_trace(go.Box(y=crime_va.Murder_and_nonnegligent_manslaughter, x=crime_va.Pop_Gp,
                     name='Murder_and_nonnegligent_manslaughter', boxpoints='all',jitter=0.3,pointpos=-1.8))
fig.add_trace(go.Box(y=crime_va.Aggravated_assault, x=crime_va.Pop_Gp,
                     name='Aggravated_assault', boxpoints='all',jitter=0.3,pointpos=-1.8))
fig.update_layout(
    title='Violent crime distribution',
    yaxis_title='crime per 100,000 inhabitant',
    boxmode='group' # group together boxes of the different traces for each value of x
)
fig.show()



# check distribution of different property crime types
fig = go.Figure()
fig.add_trace(go.Box(y=crime_va.Burglary, x=crime_va.Pop_Gp, name='Burglary',
              boxpoints='all',jitter=0.3,pointpos=-1.8))
fig.add_trace(go.Box(y=crime_va.Larceny_theft, x=crime_va.Pop_Gp, name='Larceny_theft',
              boxpoints='all',jitter=0.3,pointpos=-1.8))
fig.add_trace(go.Box(y=crime_va.Motor_vehicle_theft, x=crime_va.Pop_Gp, name='Motor_vehicle_theft',
              boxpoints='all',jitter=0.3,pointpos=-1.8))
fig.update_layout(
    title='Property crime distribution',
    yaxis_title='crime per 100,000 inhabitant',
    boxmode='group' # group together boxes of the different traces for each value of x
)
fig.show()

# bar chart for 10 counties with lowest violent rate and 10 counties with highest violent rate
sorted_by_violent = crime_va.sort_values(by='Violent').iloc[np.r_[0:10, -10:0]]

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

sorted_by_property = crime_va.sort_values(by='Property_crime').iloc[np.r_[0:10, -10:0]]

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
values = crime_va.loc[:, labels].mean()
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig.show()