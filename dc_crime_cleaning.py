import requests
from pprint import pprint
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
    'f':'json'
}


response = requests.get(base_url, url_post)

json_crime = response.json()
pprint(json_crime)
