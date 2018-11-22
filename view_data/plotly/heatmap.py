'''
    Tutorial: https://plot.ly/python/heatmaps/
    Date: 22/11/2018
'''
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='rodriguesfas', api_key='8pbWwhm2biYm8ApskFCl')

trace = go.Heatmap(z=[[1, 20, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]],
                   x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                   y=['Morning', 'Afternoon', 'Evening'])
data=[trace]
py.iplot(data, filename='labelled-heatmap')