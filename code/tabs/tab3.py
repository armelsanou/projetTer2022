import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc 
import pandas as pd
from dash.dependencies import Input, Output, State, ALL
from app import app 
from tabs import tab2

if tab2.model_coclust is not None:
	clusters = range(tab2.model_coclust.n_clusters)
else:
	clusters = []

view_type = dbc.Card(
	[
		#html.H4("Select :", className="card-title"),
		
		dbc.RadioItems(
			id = 'cluster_type',
			options =[
				{'label':'Document', 'value':1},
				{'label': 'Term', 'value':2},	
			],
			value = 1
		),
		html.Hr(),
		
		dbc.Button('Show clusters', id = 'show_cluster', color='primary', n_clicks=0)	
	],
	style={'width':'18rem'}
)


layout =html.Div(id="tab1_content", children = [html.Hr(),html.Div(id='choice', children=view_type),
	html.Hr() ,html.Div(id = 'content'),html.Hr(), html.Div(id='show')])

@app.callback(
    Output('content', 'children'),
    Input('show_cluster', 'n_clicks'),
    State('content', 'children'))

def dropdown(n_clicks, children):
	if n_clicks > 0:
		if tab2.model_coclust is None:
			return  dbc.Jumbotron(
				[
				html.H1('Error: Not found', className = 'text-danger'), 
				html.Hr(),
				html.P('Train a coclust model before...')
				]
				)
		else:
			return dcc.Dropdown(
				id={
				'type': 'filter-dropdown',
				'index': n_clicks
				},
				options=[{'label': f'cluster {i+1}', 'value': i} for i in range(tab2.model_coclust.n_clusters)]
				)


cluster_state = None
@app.callback(
    Output('show', 'children'),
    [Input({'type': 'filter-dropdown', 'index': ALL}, 'value'), Input('cluster_type', 'value')]
)

def display_output(values, cluster_type):
	global cluster_state
	if len(values) > 0 and values[0] is not None:
		if cluster_type == 1: # doc_clusters
			if tab2.doc_clusters is not None:
				cluster_state=tab2.doc_clusters[values[0]]
		else: # term_clusters
			if tab2.term_clusters is not None:
				cluster_state=tab2.term_clusters[values[0]]
	return cluster_state
