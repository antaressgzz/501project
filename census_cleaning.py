from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import warnings

base_url = 'https://www.census.gov/quickfacts/geo/chart/ameliacountyvirginia/'
url_h_grad = 'EDU635217', 'h_grad'
url_b_grad = 'EDU685217', 'b_grad'
url_o_occ_r = 'HSG445217', 'o_occ_r'
url_o_occ_mv = 'HSG445217', 'o_occ_mv'
url_o_m_cst = 'HSG650217', 'o_m_cst'
url_gos_ret = 'HSG860217', 'gos_ret'
url_ps_pr_hh = 'HSD310217', 'ps_pr_hh'
url_lv_sm = 'POP715217', 'lv_sm'
url_tvl_t = 'LFE305217', 'tvl_t'
url_ps_pvt = 'IPE120218', 'ps_pvt'
url_emp_chg = 'BZA115216', 'emp_chg'

all_url = [url_h_grad, url_b_grad, url_o_occ_r, url_o_occ_mv,
           url_o_m_cst, url_gos_ret,url_ps_pr_hh,url_lv_sm,url_tvl_t, url_emp_chg]

for i in range(len(all_url)):
    all_url[i] = base_url + all_url[i][0], all_url[i][1]

def census_data(url_list):
    census_df = pd.DataFrame()
    for url, var_name in url_list:
        page = urlopen(url)
        soup = BeautifulSoup(page, 'lxml')
        d_list = [d for d in list(soup.find(class_='qf-graph-scroll').strings) if d != '\n' and d != '1']
        # print(len(d_list))
        Counties = d_list[::2]
        data = d_list[1::2]
        # print(Counties)
        # print(len(data))
        if 'County' in census_df.columns.values:
            print(var_name)
            if (census_df.County.values == Counties).all():
                census_df.loc[:, var_name] = data
            else:
                warnings.warn('The counties do not match.')
        else:
            census_df.loc[:, 'County'] = Counties
            census_df.loc[:, var_name] = data
    return census_df


census_df = census_data(all_url)


