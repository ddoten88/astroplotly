from jupyter_dash import JupyterDash
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import pandas as pd
from kerykeion import CompositeAspects, KrInstance
# import chart_studio.plotly as py
import plotly
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import os
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots

from astrofunctions import *
#from layouts import *

# __________________________________________________________
import plotly
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
                    
import pandas as pd

#df = pd.read_csv('df.csv')


datelist = pd.date_range(start= '2003-01-01', end='2025-01-01', freq='W').tolist()
ref = KrInstance("Diane", 1988, 2, 16, 22, 28, "Lino Lakes")



import datetime
import pandas as pd
from datetime import datetime
maindf = pd.DataFrame([])
for i in datelist:
    YEAR = i.year
    MONTH = i.month
    DAY = i.day
    
    comparison = KrInstance("comp", YEAR, MONTH, DAY, 22, 28, "Lino Lakes")
    
    
    name = CompositeAspects(comparison, ref)
    aspect_list = name.get_relevant_aspects()
    al = pd.DataFrame(aspect_list).rename(columns={'p1_name':'transit','p2_name':'natal'})
    al['date'] = i
    al['year'] = YEAR
    al['month'] = MONTH
    maindf = pd.concat((maindf, al))
maindf['intensity'] = pd.cut(abs(maindf['orbit']),bins=[0,1,5,10,15], labels=[100,50,10,1])
maindf['intensity'] = maindf['intensity'].astype(float)
maindf['yearmonth']=maindf.apply(lambda x: str(x['year'])+"-"+str(x['month']), axis=1)


maindf['planetgroup'] = maindf['natal'].apply(lambda x: getplanetgroup(x))

maindf['aspectgroup'] = maindf['aspect'].apply(lambda x: getaspectgroup(x))




#df = return_filter(maindf, 'transit', 'Saturn', False)
def graph_heatmap(satslice):

    fig4 = go.Figure(
        go.Heatmap(x=satslice['yearmonth'],\
                   y=satslice['natal'],\
                   z=satslice['intensity'],\
                   xgap = 2,\
                   ygap = 2,\
                   colorscale='pubu'
        )
    )
    return fig4

def plot_bargraph(o):
    fig = go.Figure(px.bar(o,\
             x="date",\
             y="intensity",\
             color="natal",\
             hover_name="natal",\
             facet_row='aspect',\
             labels='natal',\
             width=1000, \
             height=1000,\
            opacity=1)
                   )
    return fig

import plotly.express as px
fig0 = px.bar(maindf,\
             x="date",\
             y="intensity",\
             color="natal",\
             hover_name="natal",\
             facet_row='aspect',\
             labels='natal',\
             width=1000, \
             height=1000,\
            opacity=1)


npg_selections = [{'label': i, 'value': i} for i in maindf['planetgroup'].unique()]
npg_selections.append({'label': 'ALL', 'value': 'ALL'})
                    
ag_selections = [{'label': i, 'value': i} for i in maindf['aspectgroup'].unique()]
ag_selections.append({'label': 'ALL', 'value': 'ALL'})
                    
transit_selections = [{'label': i, 'value': i} for i in maindf['transit'].unique()]
transit_selections.append({'label': 'ALL', 'value': 'ALL'})
                    
natal_selections = [{'label': i, 'value': i} for i in maindf['natal'].unique()]
natal_selections.append({'label': 'ALL', 'value': 'ALL'})
                    
aspect_selections = [{'label': i, 'value': i} for i in maindf['aspect'].unique()]
aspect_selections.append({'label': 'ALL', 'value': 'ALL'})
                    
