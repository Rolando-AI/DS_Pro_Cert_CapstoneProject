# Import required libraries
import pandas as pd
#import dash
from dash import html #import dash_html_components as html
from dash import dcc #import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
# The default select value is for ALL sites
# dcc.Dropdown(id='site-dropdown',...)
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    ],
                                    value='ALL',placeholder="place holder here",
                                    searchable=False
                                    ),
                                    html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0', 2500: '2500', 5000:'5000', 10000:'10000'},
                                value=[0, 10000]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                                Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df.groupby('Launch Site', as_index=False).count()
        fig = px.pie(data, values='class',
        names=data['Launch Site'],
        title='Total successful launches by Site')
        return fig
    else :
        data = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_count = data.groupby('class', as_index=False).count()
        fig = px.pie(success_count, values='Flight Number', 
        names=success_count['class'],
        title=f'Success vs Failure count for {entered_site}')
        return fig
        # return the outcome piechart for a selected site                                
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value'),
Input(component_id='payload-slider', component_property='value'))

def get_scat_plot(entered_site, entered_values):
    slider_data = spacex_df[
            (spacex_df['Payload Mass (kg)']>entered_values[0]) &
            (spacex_df['Payload Mass (kg)']<entered_values[1])
            ]    
    if entered_site == 'ALL':
        fig2 = px.scatter(slider_data, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category', title='Success vs Fail launches by Payload for All Sites')
        return fig2
    else :
        filtered_data = slider_data[slider_data['Launch Site'] == entered_site]
        fig2 = px.scatter(filtered_data, x='Payload Mass (kg)', y='class',
         color='Booster Version Category', title=f'Site {entered_site}: Success vs Fail launches by Payload')
        return fig2
        #return f'For site {entered_site}, the values are in the range of {entered_values[0]} and {entered_values[1]}'
# Run the app
if __name__ == '__main__':
    app.run_server()