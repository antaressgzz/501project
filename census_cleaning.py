from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url_h_grad = 'https://www.census.gov/quickfacts/geo/chart/arlingtoncdpvirginia/EDU635217'
# url_b_grad = 'https://www.census.gov/quickfacts/geo/chart/arlingtoncdpvirginia/EDU685217'



def census_data(url_list):
    census_df = pd.DataFrame()
    for url in url_list:
        page = urlopen(url)
        soup = BeautifulSoup(page, 'lxml')
        d_list = [d for d in list(soup.find(class_='qf-graph-scroll').strings) if d != '\n']
        Counties = d_list[::2]
        data = d_list[1::2]
        census_df.loc[:, 'County'] = Counties
        census_df.loc[:, 'data'] = data
    return census_df

df = census_data([url_h_grad])