friendlynames = ["no filter", "greater than 1 degree", "greater than 2 degrees", "greater than 3 degrees", "greater than 4 degrees", "greater than 5 degrees", ]
thresholds = [0, 1,2,3,4,5,10]
threshold_selections = [
    {"label": a, "value": b} for a, b in zip(friendlynames, thresholds)
]
threshold_selections.append({'label': 'ALL', 'value': 'ALL'})
LEFT_COLUMN = dbc.Container(
    [
        html.H3(children="TITLE", className="display-5"),
        html.Hr(className="my-2"),
        html.H4(children="Select groups", className="display-5"),
        html.Hr(className="my-2"),
        #html.Label("Select Natal Planet Group (primary or secondary)", className="lead"),
        dcc.Dropdown(
            id='npg-column',
            options=npg_selections,
            placeholder="Select Natal Planet Group Here",
            value='ALL',
            style={"marginBottom": 20, "font-size":12}
        ),
        
        html.Label("Select Aspect Group (easy or not)", className="lead"),
        dcc.Dropdown(
            id='ag-column',
            options=ag_selections,
            placeholder="Select Aspect Group Here",
            value='ALL',
            style={"marginBottom": 20, "font-size":12}
        ),
        
        html.Label("Select Transit Planet", className="lead"),
        dcc.Dropdown(
            id='transit-column',
            options=transit_selections,
            placeholder="Select Aspect Group Here",
            value='ALL',
            style={"marginBottom": 20, "font-size":12}
        ),
        

        html.Label("Select Natal PLanet", className="lead"),
        dcc.Dropdown(
            id='natal-column',
            options=natal_selections,
            placeholder="Select Aspect Group Here",
            value='ALL',
            style={"marginBottom": 20, "font-size":12}
        ),
        
        
        html.Label("Select Aspect", className="lead"),
        dcc.Dropdown(
            id='aspect-column',
            options=aspect_selections,
            placeholder="Select Aspect Group Here",
            value='ALL',
            style={"marginBottom": 20, "font-size":12}
        ),
        
        
        html.Label("Select aspect orb threshold", className="lead"),
        dcc.Dropdown(
            id="threshold-filter",
            options=threshold_selections,
            placeholder="Select an threshold",
            value='ALL',
            style={"marginBottom": 20, "font-size": 12},
        ),

    ],
)
                    

# header


# top plot
TOP_PLOT = [
    dbc.CardHeader(html.H5("FORECASTS")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-hist",
                children=[
                    dbc.Alert(
                        "Not enough data to render this plot, please adjust the filters",
                        id="no-data-alert-bank",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dcc.Graph(
                        id="indicator-graphic",
                        figure=fig0,
                        config={
                            "scrollZoom": True,
                            "modeBarButtonsToRemove": [
                                "pan2d",
                                "select2d",
                                "lasso2d",
                                "resetScale2d",
                                "hoverClosestCartesian",
                                "hoverCompareCartesian",
                            ],
                        },
                    ),

                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

BOTTOM_PLOT = [
    dbc.CardHeader(html.H5("TOTALS")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-hist2",
                children=[
                    dbc.Alert(
                        "Not enough data to render this plot, please adjust the filters",
                        id="no-data-alert-bank2",
                        color="warning",
                        style={"display": "none"},
                    ),
                    
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


BODY = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(LEFT_COLUMN, md=10, align="center"),
            ],
            style={"marginTop": 30},
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(TOP_PLOT, md=4, width=25),
            ],
            style={"marginTop": 30},
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(dbc.Card(BOTTOM_PLOT), md=12, width=25),
            ],
            style={"marginTop": 30},
        ),
    ],
    className="mt-12",
)
app = JupyterDash(__name__)
#app = dash.Dash(
 #   __name__,
#)

server = app.server
app.layout = html.Div(children=[BODY])

@app.callback(
    [
        Output("indicator-graphic", "figure"),

    ],
    [Input("npg-column", "value")],
    [Input("ag-column", "value")],
    [Input("transit-column", "value")],
    [Input("natal-column", "value")],
    [Input("aspect-column", "value")],
    [Input("threshold-filter", "value")],
)
def update_graph_1(planetgroup, aspectgroup, transit, natal, aspect, orbthreshold):
    df = maindf.copy()
    cols = ['transit', 'p1_abs_pos', 'natal', 'p2_abs_pos', 'aspect', 'orbit',
       'aspect_degrees', 'color', 'aid', 'diff', 'p1', 'p2', 'date', 'year',
       'month', 'intensity', 'yearmonth', 'planetgroup', 'aspectgroup']
    planetgroups = return_filter(df, 'planetgroup', planetgroup, False)
    aspectgroups = return_filter(df, 'aspectgroup', aspectgroup, False)
    transita = return_filter(df, 'transit', transit, False)
    aspecta = return_filter(df, 'aspect', aspect, False)
    natala = return_filter(df, 'natal', natal, False)
    orb = return_filter(df, 'orbit', orbthreshold, True)
                    
    #frameList = [planetgroups, aspectgroups, transita, aspecta, natala, orb]
    try:
        
        only = planetgroups.merge(aspectgroups, on=cols, how='inner')\
        .merge(aspectgroups, on=cols, how='inner')\
        .merge(transita, on=cols, how='inner')\
        .merge(aspecta, on=cols, how='inner')\
        .merge(natala, on=cols, how='inner')\
        #.merge(orb, on=cols, how='inner')\
        #.reset_index(drop=True)

        print(only.shape)

        fig = graph_heatmap(only)
        return fig
    
    except Exception as e:
        print(e)
        fig_none = generate_blank_graph()
        return fig_none

    
    







if __name__ == "__main__":
    app.run_server(debug=True)
        







