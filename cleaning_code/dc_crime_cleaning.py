import requests
from pprint import pprint
import pandas as pd
import logging
import json
import numpy as np
from datetime import datetime

desired_width = 600
pd.set_option('display.width', desired_width)

# 'https://maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/MPD/MapServer/26/query?'
#                         'where=1%3D1&outFields=REPORT_DAT,SHIFT,METHOD,OFFENSE,NEIGHBORHOOD_CLUSTER,'
#                         'LATITUDE,LONGITUDE,START_DATE,END_DATE,BLOCK&outSR=4326&f=json'


base_url = 'https://maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/MPD/MapServer/26/query'

url_post = {
    'where':'1=1',
    'outFields':'REPORT_DAT,SHIFT,METHOD,OFFENSE,'
                'NEIGHBORHOOD_CLUSTER,LATITUDE,LONGITUDE,'
                'START_DATE,END_DATE,BLOCK',
    'outSR':'4326',
    'f':'json',
    'returnIdsOnly':'true'
}

res_ids = requests.get(base_url, url_post)

obj_ids = res_ids.json()['objectIds']
# pprint(obj_ids)


url_post['returnIdsOnly'] = 'false'

# split a list into evenly sized chunks
# ref :https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(l, n):
    'Yield successive n-sized chunks from l.'
    for i in range(0, len(l), n):
        yield l[i:i + n]

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = logging.FileHandler('log.txt')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

crime_df = pd.DataFrame()
for n, l in enumerate(chunks(obj_ids[36200:], 100)):
    url_post['objectIds'] = ','.join(str(i) for i in l)
    res_crimes = requests.get(base_url, url_post)
    try:
        obj_crimes = res_crimes.json()
        logger.info('Round ' + str(n) + ' succeeded.')
        for c in obj_crimes['features']:
            crime_df = crime_df.append(c['attributes'], ignore_index=True)
    except json.decoder.JSONDecodeError:
        logger.warning('Round '+str(n)+' failed.')
        break

crime_df.to_csv('raw_data/crime_df.csv')
crime_df = pd.read_csv('raw_data/crime_df.csv')

# with pd.option_context('display.max_columns', None):
#     # print(crime_df.iloc[:, 1:].astype(np.float).describe())
#     print(crime_df.head())

cols = ['START_DATE','END_DATE','SHIFT','LATITUDE','LONGITUDE',
        'BLOCK','OFFENSE','METHOD']
crime_df = crime_df[cols]

# check missing values
print(np.where(pd.isnull(crime_df)))
print('missing values in column', np.unique(np.where(pd.isnull(crime_df))[1]))
# end_date has missing values
# where is the missing values
not_null = pd.notnull(crime_df.END_DATE)
is_null = pd.isnull(crime_df.END_DATE)
## date in this df are all unix timestamp + 000 at end
## convert them to human-readable time
crime_df.START_DATE = (crime_df.START_DATE.values / 1000).astype(np.int)
crime_df.END_DATE.values[not_null] = (crime_df.END_DATE.values[not_null] / 1000).astype(np.int)


## Compute the average time between START_DATE and END_DATE.
t_mean = np.mean(crime_df.END_DATE.values[not_null] - crime_df.START_DATE.values[not_null]).astype(np.int)
crime_df.END_DATE.values[is_null] = (crime_df.START_DATE.values[is_null] + t_mean).astype(np.int)


## sort the df by start time
crime_df.sort_values(by='START_DATE', inplace=True)
print('number of negative start date:', np.sum(crime_df.START_DATE.values < 0))

## Next we want to check if the samples are between 1/1/2016 and 12/31/2016
start_time = datetime(2016, 1, 1, 0, 0, 0)
end_time = datetime(2017, 1, 1, 0, 0, 0)
start_dates = [datetime.fromtimestamp(t) for t in crime_df.START_DATE.values]
end_dates = [datetime.fromtimestamp(t) for t in crime_df.END_DATE.values]

crime_df.START_DATE = start_dates
crime_df.END_DATE = end_dates

true_time = [start_time<t<end_time for t in start_dates]

crime_df = crime_df[true_time]

crime_df.to_csv('cleaned_data/dc_crime_cleaned.csv')