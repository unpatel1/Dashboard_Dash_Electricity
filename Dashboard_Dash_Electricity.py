import imp
import dash
from dash import html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.express as px
import os

data_dir_path = os.path.dirname(__file__)

data_url = os.path.join(data_dir_path, 'electricity.csv')

electricity = pd.read_csv(data_url)

year_min = electricity['Year'].min()
year_max = electricity['Year'].max()

# avg_price_electricity = electricity.groupby(
#     'US_State')['Residential Price'].mean().reset_index()

# map_fig = px.choropleth(avg_price_electricity, locations = 'US_State', locationmode = 'USA-states',
#                         color = 'Residential Price', scope = 'usa', color_continuous_scale = 'reds')

app = dash.Dash(external_stylesheets = [dbc.themes.SOLAR])

app.layout = html.Div(children = [
    html.H1('Electricity Prices by US State'),
    dcc.RangeSlider(id = 'year-slider', min = year_min, max = year_max, value = [year_min, year_max],
                    marks = {i:str(i) for i in range(year_min, year_max + 1)}),
#    dcc.Graph(id = 'map-graph', figure = map_fig), # "figure = map_fig" is not necessary
    dcc.Graph(id = 'map-graph'),
#    html.Div(id = 'click-children'),
    dash_table.DataTable(id = 'price-info', columns = [{'name':col, 'id':col} for col in
                                                        electricity.columns])
#                                                        electricity.columns],
#                                                        data = electricity.to_dict('records'))
])

@app.callback(
    Output('map-graph', 'figure'),
    Input('year-slider', 'value')
)

def update_map_graph(selected_years):
    filtered_electricity = electricity[(electricity['Year'] >= selected_years[0]) &
                                       (electricity['Year'] <= selected_years[1])]
    avg_price_electricity = filtered_electricity.groupby(
        'US_State')['Residential Price'].mean().reset_index()
    map_fig = px.choropleth(avg_price_electricity, locations = 'US_State', locationmode = 'USA-states',
                            color = 'Residential Price', scope = 'usa', color_continuous_scale = 'reds')
    return map_fig

@app.callback(
#    Output('click-children', 'children'),
    Output('price-info', 'data'),
    Input('map-graph', 'clickData'),
    Input('year-slider','value')
)

def update_datatable(clicked_data, selected_years):
    if clicked_data is None:
        return []
    us_state = clicked_data['points'][0]['location']
    filtered_electricity = electricity[(electricity['Year'] >= selected_years[0]) &
                                       (electricity['Year'] <= selected_years[1]) &
                                       (electricity['US_State'] == us_state)]
    return filtered_electricity.to_dict('records')
#    return str(clicked_data)

# def print_click_data(clicked_data):
#    return clicked_data
#    return str(clicked_data)

if __name__=='__main__':
    app.run_server(debug = True)
    # debug=True: when developing the app
    # debug=False: when deployig the app to production

