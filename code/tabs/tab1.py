import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc 
import pandas as pd
#import dash_table
from dash import dash_table
from dash.dependencies import Input, Output
from app import app 
from tabs import sidepanel, navbar
import plotly.graph_objects as go
from traitements import server
import string
import nltk
import numpy as np
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from traitements import server
import seaborn as sns
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import base64
import datetime

import re
from collections import Counter
import nltk
from nltk.corpus import stopwords

from dash.dependencies import Input, Output, State



radios_input = dbc.FormGroup(
    [
        dbc.Card(
        dbc.Col(
            dbc.RadioItems(
                id="display_type",
                options=[
                    {"label": "Text", "value": 1},
                    {"label": "Frequency", "value": 2},
                    {"label":"Frequency per document", "value":3},
                    {"label": "Words cloud",
					  "value": 5,}
                ],
                value=1
            ),
            width=10,
        ),)
    ],
    row=True,

)

layout = html.Div(id="tab2_content", children=[html.Hr(),html.H5("Display type:", className='card-title'),
			radios_input,html.Hr(),html.Div(id="display")])

	
			
df = None
n_clicks = 0
text = None
freq_graph_corpus = None
freq_graph_doc = None
word_cloud = None
corr = None
file_content = None

@app.callback(Output("display", "children"), [Input("display_type", "value"),
			Input("apply", "n_clicks"), Input('term', 'value'), Input('number', 'value'),
			Input('norm', 'value'), Input('clean', 'value'), Input('user_stopwords', 'value')])


def display(display_type, search, term, number, norm, clean, user_stopwords):
	global df
	global n_clicks
	global text
	global freq_graph_corpus
	global freq_graph_doc
	global word_cloud
	global corr
	valeur = ""
	if file_content is not None and term is not None:
		valeur = file_content
	elif term is not None:
		valeur = term
	elif file_content is not None:
		valeur = str(file_content)
	
	#if df is None: # Pas besoin de refaire une recherche

	if valeur is not None and valeur != "":
		valeur = str(valeur)
		extract = extract_most_frequent_word(valeur)
		split_list = split_string(extract)
		#print("file content", valeur)
		
		if search == 0:
			return server.home()
			
		elif search != 0:
			df = None #vider à chaque recherche
			text = None #vider à chaque recherche
			freq_graph_corpus = freq_graph_doc = word_cloud = corr = None  #vider à chaque recherche
			if number <= 0:
				df = server.load_articles(extract)
			else:
				df = server.load_articles(extract, number*10)
			df.iloc[0, :] = server.preprocessing(df.iloc[0, :], norm, clean, user_stopwords) # preprocessing
		
		if df is not None :
			if display_type == 1: # Text
				if text is None:
					corpus = df.copy().iloc[0,:]
					text = corpus
					f = open("corpus.txt", "a+")
					#on découpe chaque ligne en taille de 50 maximum mots avant d'écrire dans le fichier
					for line in text:
						tmp = str(line).split(" ")
						cpt = 0
						#print("----", tmp)
						f.write(str(' '.join(tmp[cpt:cpt+50])).strip('[]')) #on écrit juste 50 mots max par ligne
						f.write('\n\n')
						cpt = cpt+45
					f.close()
				return text
				
			elif display_type == 2: # Frequency
				if freq_graph_corpus is None:
					corpus = df.copy().iloc[0,:]
					df_freq = server.frequenceCorpus(corpus, norm, clean, user_stopwords)
					fig = px.bar(df_freq, x='word', y='count', title='Word frequency on corpus', 
					template='plotly_white', labels={'word':'Words', 'count':'Count'})
					freq_graph_corpus = dcc.Graph(figure = fig)
				return freq_graph_corpus
				
			elif display_type == 3: # Frequency per document
				if freq_graph_doc is None:
					corpus = df.copy()
					df_freq = server.frequenceDocument(corpus, norm, clean, user_stopwords)
					fig = px.imshow(df_freq.transpose())
					#fig.update_layout(legend_orientation="h")
					freq_graph_doc = dcc.Graph(figure = fig)

				return freq_graph_doc   
			
			else: # words cloud
				if word_cloud is None:
					corpus = df.copy().iloc[0,:]
					corpus = server.preprocessing(corpus, norm, clean, user_stopwords)
					wordcloud = WordCloud(background_color="white")
					text = " ".join(corpus) 
					wordcloud.generate(text)
					fig = px.imshow(wordcloud)
					word_cloud = dcc.Graph(figure=fig)
				return word_cloud

