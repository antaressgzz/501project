import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go

chart_studio.tools.set_credentials_file(username='zz249', api_key='J3lMY1dU1FIpIz7u2w4D')

##Heatmap

trace = go.Heatmap(z=[[1, 20, 30],
                      [20, 1, 60],
                      [30, 60, 1]])
data=[trace]
#py.iplot(data, filename='basic-heatmap')
py.plot(data, filename = 'heatmap')



