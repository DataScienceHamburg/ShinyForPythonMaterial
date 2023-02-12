#%% Package imports
from shiny import App, render, ui, reactive
import pandas as pd
import numpy as np
from pathlib import Path
from plotnine import ggplot, aes, geom_line, theme, element_text, labs

#%% Data Preparation
languages = pd.read_csv(Path(__file__).parent /'MostPopularProgrammingLanguages.csv')
languages['datetime'] = pd.to_datetime(languages['Date'])
languages.drop(axis=1, columns=['Date'], inplace=True)

languages_long = languages.melt(id_vars='datetime', value_name='popularity', var_name='language').reset_index(drop=True)


date_range_start = np.min(languages_long['datetime'])
date_range_end = np.max(languages_long['datetime'])

language_names = languages_long['language'].unique()
languages_names_dict = {l:l for l in language_names}

#%%
app_ui = ui.page_fluid(
    ui.panel_title("Most Popular Programming Languages"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_selectize(id="language", label="Languages", choices=languages_names_dict, selected='Python', multiple=True),
            ui.input_date_range(id='date_range', label='Date Range', start=date_range_start, end=date_range_end),
        ),
        ui.panel_main(
            ui.output_plot("plotTimeseries"),
        )
    ),
)

def server(input, output, session):
    
    @reactive.Calc
    def lang_filt():
        date_selected_start = pd.to_datetime(input.date_range()[0])
        date_selected_end = pd.to_datetime(input.date_range()[1])
        lang_filt = languages_long.loc[(languages_long['language'].isin(list(input.language()))) & (languages_long['datetime']>= date_selected_start) & (languages_long['datetime']<= date_selected_end)].reset_index(drop=True)
        return lang_filt
    
    @output
    @render.plot
    def plotTimeseries():
        
        g = ggplot(lang_filt()) + aes(x = 'datetime', y='popularity', color='language') + geom_line() + theme(axis_text_x=element_text(rotation=90, hjust=1)) + labs(x ='Date', y='Popularity [%]', title='Popularity over Time')
        return g


app = App(app_ui, server)
