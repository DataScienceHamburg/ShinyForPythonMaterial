#%% packages
from shiny import App, render, ui, reactive
from asyncio import sleep
from shinywidgets import output_widget, register_widget, reactive_read
import pandas as pd
import numpy as np
from pathlib import Path
import ipyleaflet as L
import json

from plotnine import ggplot, aes, geom_point, geom_smooth, coord_cartesian, labs, scale_color_discrete, theme_bw, coord_cartesian, theme, element_rect, element_line, annotate

#%% data prep
# temperatures = pd.read_csv(Path(__file__).parent / 'FAOSTAT_data_1-10-2022.csv')
# temperatures.rename(columns={'Area': 'Country'}, inplace=True)
# codes = pd.read_csv(Path(__file__).parent / 'FAOSTAT_data_11-24-2020.csv')
# codes = codes[['Country Code', 'ISO2 Code', 'ISO3 Code']]
# temperatures.rename(columns={'Area': 'Country'}, inplace=True)
# temperatures = temperatures.merge(codes, left_on='Area Code (FAO)', right_on='Country Code')
# temperatures.to_csv('temperatures.csv', index=False)
temperatures = pd.read_csv(Path(__file__).parent / 'temperatures.csv')

# values for dropdowns
countries = temperatures['Country'].unique().tolist()
temp_years = temperatures['Year'].unique()
temp_year_min = temp_years.min()
temp_year_max = temp_years.max()

#%% Function for Plotting World
def plot_world(temp, year):
    temp_filt = temp.loc[(temperatures['Year'] == year) & (temp['Months'] == 'January'), ['Country', 'Value', 'ISO3 Code']]
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
def plot_country(temp, country = 'Germany'):
    temp_filt = temp.loc[(temperatures['Country'] == country), ['Country', 'Year', 'Months','Value']]
    # group sum for all countries
    temp_filt_groupsum_all = temp.groupby(['Country', 'Year'])['Year','Value'].agg({'Value': np.median}).reset_index()
    # group sum for specified country
    temp_filt_groupsum = temp_filt.groupby('Year')['Year','Value'].agg({'Value': np.median}).reset_index()
    temp_filt_groupsum['Country'] = country
    g = ggplot(data=temp_filt_groupsum_all) + aes(x='Year', y='Value') + geom_point(color='grey', alpha=0.1) + annotate('text', x=1975, y=2.0, label='all countries', color='grey') + annotate('text', x=1975, y=2.5, label='selected country', color='red') + scale_color_discrete(guide=False) + geom_smooth() + geom_smooth(data=temp_filt_groupsum, color='red') + coord_cartesian(ylim = [-1, 4]) + labs(x = 'Year [-]', y='Temperature Change [deg C]', title=f'Temperature Change for {country}') + theme_bw() + coord_cartesian(ylim=[-1, 3]) + theme(
    plot_background=element_rect(fill='gray', alpha=0), panel_background=element_rect(fill='gray', alpha=0), 
    rect=element_rect(color='gray', size=0, fill='#EEBB0050'))
    return g

#%% Frontend
app_style = "background-color:#fff;"
font_style = "font-weight: 100;"
course_link_style = "text-align: center; font-weight: 100;"
app_ui = ui.page_fluid(
    ui.h2("Climate Change", style=font_style),
    
         
        ui.row(
            ui.column(6, ui.input_select("country", "Choose a County", countries, width="400px")),
            ui.column(6, ui.row(
                ui.column(6, ui.input_slider("year", "Choose a Year", temp_year_min, temp_year_max, 1)),
                ui.column(6, ui.output_ui('color_map') )
            )
                      )
        ),
        ui.row(
            ui.column(6, ui.output_plot('graph_country')),
            ui.column(6, output_widget('map')),
        ),
        ui.br(),
        ui.row(
            ui.column(6, ui.h5("Imprint", style = font_style)),
            ui.column(6, ui.p(f'Learn how this app is developed and deployed in my course:', style=font_style), style="text-align: center;")
            ),
        ui.row(
            
            ui.column(6, 
                      ui.row(
                ui.column(2, ui.img(src="developer.png", width="32px"), style="text-align: center;"),
                ui.column(10, ui.p('Bert Gollnick', style = font_style))
                ),
                      ui.row(
                ui.column(2, ui.img(src="address2.png", width="32px"), style="text-align: center;"),
                ui.column(10, ui.p('Redderblock 28', style = font_style))
                ),ui.row(
                ui.column(2, ),
                ui.column(10, ui.p('22145 Hamburg', style = font_style))
                ),
                ui.row(
                ui.column(2, ),
                ui.column(10, ui.p('Germany', style = font_style))
                ),
                      ui.row(
                ui.column(2, ui.img(src="mail2.png", width="32px"), style="text-align: center;"),
                ui.column(10, ui.a(ui.p('bert.gollnick@posteo.net'), href="mailto:bert.gollnick@posteo.net", style = font_style))
                ),
                      ),
            ui.column(6, ui.a(ui.img(src="course_logo_300x169.png"), href="https://www.udemy.com"), style="text-align: center;"
            )),
        ui.row(
            ui.column(6, ui.p("")),
            ui.column(6, ui.h5(ui.a('Shiny for Python Ultimate: Web Development with Python', href ="https://www.udemy.com", class_="help-link")), style=course_link_style)

    ), style= app_style
)


# Backend
def server(input, output, session):
    map = L.Map(center = (0,0), zoom = 1)
    # Add a distance scale
    map.add_control(L.leaflet.ScaleControl(position="bottomleft"))
    register_widget("map", map)
    
    # When the year changes, update the map's zoom attribute (2)
    @reactive.Effect
    def _():
        layer = plot_world(temperatures, input.year())
        map.add_layer(layer)
        
    @output
    @render.plot
    async def graph_country():
        g = plot_country(temperatures, input.country())
        with ui.Progress(min=1, max=15) as p:
            p.set(message="Calculation in progress", detail="Please wait...")
            for i in range(1, 15):
                p.set(i, message="Computing")
                await sleep(0.1)
        return g
    
    
    
    @output
    @render.ui
    def color_map() -> ui.Tag:
        img = ui.img(src="colormap.png")
        return img

www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=www_dir)
