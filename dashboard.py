'''DashBoard para apresentação do Projeto Integrador - Digital House 2021------

---------Grupo 7: Daiane Ucceli Kreitlow & Rodney Soares-----------------------

------------ Importação das bibliotecas necessárias: --------------------------'''


import numpy as np
import pandas as pd
import json

# ------------imports dos componentes Dash  -----------------------------------
import dash
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
from dash_html_components.H3 import H3
from dash_html_components.H5 import H5
from dash_html_components.H1 import H1
from dash_html_components.Hr import Hr
import plotly.express as px
import plotly.graph_objects as go
from _plotly_utils.exceptions import PlotlyDataTypeError

CENTER_LAT, CENTER_LON = -14.272572694355336, -51.25567404158474
''' ---------- Leitura do DataFrame já clusterizado com as classes separadas 
----------------- em compoentes "Grupo1" & "Grupo2" ---------------------------'''
df_states = pd.read_csv("df_states.csv")
df_brasil = pd.read_csv("df_brasil.csv")
df_1 = pd.read_csv(
    'df_fases_total.csv', sep=',')

brasil_states = json.load(open('geojson/brazil_geo.json', 'r'))

select_columns = {
    'casosAcumulado': 'Casos Acumulados',
    'obitosAcumulado': 'Óbitos Totais',
    "obitosAcumulado": "Óbitos Totais",
    "obitosNovos": "Óbitos por dia"
}

select_columns1 = {
    'fase1': 'Agrupamento Fase 1',
    'fase2': 'Agrupamento Fase 2',
    'fase3': 'Agrupamento Fase 3'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server

fig = px.choropleth_mapbox(df_1, locations='estado',
                           color='fase1', center={'lat': -16.95, 'lon': -47.78}, zoom=2,
                           geojson=brasil_states, color_continuous_scale='viridis', opacity=0.8,
                           hover_data={'casosAcumulado': True, 'obitosAcumulado': True, 'fase1': True})

fig.update_layout(paper_bgcolor="#D8D8F6",
                  autosize=True,
                  margin=dict(
                      l=15,
                      r=15,
                      b=15,
                      t=15),
                  showlegend=True,
                  mapbox_style="open-street-map")

df_data = df_states[df_states["estado"] == "RO"]


fig2 = go.Figure(layout={"template": "plotly_dark"})
fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor="#D8D8F6",
    plot_bgcolor="#D8D8F6",
    autosize=True,
    margin=dict(l=10, r=10, b=10, t=10),
)


