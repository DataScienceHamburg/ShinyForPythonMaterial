#%% packages
import pandas as pd
import numpy as np
from pathlib import Path
import ipyleaflet
import json
# %% data import
temperatures = pd.read_csv('FAOSTAT_data_1-10-2022.csv')
codes = pd.read_csv('FAOSTAT_data_11-24-2020.csv')
codes = codes[['Country Code', 'ISO2 Code', 'ISO3 Code']]
temperatures.rename(columns={'Area': 'Country'}, inplace=True)
temperatures = temperatures.merge(codes, left_on='Area Code (FAO)', right_on='Country Code')

#%% correct some names
#%%
temp_filt = temperatures.loc[(temperatures['Year'] == 1961) & (temperatures['Months'] == 'January'), ['Country', 'ISO3 Code','Value']]
temp_filt.reset_index(inplace=True)


# %% prepare geo-data
world_path = f"countries.geo.json"
with open(world_path, encoding='UTF-8') as f:
    geo_world = json.load(f)

#%% get all available countries from 'geo_world'
geo_world_countries = {}
for i in range(len(geo_world['features'])):
    current_country = geo_world['features'][i]['id']
    geo_world_countries[current_country] = 0  

#%% prep data for temp
country_temp = dict(zip(temp_filt['ISO3 Code'].tolist(), temp_filt['Value'].tolist()))

#%%
for k in country_temp.keys():
    if k in geo_world_countries:
        # get the temperature for this key 'k'
        current_temperature = country_temp[k]
        geo_world_countries[k] = current_temperature



# %% Choropleth Graph
layer = ipyleaflet.Choropleth(
    geo_data=geo_world,
    choro_data=geo_world_countries,
    colormap=ipyleaflet.linear.YlOrRd_04,
    border_color='black',
    )

m = ipyleaflet.Map(center = (0,0), zoom = 1)
m.add_layer(layer)
m
# %% create function
def create_world_map(temp_filt):
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
    layer = ipyleaflet.Choropleth(
        geo_data=geo_world,
        choro_data=geo_world_countries,
        colormap=linear.YlOrRd_04,
        border_color='black',
        )

    m = ipyleaflet.Map(center = (0,0), zoom = 1)
    m.add_layer(layer)
    return m

#%%
create_world_map(temp_filt)
# %%
color_map = pd.DataFrame({'values': np.linspace(-1, 4, 16)},
                         'colors':)

ggplot(temp_filt) + aes(x=, y=1) + geom_point()
# %%
linear.YlOrRd_04
# %%
import seaborn as sns
import ipyleaflet as L
sns.palplot(sns.color_palette(L.linear.YlOrRd_04.colors))
# %%
