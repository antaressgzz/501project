from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import warnings

base_url = 'https://www.census.gov/quickfacts/geo/chart/ameliacountyvirginia/'
url_h_grad = 'EDU635217', 'h_grad' # high school graduation rate
url_b_grad = 'EDU685217', 'b_grad' # bachelor percentage
url_o_occ_r = 'HSG445217', 'o_occ_r' # owner-occupied house rate
url_o_occ_mv = 'HSG445217', 'o_occ_mv' # owner-occupied house mean value
url_o_m_cst = 'HSG650217', 'o_m_cst' # Median selected monthly owner costs -with a mortgage
url_gos_ret = 'HSG860217', 'gos_ret' # median gross rent
url_ps_pr_hh = 'HSD310217', 'ps_pr_hh' # Persons per household
url_lv_sm = 'POP715217', 'lv_sm' # live in same house in past 1 year
url_tvl_t = 'LFE305217', 'tvl_t' # average travel time to work
url_ps_pvt = 'IPE120218', 'ps_pvt' # poverty rate
url_emp_chg = 'BZA115216', 'emp_chg' # employment change

all_url = [url_h_grad, url_b_grad, url_o_occ_r, url_o_occ_mv,
           url_o_m_cst, url_gos_ret,url_ps_pr_hh,url_lv_sm,url_tvl_t, url_emp_chg]

for i in range(len(all_url)):
    all_url[i] = base_url + all_url[i][0], all_url[i][1]

def scraping_census_data(url_list):
    census_df = pd.DataFrame()
    # each iteration scrape one variable in the given url list
    for url, var_name in url_list:
        page = urlopen(url)
        soup = BeautifulSoup(page, 'lxml')
        # web scraping
        d_list = [d for d in list(soup.find(class_='qf-graph-scroll').strings) if d != '\n' and d != '1']
        # print(len(d_list))
        Counties = d_list[::2]
        data = d_list[1::2]
        # print(Counties)
        # print(len(data))
        if 'County' in census_df.columns.values:
            # print(var_name)
            if (census_df.County.values == Counties).all():
                census_df.loc[:, var_name] = data
            else:
                # if the counties order change
                warnings.warn('The counties do not match.')
        else:
            census_df.loc[:, 'County'] = Counties
            census_df.loc[:, var_name] = data
    return census_df

# scraped data
census_df = scraping_census_data(all_url)

census_df.to_csv('raw_data/census_raw.csv')



