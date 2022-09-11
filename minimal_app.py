import dash
from dash.dependencies import Input, Output
from dash import html, dcc

image_path = 'assets/ufo_image.png'

app = dash.Dash(__name__)

app.layout = html.Div([
        dcc.Input(id='my-id', value='initial value', type='text'),
        html.Div(html.Img(src=image_path))
        ])

if __name__ == '__main__':
    app.run_server(debug=True)