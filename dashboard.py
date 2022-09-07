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
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url


#### PREPARE DATA
# read data
aliens = pd.read_csv("./data/aliens.csv")
details = pd.read_csv("./data/details.csv")
location = pd.read_csv("./data/location.csv")
# grouping all the 3 above dataframes into the one
combined_df = pd.merge(aliens, details, left_on="id", right_on="detail_id")
combined_df = pd.merge(combined_df, location, left_on="id", right_on="loc_id")
# converting the state names to their abbreviations
combined_df["state"] = combined_df["state"].map(
    {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
    }
)


# removing loc_id , detail_id and id columsn
combined_df.drop(["loc_id", "detail_id", "id"], axis=1, inplace=True)

#### DASH APP
# create dash app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR, dbc_css], title = "👽Aliens in America" , update_title ="🛸🛸🛸...")

# create layout
app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        "Aliens in America Dashboard 🛸",
                        className="bg-primary text-white p-2 mb-2 text-center",
                    ),
                    width=12,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Col(ThemeChangerAIO(aio_id="theme", radio_props = {"value":dbc.themes.LUX}), width=2),
                                    dbc.Col(
                                        html.H3("🛸Alien Sightings Statewise"), width=4
                                    ),
                                ]
                            )
                        ),
                        dcc.Graph(id="state_graph", figure={}),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3("🛸How often do aliens feed?"),
                                dcc.Graph(id="feed_freq_graph", figure={}),
                            ]
                        )
                    ],
                    width=6,
                ),
                html.H3("🛸Which type of Alien Sightings were there?"),
                html.Div(
                    dcc.Graph(id="type_graph", figure={}),
                ),
            ]
        ),
        dbc.Row(
            [
                html.H2("🛸How many aliens of selected types appeared in each year?"),
                html.H3("Select the type of aliens"),
                dbc.Col(
                    dcc.Dropdown(
                        id="alien_type_select",
                        options=combined_df.type.unique().tolist(),
                        value="Reptile",
                    ),
                    width=6,
                ),
                dcc.Graph(id="aliens_per_year_graph", figure={}),
            ]
        ),
    ]
)

# create callbacks
@app.callback(
    dash.dependencies.Output("state_graph", "figure"),
    [
        dash.dependencies.Input("state_graph", "figure"),
        dash.Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    ],
)
def update_state_graph(value, theme):
    # create choropleth
    value_count_df = pd.DataFrame(columns=["state", "count"])
    value_count_df["state"] = combined_df["state"].value_counts().to_dict().keys()
    value_count_df["count"] = combined_df["state"].value_counts().to_dict().values()
    fig = px.choropleth(
        value_count_df,
        scope="usa",
        locationmode="USA-states",
        locations="state",
        color="count",
        hover_name="state",
        color_discrete_sequence=px.colors.sequential.Plasma,
        template=template_from_url(theme),
    )
    return fig


@app.callback(
    dash.dependencies.Output("type_graph", "figure"),
    [
        dash.dependencies.Input("type_graph", "figure"),
        dash.dependencies.Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    ],
)
def update_type_graph(value, theme):
    fig = px.histogram(
        combined_df,
        x="type",
        color="type",
        title="Alien Sightings by Type",
        template=template_from_url(theme),
    )
    return fig


@app.callback(
    dash.dependencies.Output("feed_freq_graph", "figure"),
    [
        dash.dependencies.Input("feed_freq_graph", "figure"),
        dash.dependencies.Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    ],
)
def update_feed_freq_graph(value, theme):
    fig = px.histogram(
        combined_df,
        x="feeding_frequency",
        template=template_from_url(theme),
    )
    return fig


@app.callback(
    dash.dependencies.Output("aliens_per_year_graph", "figure"),
    [
        dash.dependencies.Input("alien_type_select", "value"),
        dash.dependencies.Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    ],
)
def update_aliens_per_year_graph(value, theme):
    # selecting the df for reuiqred type
    selected_df = combined_df[combined_df["type"] == value]
    value_counts_df = pd.DataFrame(columns=["year", "count"])
    value_counts_df["year"] = selected_df["birth_year"].value_counts().to_dict().keys()
    value_counts_df["count"] = (
        selected_df["birth_year"].value_counts().to_dict().values()
    )
    fig = px.histogram(
        value_counts_df,
        x="year",
        y="count",
        title=f"Aliens per Year for type {value}",
        color_discrete_sequence=["indianred"],
        opacity=0.5,
        template=template_from_url(theme),
    )
    return fig


# run app
if __name__ == "__main__":
    app.run_server(debug=True)
