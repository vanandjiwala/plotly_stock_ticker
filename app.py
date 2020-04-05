import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from iexfinance.stocks import Stock,get_historical_data
from datetime import datetime

import projectconfig as config
import pandas as pd

app = dash.Dash()

nsdq = pd.read_csv('Data/nasdaq-company-list.csv')
nsdq.set_index('Symbol',inplace=True)

options = []
for tic in nsdq.index:
    stock_option = {
        'label': '{}:{}'.format(tic,nsdq.loc[tic]['Name']),
        'value': tic
    }
    options.append(stock_option)


app.layout = html.Div([
    html.Nav([
        html.Div([
            html.A([
                html.Img(src=app.get_asset_url("logo.png"))
            ],className="navbar-item")
        ],className="navbar-brand")
    ],className="navbar is-dark is-bold",role="navigation"),
    #END OF NAVBAR

    html.Section([
        html.Div([
            html.Div([
                html.H1(children="Stock Ticker DashBoard",className="title"),
                html.H5(children="A Demo Dashboard For Stock Research",className="subtitle")
            ],className="container has-text-centered")
        ],className="hero-body")
    ],className="hero is-dark"),
    #END OF HEADER SECTION

    html.Div([
        html.Div([
            #Buffer DIV Left Side
        ],className="column is-1"),
        html.Div([
            html.Div([
                html.Label(children="Ticker Name",className="label has-text-white"),
                html.Div([
                    dcc.Dropdown(
                        id ='my_ticker_symbol',
                        options=options,
                        value=['TSLA'],
                        multi=True,
                        style={'border-radius':0}
                    )
                ],className="control"),
            ],className="field"),
            html.Div([
                html.Label(children="Select Date",className="label has-text-white"),
                dcc.DatePickerRange(
                    id='my_date_picker',
                    min_date_allowed=datetime(2020, 1, 1),
                    max_date_allowed=datetime.today(),
                    start_date=datetime(2020, 1, 1),
                    end_date=datetime(2020, 1, 1)
                )
            ],className="field"),
            html.Div([
                html.Button('Submit', id='submit-val', n_clicks=0, className="button is-medium is-light is-fullwidth")
            ], className="field")
        ],className="column is-3"),
        html.Div([
            dcc.Graph(
                id='my_graph',
                figure={
                    'data': [
                        {'x': [1, 2], 'y': [3, 1]}
                    ],
                    'layout':{
                        'title':'ticker',
                        'plot_bgcolor': '#CDE0CA',
                        'paper_bgcolor': '#CDE0CA',
                    }
                }
            )
        ],className="column is-7"),
        html.Div([
            #Buffer DIV Right Side
        ], className="column is-1")
    ],className="columns is-vcentered")
    #END OF ROW1
],className="has-background-grey-darker")


@app.callback(Output('my_graph','figure'),
              [Input('submit-val','n_clicks')],
              [State('my_ticker_symbol','value'),
               State('my_date_picker', 'start_date'),
               State('my_date_picker', 'end_date')])
def update_chart(n_clicks,stock_ticker, start_date, end_date):

    start = datetime.strptime(start_date[:10],'%Y-%m-%d')
    end = datetime.strptime(end_date[:10],'%Y-%m-%d')

    #TODO: Complete testing this functionality. Free tier API requrests used while testing so can not perform further testing till next month!!
    #TODO: Resolve and handle issues around API calls
    traces = []
    for tic in stock_ticker:
        df = get_historical_data(tic, start, end, output_format='pandas', token=config.api_key, close_only=True)
        traces.append({'x':df.index,'y': df.close,'name':tic})


    figure = {
        'data': traces,
        'layout': {
            'title': stock_ticker,
            'plot_bgcolor': '#CDE0CA',
            'paper_bgcolor': '#BFD8FF',
        }
    }

    return figure



if __name__ == "__main__":
    app.run_server()