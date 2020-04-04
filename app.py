import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

app = dash.Dash()

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

        ],className="column is-1"),
        html.Div([
            html.Div([
                html.Label(children="Ticker Name",className="label has-text-white"),
                html.Div([
                    dcc.Input(
                        id ='my_ticker_symbol',
                        value='TSLA',
                        className="input"
                    )
                ],className="control")
            ],className="field")
        ],className="column is-3"),
        html.Div([
            dcc.Graph(
                id='my_graph',
                figure={
                    'data': [
                        {'x': [1, 2], 'y': [3, 1]}
                    ]
                }
            )
        ],className="column is-7"),
        html.Div([

        ], className="column is-1")
    ],className="columns is-vcentered")
    #END OF ROW1
],className="has-background-grey-darker")

if __name__ == "__main__":
    app.run_server()