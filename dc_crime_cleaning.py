import requests
from pprint import pprint
import pandas as pd
import logging
import json

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

