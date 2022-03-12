import dash
import plotly
#import dash_core_components as dcc
from dash import dcc
#from dash import html
from dash import html
#import dash_table
from dash import dash_table
from dash.dependencies import Input, Output
from app import app
from tabs import sidepanel, tab1, tab2, tab3, navbar
import dash_bootstrap_components as dbc 
import nltk
from nltk.corpus import wordnet as wn  #commented 3 lines bottom and replace them by this line, armel sanou
#from nltk.corpus import wordnet
#wordnet.ensure_loaded()
#nltk.download('wordnet')
#nltk.download() #moi
server = app.server
app.title = 'Dashboard'
app.layout = html.Div([navbar.Navbar()
                        , sidepanel.layout
            ])


            
@app.callback(Output('tabs-content', 'children'),[Input('tabs', 'value'), Input('apply', 'n_clicks')])
def render_content(tab, search):
			
	if tab == 'tab-1':
		return tab1.layout
	elif tab == 'tab-2':
	   return tab2.layout
	elif tab == 'tab-3':
	   return tab3.layout

if __name__ == '__main__':
    #app.run_server(debug = True) # debug = True
	#app.run_server(debug=True, host="127.0.0.1", port=4000, use_reloader=False)
	app.run_server()
