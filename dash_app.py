# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import analizer

app = dash.Dash()

a = analizer.get_data('SBER')

app.layout = html.Div(children=[
    html.H1(children='Stocker DSS'),

    html.Div(children='''
    Stocker DSS 
    '''),

    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Sberbank', 'value': 'SBER'},
            {'label': 'Gazporm', 'value': 'GAZP'},
            {'label': 'Yandex', 'value': 'YNDX'}
        ],
        value='SBER'
    ),
])

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])

def update_graph(ticker):
    graphs = []

    graphs.append(dcc.Graph(
        id='close+emas chart',
        figure={
            'data': [
                {'x': a[2],'y': a[1], 'type': 'line', 'name': 'close'},
                {'x': a[2],'y': a[3], 'type': 'line', 'name': 'ema10'},
                {'x': a[2],'y': a[4], 'type': 'line', 'name': 'ema20'},
            ],      
            'layout': {
                'title': 'Close and EMA'
            }
        }
    )),

    graphs.append(dcc.Graph(
        id='fi',
        figure={
            'data': [
                {'x': a[2],'y': a[5], 'type': 'line', 'name': 'fi2'},
                {'x': a[2],'y': a[6], 'type': 'line', 'name': 'fi13'},
            ],      
            'layout': {
                'title': 'Elder FI'
            }
        }
    ))
    
    return graphs

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')