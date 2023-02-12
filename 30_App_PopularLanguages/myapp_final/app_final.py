#%% packages
from shiny import Inputs, Outputs, Session, App, reactive, render, req, ui
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_line, theme, element_text, labs
from pathlib import Path
#%% data prep
# data source: https://www.kaggle.com/datasets/muhammadkhalid/most-popular-programming-languages-since-2004
# final result is hosted on https://gist.github.com/SmartDataWithR/5dd3c152b5353f01730a1a2fe1fb308b

languages = pd.read_csv(Path(__file__).parent / 'MostPopularProgrammingLanguages.csv')

languages['datetime'] = pd.to_datetime(languages['Date'])
languages.drop(axis=1, columns=['Date'], inplace=True)  # Date column not required anymore

#%% set up input values
languages_long = languages.melt(id_vars='datetime', value_name='popularity', var_name='language').reset_index(drop=True)

date_range_start = np.min(languages_long['datetime'])
date_range_end = np.max(languages_long['datetime'])

#%%
# languages.info()
# languages.describe()

#%% values for dropdown field
language_names = languages_long['language'].unique()
langugage_names_dict = {l:l for l in language_names}
#%% sample graph
# ggplot(languages_long.loc[languages_long['language'].isin(['Python','R'])], aes('datetime', 'popularity', color='language')) + geom_line() 

#%% app
app_ui = ui.page_fluid(
    ui.panel_title('Most Popular Programming Languages'),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_selectize(id="language", label="Languages", choices=langugage_names_dict, selected='Python', multiple=True),
            ui.input_date_range(id='date_range', label='Date Range', start=date_range_start, end=date_range_end, ),
            
        ),
        ui.panel_main(
            ui.output_plot("plotTimeseries"),
            
        ),
        
), 
   ui.h6('Imprint'),
   ui.p('Bert Gollnick, Redderblock 28, 22145 Hamburg'),
   ui.a(ui.p('bert.gollnick@posteo.net'), href='mailto:bert.gollnick@posteo.net')
    )


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc
    def languages_filt():
        date_selected_start = str(input.date_range()[0])
        date_selected_end = str(input.date_range()[1])
        l = languages_long.loc[(languages_long['language'].isin(list(input.language()))) & (languages_long['datetime']>= date_selected_start) & (languages_long['datetime']<= date_selected_end)]
        return l.reset_index(drop=True)


    @output
    @render.plot
    def plotTimeseries():
        g = ggplot(languages_filt(), aes('datetime', 'popularity', color='language')) + geom_line() + theme(axis_text_x=element_text(rotation=90, hjust=1)) + labs(x = 'Date', y='Popularity [%]', title='Popularity over Time')
        return g

app = App(app_ui, server)

# %%