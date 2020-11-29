import dash
import dash_core_components as dcc
import dash_html_components as html 
import dash_bootstrap_components as dbc 

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

server = app.server

app.title = 'Demo App'

# a card is a formatted container, every compoent has something called id and children, 
# callbacks relies solely on the use of IDs, 
# you cannot use same ID for two different components
# unless you have multipage web application
header = dbc.Card([
    dbc.Row([
        dbc.Col([html.H5('OUR FIRST APP DEMO')], width=7, style={'padding':'20px'}),
        # style is a dictionary
        dbc.Col([html.Img(src='./assets/Ottawa-Where-to-Visit-Santa-725x420-c.jpg',style={'width':'150px','height':'140px'})], width=5)
    ], style={'align-items':'center'})
], style={'margin':'10px'})

# def make_layout():
#     return()

app.layout = header

if __name__ == '__main__':
    # port = localhost
    app.run_server(debug=False, port=8053)