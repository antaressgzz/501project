import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff


desired_width = 600
pd.set_option('display.width', desired_width)

input_file = 'raw_data/mobility_2012_2016.xlsx'

mobility_va_ori = pd.read_excel(input_file, sheet_name='Virginia', header=1)
mobility_md_ori = pd.read_excel(input_file, sheet_name='Maryland', header=1)
mobility_va = mobility_va_ori.copy()
mobility_md = mobility_md_ori.copy()

##################### extract useful data #####################
mobility_va = mobility_va.loc[:, ['FIPS County Code of Geography A',
                                  'County Name of Geography A', 'County Name of Geography B',
                                  'Flow from Geography B to Geography A', 'Counterflow from Geography A to Geography B1']]
mobility_va.drop([0, 18817, 18818,18819,18820,18821], axis=0, inplace=True)
mobility_va.columns = ['FIPS','County', 'County2', 'In', 'Out']
mobility_md = mobility_md.loc[:, ['FIPS County Code of Geography A',
                                  'County Name of Geography A', 'County Name of Geography B',
                                  'Flow from Geography B to Geography A', 'Counterflow from Geography A to Geography B1']]
mobility_md.drop([0, 6094,6095,6096,6097,6098], axis=0, inplace=True)
mobility_md.columns = ['FIPS','County', 'County2', 'In', 'Out']
###############################################################

# with pd.option_context('display.max_columns', None):
#     print(mobility_va.head(10))
#     print(mobility_va.tail(10))

##################### create df with new features #####################
def fe_gen(df, state_fips):
    s1 = 'County'
    s2 = 'city'
    agg_flows = []
    all_areas = pd.unique(df.County.values)
    for area in all_areas:
        area_df = df.loc[df['County']==area]
        area_dic = {}
        area_dic['FIPS'] = state_fips+ str(int(area_df.FIPS.values[0])).zfill(3)
        if area.endswith(s2):
            area_dic['County'] = area
        if area.endswith(s1):
            area_dic['County'] = area[:-7]
        outflow = np.sum(area_df['Out'])
        overseas = np.sum(area_df.loc[area_df['County2']=='-','In'])
        inflow = np.sum(area_df['In']) - overseas
        area_dic['mob_ratio'] = inflow / outflow
        area_dic['os_ratio'] = overseas / inflow
        agg_flows.append(area_dic)
    return pd.DataFrame.from_dict(agg_flows)

mob_va_cleaned = fe_gen(mobility_va, '051')
mob_md_cleaned = fe_gen(mobility_md, '024')
mob_va_cleaned.to_csv('cleaned_data/mob_va_cleaned.csv')
mob_va_cleaned.to_csv('cleaned_data/mob_md_cleaned.csv')
#################################################################

##################### boxplot ####################
# fig = go.Figure()
# fig.add_trace(go.Box(y=mob_va_cleaned.mob_ratio, name='in/out', boxpoints='all',jitter=0.3,pointpos=-1.8))
# fig.add_trace(go.Box(y=mob_va_cleaned.os_ratio, name='overseas/in', boxpoints='all',jitter=0.3,pointpos=-1.8))
# fig.update_layout(
#     title='ratio boxlpot',
#     yaxis_title='ratio'
# )
# fig.show()

##### boxplot shows tha there is a in/out ratio extremely higher than majority
##### we check what happened
# with pd.option_context('display.max_columns', None):
#     print(mob_va_cleaned.sort_values(by='mob_ratio').iloc[-5:])

### Norton city has in/out ratio of 10.5, significant higher than 50% quantil, which is 1
### After checking the origin data, we may believe there is no incorrectness, consistency about this sample
### We decide to believe this outlier is correct
###############################################################


############ Choropleth for mobility ############
fig = ff.create_choropleth(fips=mob_va_cleaned.FIPS, values=mob_va_cleaned.mob_ratio,
                           scope=['VA'], binning_endpoints=[0.3, 0.8, 1, 1.2, 1.6],
                           county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
                           legend_title='Mobility by County', title='Mobility by Counties in VA')
fig.layout.template = None
fig.show()

fig = ff.create_choropleth(fips=mob_md_cleaned.FIPS, values=mob_md_cleaned.mob_ratio,
                           scope=['MD'], binning_endpoints=[0.3, 0.8, 1, 1.2, 1.6],
                           county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
                           legend_title='Mobility by County', title='Mobility by Counties in MD')
fig.layout.template = None
fig.show()
#######################################################