app.layout = dbc.Container([
    dbc.Row([
            dbc.Col([
                    html.Div([
                        html.H1("Grupo 7 - Projeto Integrador"),
                        html.H4(children=""),
                        dbc.Button("BRASIL", color="primary",
                                   id="location-button", size="lg")
                    ], style={"background-color": "#D8D8F6", "margin": "-25px", "padding": "25px"}),
                    html.H5("Informe a data na qual deseja obter informações:", style={
                        "margin-top": "40px"}),
                    html.Div(
                        className="div-for-dropdown",
                        id="div-test",
                        children=[
                            dcc.DatePickerSingle(
                                id="date-picker",
                                min_date_allowed=df_states.groupby(
                                    "estado")["data"].min().max(),
                                max_date_allowed=df_states.groupby(
                                    "estado")["data"].max().min(),
                                initial_visible_month=df_states.groupby(
                                    "estado")["data"].min().max(),
                                date=df_states.groupby("estado")[
                                    "data"].max().min(),
                                display_format="MMMM D, YYYY",
                                style={"border": "0px solid black"},
                            )
                        ],
                    ),

                    dbc.Row([

                        dbc.Col([dbc.Card([
                                dbc.CardBody([
                                    html.Span("Casos confirmados totais",
                                              style={"color": "#424242"},
                                              className="card-text"),
                                    html.H3(style={"color": "#389fd6"},
                                            id="casos-confirmados-text"),
                                    html.Span("Novos casos na data",
                                              style={"color": "#424242"},
                                              className="card-text"),
                                    html.H5(
                                        style={"color": "#389fd6"}, id="novos-casos-text"),
                                ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                                                       "color": "#FFFFFF"})], md=6),
                        dbc.Col([dbc.Card([
                                dbc.CardBody([
                                    html.Span("Óbitos confirmados",
                                              style={"color": "#424242"},
                                              className="card-text"),
                                    html.H3(
                                        style={"color": "#DF2935"}, id="obitos-text"),
                                    html.Span("Óbitos na data",
                                              style={"color": "#424242"},
                                              className="card-text"),
                                    html.H5(style={"color": "#DF2935"},
                                            id="obitos-na-data-text"),
                                ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                                                       "color": "#FFFFFF"})], md=6),
                    ]),

                    html.Div([
                        html.H5("Selecione que tipo de dado deseja visualizar:", style={
                            "margin-top": "25px"}),
                        dcc.Dropdown(
                            id="location-dropdown",
                            options=[{"label": j, "value": i}
                                     for i, j in select_columns.items()
                                     ],
                            value="casosNovos",
                            style={"margin-top": "10px"}
                        ),
                        dcc.Graph(id="line-graph", figure=fig2, style={
                            "background-color": "#D8D8F6",
                        }),
                    ], id="teste")
                    ], md=5, style={
                "padding": "25px",
                "background-color": "#D8D8F6"
            }),

            dbc.Col(
                [
                    html.H5("Selecione a Fase: ",
                            style={"margin-top": "25px"}),
                    dcc.Dropdown(
                        id="location-dropdown1",
                        options=[{"label": j, "value": i}
                                 for i, j in select_columns1.items()
                                 ],
                        value="fase1",
                        style={"margin-top": "10px", 'margin-bottom': '10px'}
                    ),
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=[dcc.Graph(id="choropleth-map", figure=fig,
                                            style={'height': '100vh', 'margin-right': '20px'})],
                    ),
                ], md=7, style={
                    "padding": "25px",
                    "background-color": "#D8D8F6"
                }),
            ], no_gutters=True)

], fluid=True,
)
# ---------------- Interação dos componentes: --------------------------------


@app.callback(
    [
        Output('casos-confirmados-text', 'children'),
        Output('novos-casos-text', 'children'),
        Output('obitos-text', 'children'),
        Output('obitos-na-data-text', 'children'),
    ],
    [Input('date-picker', 'date'), Input('location-button', 'children')]
)
def display_status(date, location):
    if (location == 'BRASIL'):
        df_data_na_data = df_brasil[df_brasil['data'] == date]
    else:
        df_data_na_data = df_states[df_states['estado']
                                    == location & (df_states['data'] == date)]

    casos_acumulados = "-" if df_data_na_data["casosAcumulado"].isna(
    ).values[0] else f'{int(df_data_na_data["casosAcumulado"].values[0]):,}'.replace(",", ".")
    casos_novos = "-" if df_data_na_data["casosNovos"].isna(
    ).values[0] else f'{int(df_data_na_data["casosNovos"].values[0]):,}'.replace(",", ".")
    obitos_acumulado = "-" if df_data_na_data["obitosAcumulado"].isna(
    ).values[0] else f'{int(df_data_na_data["obitosAcumulado"].values[0]):,}'.replace(",", ".")
    obitos_novos = "-" if df_data_na_data["obitosNovos"].isna(
    ).values[0] else f'{int(df_data_na_data["obitosNovos"].values[0]):,}'.replace(",", ".")

    return (
        casos_acumulados,
        casos_novos,
        obitos_acumulado,
        obitos_novos
    )


@app.callback(
    Output('choropleth-map', 'figure'),
    Input('location-dropdown1', 'value'))
def update_map(value):
    if (value == 'fase1'):
        fig = px.choropleth_mapbox(df_1, locations="estado", geojson=brasil_states,
                                   # https://www.google.com/maps/ -> right click -> get lat/lon
                                   center={"lat": CENTER_LAT,
                                           "lon": CENTER_LON},
                                   zoom=4, color='fase1', color_continuous_scale="viridis", opacity=0.55,
                                   hover_data={
                                       "casosAcumulado": True, "estado": True}
                                   )

        fig.update_layout(paper_bgcolor="#D8D8F6", mapbox_style="open-street-map", autosize=True,
                          margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)

    elif (value == 'fase2'):
        fig = px.choropleth_mapbox(df_1, locations="estado", geojson=brasil_states,
                                   # https://www.google.com/maps/ -> right click -> get lat/lon
                                   center={"lat": CENTER_LAT,
                                           "lon": CENTER_LON},
                                   zoom=4, color='fase2', color_continuous_scale="viridis", opacity=0.55,
                                   hover_data={
                                       "casosAcumulado": True, "estado": True}
                                   )

        fig.update_layout(paper_bgcolor="#D8D8F6", mapbox_style="open-street-map", autosize=True,
                          margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    elif (value == 'fase3'):
        fig = px.choropleth_mapbox(df_1, locations="estado", geojson=brasil_states,
                                   # https://www.google.com/maps/ -> right click -> get lat/lon
                                   center={"lat": CENTER_LAT,
                                           "lon": CENTER_LON},
                                   zoom=4, color='fase3', color_continuous_scale="viridis", opacity=0.55,
                                   hover_data={
                                       "casosAcumulado": True, "estado": True}
                                   )

        fig.update_layout(paper_bgcolor="#D8D8F6", mapbox_style="open-street-map", autosize=True,
                          margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    return fig


@app.callback(
    Output("line-graph", "figure"),
    [Input("location-dropdown", "value"), Input("location-button", "children")]
)
def plot_line_graph(plot_type, location):
    if location == "BRASIL":
        df_data_on_location = df_brasil.copy()
    else:
        df_data_on_location = df_states[(df_states["estado"] == location)]
    fig2 = go.Figure(layout={"template": "plotly_dark"})
    bar_plots = ["casosNovos", "obitosNovos"]

    if plot_type in bar_plots:
        fig2.add_trace(
            go.Bar(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    else:
        fig2.add_trace(go.Scatter(
            x=df_data_on_location["data"], y=df_data_on_location[plot_type]))

    fig2.update_layout(
        paper_bgcolor="#D8D8F6",
        plot_bgcolor="#D8D8F6",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
    )
    return fig2


if __name__ == '__main__':
    app.run_server(debug=True)
