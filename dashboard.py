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
import dash_daq as daq
import matplotlib.pyplot as plt

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
from PIL import Image
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.VAPOR, dbc_css],
    title="👽Aliens in America",
    update_title="🛸🛸🛸...",
)

# create layout
app.layout = dbc.Container(
        [dbc.Row(
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
                [dbc.Col(
                    [
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        ThemeChangerAIO(
                                            aio_id="theme",
                                            radio_props={"value": dbc.themes.LUX},
                                        ),
                                        width=2,
                                    ),
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
                    html.H3("🛸What's the gender of Aliens?"),
                    dcc.Graph(id = "gender_pie")
                    ],
                    width=6,
                )]),
                html.H2("🛸Which type of Alien Sightings were there?"),
                dbc.Row([
                    dbc.Col(
                        daq.ToggleSwitch(id="type_graph_toogle", value=False, label="Histogram graph",
                        ),
                    
                    width=2,),
                dbc.Col(
                    dcc.Graph(id="type_graph", figure={}),
                    width=6,
                ),
                dbc.Col(
                    html.Img(src='assets/ufo-green.gif'),
                    width=4,
                ),
                ]
                )
        ,
        html.Br(),
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
        dbc.Row(
                [
                    html.Div(
                            [
                                html.H3("🛸How often do aliens feed?"),
                                dcc.Graph(id="feed_freq_graph", figure={}),
                            ]
                        )
                ]
        ),],
    fluid=True,
    className="dbc",
)

# ---------------------CALLBACKS---------------------
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
        title=  "Texas has highest no of 👽️ sightings." ,
        locations="state",
        color="count",
        hover_name="state",
        color_discrete_sequence=px.colors.sequential.Plasma,
        template=template_from_url(theme),
    )
    return fig

@app.callback(
    dash.dependencies.Output("gender_pie" ,"figure"),
    [
        dash.Input(ThemeChangerAIO.ids.radio("theme"), "value")
    ]
    )
def update_gender_graph(theme):
    new_df = pd.DataFrame(columns = ["Gender" , "Count"])
    new_df["Gender"] = combined_df.gender.value_counts().to_dict().keys()
    new_df["Count"] = combined_df.gender.value_counts().to_dict().values()
    fig = px.pie(new_df ,names = "Gender" , values = "Count",
            title = "There are lot of Female aliens 👯‍♀️" , 
            # color_discrete_sequence = px.colors.sequential.Plasma, 
            hole = 0.3,
            template = template_from_url(theme))
    return fig


@app.callback(
    dash.dependencies.Output("type_graph", "figure"),
    [
        dash.dependencies.Input("type_graph", "figure"),
        dash.dependencies.Input(ThemeChangerAIO.ids.radio("theme"), "value"),
        dash.dependencies.Input("type_graph_toogle" , "value")
    ],
)
def update_type_graph(value, theme, toggle_mode):
    types_df = pd.DataFrame(columns=["type", "count"])
    types_df["type"] = combined_df["type"].value_counts().to_dict().keys()
    types_df["count"] = combined_df["type"].value_counts().to_dict().values()
    if toggle_mode:
            fig = px.histogram(
                combined_df,
                x="type",
                color="type",
                title="👽️ Alien Sightings histogram by Type",
                template=template_from_url(theme),
                range_y = [8000, 11000],
            )
    else:
        fig = px.pie(
            types_df,
            values="count",
            names="type",
            title = "there are almost same % of 👽️ of each type" , 
            hole=0.3,
            color_discrete_sequence=px.colors.sequential.Plasma,
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
        title = "👽️ feeding frequency." , 
        template=template_from_url(theme),
        range_y=[5500, 7000],
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
    value_counts_df["year"] = (
        selected_df["birth_year"].value_counts().sort_index().to_dict().keys()
    )
    value_counts_df["count"] = (
        selected_df["birth_year"].value_counts().sort_index().to_dict().values()
    )
    max_count_val = value_counts_df.max()["count"]
    scatter_df = value_counts_df.query(f"count == {max_count_val}")

    fig = px.line(
        value_counts_df,
        x="year",
        y="count",
        title=f"👽️ per Year for type {value}", 
        # color_discrete_sequence=["green"],
        # opacity=0.5,
        template=template_from_url(theme),
    )
    fig.add_traces(
        go.Scatter(

            x=scatter_df["year"], y=scatter_df["count"], mode="markers", name = "maximum count"
            )
    )

    return fig




# ---------------------RUN APP---------------------
if __name__ == "__main__":
    app.run_server()
