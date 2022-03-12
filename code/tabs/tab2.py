import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc 
import pandas as pd
#import dash_table
from dash import dash_table
from dash.dependencies import Input, Output, State, MATCH, ALL
from app import app 
from tabs import sidepanel, navbar, tab1
from traitements import server, coclust


model = dbc.Card(
	[
		html.H4("Select a model:", className="card-title"),
		dcc.Dropdown(
			id = 'model',
			options = [
				{'label':'Coclust Mod', 'value':1},
				{'label': 'Coclust Spectral Mod', 'value':2},
				{'label':'Best Modularity Partition', 'value':3}
			],
			value = 1
		),
		
		dbc.Input(id= 'n_clusters',type ='number', placeholder='Number of clusters'),
		
		
	
	],
	style={"width": "18rem"}
)


display = dbc.Card(
	[
		dbc.RadioItems(
			id = 'display_coclust',
			options =[
				{'label':'Clusters size', 'value':1},
				{'label': 'Reorganized matrix', 'value':2},
				{'label': 'Cluster top terms', 'value':3},
				{'label': 'Modularities', 'value':4},
				
			],
			value = 1
		),
		dbc.Button('Apply', id = 'coclust_apply', color='primary', n_clicks=0)	
	],
	style={'width':'18rem'}
)


layout =html.Div(id="tab1_content", children=[
				html.Hr(),
				html.Div(id='divModel', children=model),
				html.Hr(),
				html.Div(id = 'divDisplay', children=display),
				html.Hr(),
				html.Div(id='clusters_size', children=dbc.Card([
					dbc.CardImg(id='clusters_size_plot', src='')
				],style={"width": "60rem"})),
				html.Hr(),
				html.Div(id='container', children=[]),
				html.Hr(),
				html.Div(id='container_output'),
				html.Hr(),
				html.Div(id='doc_groups'),
				html.Hr(),
				html.Div(id='word_groups') 
				])
df = None
click = 0
state = None
model_coclust = None 
doc_clusters = None
term_clusters = None
dtm = None


@app.callback(Output('clusters_size_plot', 'src'), [Input("coclust_apply", "n_clicks"), Input('model', 'value'),
													Input('display_coclust', 'value'), Input('n_clusters', 'value')])
			
def clusters_size(btn, model, display, n_clusters):
	global df
	global click
	global state
	global model_coclust
	global doc_clusters
	global term_clusters
	global dtm
	modularity = None
	n_clusters = 4
	
	if n_clusters is None:
		n = 10
	else:
		n = n_clusters
	
	if tab1.df is None:
		state = dbc.Jumbotron(
		[
		html.H1('Error: Not found', className = 'text-danger'), 
		html.Hr(),
		html.P('Load articles before...')
		]
		)
		state = None
	elif click < btn :
		click = btn
		dtm = server.DTM(tab1.df)
		if model== 1:
			model_coclust = coclust.coclustmod(dtm, n)
		elif model == 2:
			model_coclust = coclust.coclustspecmod(dtm, n)
		else:
			model_coclust, modularity = coclust.bestModularityPartition(dtm, n_max = n)
			print(model)
		
		if  display == 1: # cluster size
			fig = coclust.plot_cluster_sizes(model_coclust)
			state = coclust.fig_to_uri(fig)
		elif display == 2: # Reorganized matrix
			fig= coclust.plot_reorganized_matrix(dtm.to_numpy(), model_coclust)
			state = coclust.fig_to_uri(fig)
			return state
		elif display == 3: # top term clusters
			fig = coclust.plot_cluster_top_terms(dtm.to_numpy(), dtm.columns, 10, model_coclust)
			state = coclust.fig_to_uri(fig)
		elif display == 4: # Modularities
			if modularity is not None:
				fig = coclust.plot_max_modularities(modularity, range(2,n))
				modularity = None
			else:
				fig = coclust.plot_convergence(model_coclust.modularities, "Modularity")
			state = coclust.fig_to_uri(fig)
	
	if model_coclust is not None: # Generate clusters for docs and terms
		doc_clusters = {}
		term_clusters = {}
		for i in range(model_coclust.n_clusters):
			doc_clusters[i] = []
			term_clusters[i] = []
			
			if len(model_coclust.get_indices(i)[0]) > 0:
				doc_clusters[i] = '___________'.join(list(dtm.index[model_coclust.get_indices(i)[0]]))
			else:
				doc_clusters[i] = 'No doc in this cluster'
			if len(model_coclust.get_indices(i)[1]) > 0:
				term_clusters[i] = '\t'.join(list(dtm.columns[model_coclust.get_indices(i)[1]]))
			else:
				term_clusters[i] = 'No term in this cluster'
			
	return state			