#Fonction qui permet de créer une liste de tules contenant pour chaque mot, son nombre d'occurences.
def extract_most_frequent_word(input_text):
	#extract_text = []
	text = ""
	stops_words = stopwords.words('english')
	stops_words += ['ca', 'nt', "'s"]

	cleaned = re.sub('<[^>]*>', '', input_text)
	cleaned2 = re.sub('[(+*,;"!:%/.?\')]', '', cleaned)
	
	split_it = cleaned2.split()
	#print(split_it)


	f = open("cleaned_corpus.txt", "w")
	f.write(cleaned2)
	f.close()


	f = open("cleaned_corpus.txt", "r")

	f2 = open("cleaned_normaized_corpus.txt", "w")

	lines = f.readlines()
	
	count = 0
	# Strips the newline character
	for line in lines:
		tmp = str(line).split(" ")
		cpt = 0
		#print("----", tmp)
		txt = str(' '.join(tmp[cpt:cpt+45])).strip("b'").strip("  \\n'") #on écrit juste 50 mots max par ligne, car les paramètres de la traduction, la taille de chaque ligne ne doit pas dépasser 50
		f2.write(txt)
		f2.write('\n\n')
		cpt = cpt+45
	f.close()
	f2.close()

	A = [word for word in split_it if word not in stops_words]
	#print(A)

	# Pass the split_it list to instance of Counter class.
	Counters_found = Counter(A)
	#print(Counters)

	# most_common() produces k frequently encountered
	# input values and their respective counts.
	most_occur = Counters_found.most_common(10000)

	#print(most_occur)

	for word in most_occur:
		text += word[0]+" "
	extract_text = str(text).split()
	#file_content = str(text)

	#n = 8
	#[extract_text.append(text[i:i+n]) for i in range(0, len(text), n)]
	return extract_text

#Fonction qui prend en entrée un texte, le découpe en mots et crée une liste qui sera utilisée pour boucler la recherche dans pubmed
def split_string(str_list):
	#print("given string", str_list)
	#Stores the length of the string  
	length = len(str_list)
	#Stores the array of string  
	equalStr = [];   
	#Check whether a string can be divided into n equal parts  
	if(length > 0):  
		#for i in range(0, length, chars):
		for i in range(0, length+1): 
			#Dividing string in n equal part using substring()  
			#part = str[ i : i+chars]
			if len(str_list[0:i]) > 0:
				equalStr.append(' '.join(str_list[0:i]))
		#print("après découpe", equalStr)
	return equalStr

def parse_contents(contents, filename, date):
	global file_content

	content_type,content_string = contents.split(',')

	decoded = base64.b64decode(content_string)
	file_content = decoded.decode('utf8').strip()
	try:
		print("")
	except Exception as e:
		print(e)
		return html.Div([
			'There was an error processing this file.'
		])

	return html.Div([
		html.H5(filename),
		html.H6(datetime.datetime.fromtimestamp(date)),
		#html.H6(contents),

		#dash_table.DataTable(
		#   df.to_dict('records'),
		#  [{'name': i, 'id': i} for i in df.columns]
		#),

		html.Hr(),  # horizontal line

		# For debugging, display the raw contents provided by the web browser
		#html.Div('Raw Content'),
		#html.Pre(contents[0:200] + '...', style={
			#'whiteSpace': 'pre-wrap',
			#'wordBreak': 'break-all'
		#})
	])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children