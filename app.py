# understand dash component
import dash
import dash_core_components as dcc
import dash_html_components as html 
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go 

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

server = app.server

app.title = 'SALARY PROJECTION'

provinces = {'AB': 70000, 'ON': 72000, 'MB': 58000, 'BC': 73000, 'NL': 53000, 'SK': 56000, 'QB':53000, 'NB': 57000}

modal = html.Div(
    [
        dbc.Button("About", id='open'),
        dbc.Modal(
            [
                dbc.ModalHeader('About Dashboard'),
                dbc.ModalBody("""This dashboard shows a projection of a Data Scientist salary for several provinces in Canada. 
                                Please note!!! these are just ficitious values!"""),
                dbc.ModalFooter(
                    [dbc.Button("Close", id='close', className='ml-auto')]
                ),
            ],
            id='modal',
        ),
    ]
)

# a Card is a formatted dash container, it has 12 columns in each row
header = dbc.Card([
    dbc.Row([
        dbc.Col([html.H5('DATA SCIENTIST SALARY PROJECTION FOR CANADIAN PROVINCES')], width=9, style={'text-align':'center'}),
        # style is a dictionary, uses key - value pair format
        dbc.Col([dbc.Button('GitHub', href='https://github.com/menghanzhao/dash_app_demo',target='_blank',color='link')], width=1),
        dbc.Col(modal),
        dbc.Col([html.Img(src='./assets/datascience.jpg',style={'width':'80px','height':'80px'})], width=1, style={'align-items':'right'})
    ], style={'align-items':'center','margin':'5px'})
], style={'margin':'20px'})

# dash bootstrap component: https://dash-bootstrap-components.opensource.faculty.ai/
form = dbc.FormGroup(
    [
        dbc.Label('Enter Years of Experience', html_for='ex-yrs', width=5),
        dbc.Col([dcc.Input(id='ex-yrs', type='number', min=0, value=10)], width=5),
    ],
    row=True, style={'align-items':'center'}
    # if row = False, the children will be orgnized in columns
)

form1 = dbc.FormGroup(
    [
        dbc.Label('Select Province(s)',html_for='province-drops',width=5),
        dbc.Col([
            dcc.Dropdown(
                id='province-drops',
                options=[
                    {'label':k, 'value':k} for k, v in provinces.items()
                ],
                # set initial value to be the first 2 of all the keys
                value=[*provinces.keys()][:2],
                multi=True
            )
        ], width=5),
    ],
    row=True, style={'align-items':'center'}
)

body1 = dbc.Row([
    dbc.Col([form, form1], width=4),
    dbc.Col([dbc.Spinner(dcc.Graph(id='plot'))], width=8)
], style={'margin':'4px'})

# this is where you can put a machine learning model instead of a dummy function!!
# this dummy function just increses the salary by 2% for every year of experience
def get_pay(yr):
    val = lambda x, k: int(provinces[k] * (1.02)**x)
    return {k:[val(x,k) for x in range(yr, yr+15)] for k, v in provinces.items()}

app.layout = html.Div([header,body1])

# in callback function: 
# Output('id', 'property'),
# based on changes in Input('id', 'property')
# note: there can be multiple Outputs and Inputs
@app.callback(
    Output('plot','figure'),
    [Input('province-drops', 'value'), Input('ex-yrs', 'value')],
)
def generate_figure(province_list, yr_exp):
    fig = go.Figure(data=[
        go.Bar(name=k, x=[*range(yr_exp, yr_exp+15)], y=get_pay(yr_exp)[k]) for k in province_list
    ])
    fig.update_layout(barmode='group', xaxis={'title':'Years of Experience'}, yaxis={'title':'Salary in CAD'})
    return fig

@app.callback(
    Output('modal', 'is_open'),
    [Input('open','n_clicks'), Input('close','n_clicks')],
    [State('modal','is_open')],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == '__main__':
    # port = localhost
    app.run_server(debug=True, port=8050)