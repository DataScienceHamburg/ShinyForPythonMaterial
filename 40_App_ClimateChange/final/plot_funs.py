#%% packages
import json
from pathlib import Path
import ipyleaflet as L
import numpy as np
from plotnine import ggplot, aes, geom_point, geom_smooth, coord_cartesian, labs, scale_color_discrete, theme_bw, coord_cartesian, theme, element_rect, element_line, annotate, geom_vline

def plot_world(temp, year):
    temp_filt = temp.loc[(temp['Year'] == year) & (temp['Months'] == 'January'), ['Country', 'Value', 'ISO3 Code']]
    world_path = Path(__file__).parent / "countries.geo.json"
    with open(world_path, encoding='UTF-8') as f:
        geo_world = json.load(f)

    #%% get all available countries from 'geo_world'
    geo_world_countries = {}
    for i in range(len(geo_world['features'])):
        current_country = geo_world['features'][i]['id']
        geo_world_countries[current_country] = 0  

    # prep data for temp
    country_temp = dict(zip(temp_filt['ISO3 Code'].tolist(), temp_filt['Value'].tolist()))


    for k in country_temp.keys():
        if k in geo_world_countries:
            # get the temperature for this key 'k'
            current_temperature = country_temp[k]
            geo_world_countries[k] = current_temperature

    #  Choropleth Graph
    layer = L.Choropleth(
        geo_data=geo_world,
        choro_data=geo_world_countries,
        colormap=L.linear.YlOrRd_04,
        border_color='black',
        value_min = -1, 
        value_max = 3
        )
    return layer



#%% plot specific country over time
def plot_country(temp, country = 'Germany', year = 1960):
    
    temp_filt = temp.loc[(temp['Country'] == country), ['Country', 'Year', 'Months','Value']]
    # group sum for all countries
    temp_filt_groupsum_all = temp.groupby(['Country', 'Year'])['Year','Value'].agg({'Value': np.median}).reset_index()
    
    # group sum for specified country
    temp_filt_groupsum = temp_filt.groupby('Year')['Year','Value'].agg({'Value': np.median}).reset_index()
    temp_filt_all_year = np.mean(temp_filt_groupsum_all.loc[temp_filt_groupsum_all['Year']==year, 'Value'])
    temp_filt_sel_year = np.mean(temp_filt_groupsum.loc[temp_filt_groupsum['Year']==year, 'Value'])
    temp_filt_groupsum['Country'] = country
    g = ggplot(data=temp_filt_groupsum_all) + aes(x='Year', y='Value') + geom_point(color='grey', alpha=0.1) + annotate('text', x=1985, y=2, label=f"All countries ({year}): {np.round(temp_filt_all_year, 1)} °C") + annotate('text', x=1985, y=2.5, label=f"Selected country ({year}): {np.round(temp_filt_sel_year, 1)} °C", color='red') + scale_color_discrete(guide=False) + geom_smooth() + geom_smooth(data=temp_filt_groupsum, color='red') + geom_vline(xintercept=year, linetype='dashed') + coord_cartesian(ylim = [-1, 4]) + labs(x = 'Year [-]', y='Temperature Change [deg C]', title=f'Temperature Change for {country}') + theme_bw() + coord_cartesian(ylim=[-1, 3]) + theme(
    plot_background=element_rect(fill='gray', alpha=0), panel_background=element_rect(fill='gray', alpha=0), 
    rect=element_rect(color='gray', size=0, fill='#EEBB0050'))
    return g
