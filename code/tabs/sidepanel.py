from posixpath import dirname
import dash
import plotly
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc 
#import dash_table
from dash import dash_table
import pandas
from dash.dependencies import Input, Output
from app import app
from tabs import tab1, tab2


layout = html.Div([
    html.H1("Biomédical", className="display-6"),
    dbc.Row([
		dbc.Col([
       	     dbc.Card(
            dbc.CardBody([
                dbc.FormGroup([
                    # Anciennement ******AD
                    html.P('Filter by word or text',className="lead"),
                    html.Hr(),
                    #dcc.Input(
                        #id='term',
                        #placeholder='Enter a term',
                        #type='text',
                        #value=''),
                    #]),

                    #Input remplacé par Zone de texte ******AD
                    dcc.Textarea(
                        id='term',
                        className="form-control",
                        placeholder='You can enter a word or text',
                        style={'width': '100%', 'height': 70},
                    )
                    ]),
                    #Ajout upload file     ******AD
                    html.A('Upload file on your disk'),

                    html.Hr(),

                    dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px',
                        'cursor': 'pointer'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
                html.Div(id='output-data-upload'),
                    html.Hr(),
                html.P('Choose number of articles'),
                dcc.Slider(
					id = 'number',
                    min=0,
                    max=10,
                    marks={i: '{}'.format(i*10) for i in range(10)},
                    step=10,
                    value=5),
                
                dbc.FormGroup([
                    html.P('Choose normalization type :',className="lead"),
                    dcc.Dropdown(
						id = 'norm',
                        options=[
			
                            {'label':'Lemmatization', 'value':1},
                            {'label':'Stemming','value':2}],
                        value=1)]),
                dbc.FormGroup([
                    html.P('Choose cleaning options :',className="lead"),
                    dcc.Dropdown(
                        id="clean",
                        options=[
                            {'label':'Basic stopwords', 'value':1},
                            {'label':'Basic transformations','value':2}],
                        multi=True,
                        value=1)]),
				dbc.FormGroup(
				[
                
                html.P('Add some stopwords :',className="lead"),
                dbc.Textarea(id = 'user_stopwords', bs_size=True),
                
            ],
        ),
                    
            #dbc.Button("Apply",color="primary", className="mr-1", id = 'apply', C=0)
            dbc.Button("Apply",color="primary", className="mr-1", id = 'apply'),

            dbc.Button("Export",color="secondary", className="mr-1", id = 'export') 
                
        ])),
    ], width=3)# End col
    ,dbc.Col(html.Div([
            dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label='Vizualisation', value='tab-1'),
                    dcc.Tab(label='Co-clustering', value='tab-2'),
                    dcc.Tab(label='Clusters', value='tab-3'),
                    dcc.Tab(label='About...', value='tab-4')
                ])
            , html.Div(id='tabs-content')
        ]), width=9)
    ]) #end row
    
])#end div