# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/) 
specification of Markdown.  
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''


df_url = 'https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/ggplot2/msleep.csv'
df = pd.read_csv(df_url)
df_vore = df['vore'].dropna().sort_values().unique()
opt_vore = [{'label': x + 'vore', 'value': x} for x in df_vore]

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.layout = html.Div(children=[
    dcc.Markdown(children=markdown_text),

    dcc.Graph(id='my-graph'),
    dcc.Graph(id='my-box-plot'),

    html.Div([
        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(
            id='my-multi-dropdown',
            options= opt_vore,
            value= df_vore[0:2],
            multi= True
        ),

        html.Label('Radio Items'),
        dcc.RadioItems(
            options= opt_vore,
            value= df_vore[0]
        ),

        html.Label('Checkboxes'),
        dcc.Checklist(
            options= opt_vore,
            values= df_vore[0:2],
        ),

        html.Label('Text Input'),
        dcc.Input(value= df_vore[0] + 'vore', type='text'),

        html.Label('Slider'),
        html.Div(
            dcc.Slider(
                min=0,
                max=len(df_vore) - 1,
                marks= opt_vore,
                value=2
            ),
            style={
                'marginLeft': '10%',
                'marginRight': '10%'
            }
        ),
    ], style={'columnCount': 2})
])

@app.callback(
    [Output('my-graph', 'figure'),
     Output('my-box-plot', 'figure'),],
    [Input('my-multi-dropdown', 'value')]
)
def update_output_graph(input_value):
    return  {
                'data': [
                    go.Scatter(
                        x=df[df['vore'] == i]['bodywt'] if i in input_value else [],
                        y=df[df['vore'] == i]['sleep_total'] if i in input_value else [],
                        text=df[df['vore'] == i]['name'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in df_vore
                ],
                'layout': go.Layout(
                    xaxis={'type': 'log', 'title': 'Body weight (kg)'},
                    yaxis={'title': 'Total daily sleep time (hr)'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            },            \
            {
                'data': [ go.Box(
                            y= df[df['vore'] == i]['sleep_total'],
                            name= i + 'vore'
                        ) if i in input_value else []
                          for i in df_vore ]
            }

if __name__ == '__main__':
    app.run_server(debug=True)