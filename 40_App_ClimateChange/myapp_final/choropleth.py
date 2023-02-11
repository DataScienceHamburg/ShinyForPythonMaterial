#%%
import pandas as pd
import numpy as np
#%% Load online dataset 
online_dataset_path = 'https://public.opendatasoft.com/explore/dataset/covid-19-pandemic-worldwide-data/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B'
df = pd.read_csv(online_dataset_path, sep=';')

# Columns renaming
df.columns = [col.lower() for col in df.columns]

# Filtering
df = df[df['date']=='2020-11-19'].drop('date', axis=1)
df = df[df['category']=='Confirmed'].drop('category', axis=1)

# Droping unnecessary colunms
df = df[['zone', 'count']]

# Aggregating by Zone
df = df.groupby('zone').sum()
df = df.reset_index(drop=False)

# Displaying result
df.head()
#%%
import json
world_path = f"data/custom.geo.json"
with open(world_path, encoding='UTF-8') as f:
    geo_world = json.load(f)

# Instanciating necessary lists
found = []
missing = []
countries_geo = []

# For simpler acces, setting "zone" as index in a temporary dataFrame
tmp = df.set_index('zone')

# Looping over the custom GeoJSON file
for country in geo_world['features']:
    
    # Country name detection
    country_name = country['properties']['name'] 
    
    # Checking if that country is in the dataset
    if country_name in tmp.index:
        
        # Adding country to our "Matched/found" countries
        found.append(country_name)
        
        # Getting information from both GeoJSON file and dataFrame
        geometry = country['geometry']
        
        # Adding 'id' information for further match between map and data 
        countries_geo.append({
            'type': 'Feature',
            'geometry': geometry,
            'id':country_name
        })
        
    # Else, adding the country to the missing countries
    else:
        missing.append(country_name)

# Displaying metrics
print(f'Countries found    : {len(found)}')
print(f'Countries not found: {len(missing)}')
geo_world_ok = {'type': 'FeatureCollection', 'features': countries_geo}
# %%
geo_world_ok
# %%
country_conversion_dict = {
    'Bosnia and Herz.': 'Bosnia and Herzegovina',
    'Central African Rep.': 'Central African Republic',
    'Congo': 'Congo (Kinshasa)',
    "Côte d'Ivoire": "Cote d'Ivoire",
    'Czech Rep.' :  'Czechia',
    'Dem. Rep. Congo': 'Congo (Brazzaville)',
    'Dominican Rep.':'Dominican Republic',
    'Eq. Guinea':'Equatorial Guinea',
    'Korea': 'Korea, South',
    'Lao PDR':'Laos',
    'Myanmar':'Burma',
    'S. Sudan':'South Sudan',
    'Somaliland':'Somalia',
    'Taiwan':'Taiwan*',
    'United States' : 'US'  
}
# %%
df['count_color'] = df['count'].apply(np.log10)

# Get the maximum value to cap displayed values
max_log = df['count_color'].max()
max_val = int(max_log) + 1

# Prepare the range of the colorbar
values = [i for i in range(max_val)]
ticks = [10**i for i in values]
# %%
import plotly_express as px
# Create figure
fig = px.choropleth(
    df,
    geojson=geo_world_ok,
    locations='zone',
    color=df['count_color'],
    range_color=(0, df['count_color'].max()),
)

# Define layout specificities
fig.update_layout(
    margin={'r':0,'t':0,'l':0,'b':0},
    coloraxis_colorbar={
        'title':'Confirmed people',
        'tickvals':values,
        'ticktext':ticks        
    }
)

# Display figure
fig.show()
#%%