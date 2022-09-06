# creating dashboard with plotly dash 
## IMPORTS
import dash 
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
import plotly.express as px 
import plotly.io as pio



#### PREPARE DATA
# read data
aliens = pd.read_csv("./data/aliens.csv")
details = pd.read_csv("./data/details.csv")
location = pd.read_csv("./data/location.csv")
# grouping all the 3 above dataframes into the one 
combined_df = pd.merge(aliens, details, left_on='id', right_on = "detail_id")
combined_df = pd.merge(combined_df, location, left_on='id', right_on = "loc_id")
# converting the state names to their abbreviations
combined_df['state'] = combined_df['state'].map({'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'})


# removing loc_id , detail_id and id columsn 
combined_df.drop(['loc_id', 'detail_id',  "id"], axis=1, inplace=True)

#### DASH APP
# create dash app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY, dbc_css])

# create layout
app.layout = html.Div([
    html.H1("Alien Dashboard",
            className="bg-primary text-white p-2 mb-2 text-center"),
    html.H3("Alien Sightings by State"),
    dcc.Graph(id="state_graph", figure={}),
    html.H3("Alien Sightings by Type"),
    dcc.Graph(id="type_graph", figure={}),

]
)

# create callbacks
@app.callback(
    dash.dependencies.Output("state_graph", "figure"),
    [dash.dependencies.Input("state_graph", "figure")],
)
def update_state_graph(value):
    # create choropleth 
    value_count_df = pd.DataFrame(columns =[ 'state', 'count'])
    value_count_df['state'] = combined_df['state'].value_counts().to_dict().keys()
    value_count_df['count'] = combined_df['state'].value_counts().to_dict().values()
    print(value_count_df.head())
    fig = px.choropleth(value_count_df, scope="usa",locationmode="USA-states", 
                        locations="state", color="count", hover_name="state",
                         color_discrete_sequence=px.colors.sequential.Plasma)
    return fig

@app.callback(
    dash.dependencies.Output("type_graph", "figure"),
    [dash.dependencies.Input("type_graph", "figure")],
)
def update_type_graph(value):
    fig = px.histogram(combined_df, x="type", color="type", title="Alien Sightings by Type")
    return fig

# run app
if __name__ == "__main__":
    app.run_server(debug=True)
