import random
import string

import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output
from flask_caching import Cache

SECRET_KEY = 'superman is the best superhero ever'


def dash_server(server):
    app = Dash(server=server, url_base_pathname='/dash')
    app.config.supress_callback_exceptions = True

    cache = Cache(app.server, config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'cache-directory',
        'CACHE_THRESHOLD': 10  # should be equal to maximum number of active users
    })

    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='div_main_place_holder')
    ])

    @cache.memoize()
    def create_secret(key):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(100))

    @app.callback(
        Output('div_main_place_holder', 'children'),
        [Input('url', 'search')])
    def display_page(request_args):
        try:
            if request_args:
                arg_parts = str(request_args)[1:].split('=')
                key = arg_parts[0]
                value = arg_parts[1]
                if 'secret' == key and value == create_secret('some value as key'):
                    return html.Div([
                        html.Div(id='div_result'),
                        dcc.Input(id='div_input', type='text', value=''),
                        html.Div(id='div_chart'),

                    ])
            return html.Div('Error Has Occured')
        except Exception as e:
            print(e)



    @app.callback(
        Output('div_result', 'children'),
        [Input('div_input', 'value')])
    def callback(text):
        return "Search Charts by Type: {}".format(text)

    @app.callback(
        Output('div_chart', 'children'),
        [Input('div_input', 'value')])
    def callback(text):
        if text == 'line':
            return dcc.Graph(
                            id='example',
                            figure={
                                'data': [
                                    {'x': [1, 2, 3, 4, 5], 'y': [2, 3, 2, 5, 10], 'type': 'line', 'name': 'Revenue'},
                                ],
                                'layout': {
                                    'title': 'Revenue Graph'
                                }
                            }
                        )

        elif text == 'bar':
            return  dcc.Graph(
                            id='example',
                            figure={
                                'data': [
                                    {'x': [1, 2, 3, 4, 5], 'y': [2, 3, 2, 5, 10], 'type': 'bar', 'name': 'Revenue'},
                                ],
                                'layout': {
                                    'title': 'Revenue Graph'
                                }
                            }
                        )
        return "(Only line and bar charts are supported)"

    return app.server, create_secret
