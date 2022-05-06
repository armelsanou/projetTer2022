# Page d'accueil de l'application
#import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc
import coclust

# pip install Bio
# pip install stop_words
# pip install orange3
# pip install pyenchant si le mot est englais ou pas

from Bio import Entrez # Accés à la base PubMed
import pandas as pd # Manipulation des données
import string # gestion des ponctuations
import unicodedata # remplacer les caractères accentués
import re # segmentation de texte
from stop_words import get_stop_words
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
import nltk
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import CountVectorizer

# Hierarchical Clustering
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
# Non Hierarchical Clustering
from scipy.cluster.vq import kmeans, vq, whiten
from sklearn.decomposition import TruncatedSVD
# Coclustering
from coclust.coclustering import CoclustMod
from coclust.visualization import plot_cluster_top_terms
from coclust.visualization import plot_cluster_sizes
from coclust.visualization import plot_reorganized_matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import confusion_matrix
from coclust.visualization import plot_convergence
from coclust.visualization import plot_delta_kl
from coclust.visualization import plot_confusion_matrix
import time

 # Lemmatisation


# Message de bienvenue
def home():
	return dbc.Container(
		dbc.Alert("Bienvenue sur l'application! \n Pour démarrer, veuillez entrer un mot clé dans la barre de recherche et le nombre d'articles à importer.\n"+
		"Si aucune valeur n'est donnée le nombre d'articles par défaut sera 100.", color="success"),
		className="p-5",
		)

# Recherche de l'existance de documents suivant un mot clé
""" def search(query, n_articles):
    Entrez.email = 'biljolefa@gmail.com'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax=str(n_articles),
                            retmode='xml', 
                            term=query)
    results = Entrez.read(handle)
    return results """

#Recherche des documents suivant une liste de mots clés A & D
def search(query, n_articles):
	#print("-----------liste de mots ----------", query)
	results = []
	Entrez.email = 'biljolefa@gmail.com'
	for q in query:
		handle = Entrez.esearch(db='pubmed', sort='relevance', retmax=str(n_articles), retmode='xml', term=q)
		results.append(Entrez.read(handle))
		time.sleep(2)
	return results


# Charger le résultat de la recherche, les articles trouvés suivant le mot clé
def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'biljolefa@gmail.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


# Recherche et chargement des articles trouvés sur pubmed
def load_articles(keyword='fever', n_articles = 100):

	#Plot corpus size evolution peer number on keywords

	results = search(keyword, n_articles) # fever
	#print("--------- result dans load --------------", results)
	#id_list = results['IdList']
	#results = search(keyword, n_articles) # fever
	id_list = []
	for re in results:
		#print("-------------------------------------re--------------------------------", re)
		id_list.append(str(re['IdList']).strip('[]'))
	#print("----------------- id list --------------------", id_list)
	papers = fetch_details(id_list)
	articles = dict()
	for article in papers['PubmedArticle']:
		#print("-----clefs--------", article['MedlineCitation']['Article'].keys())
		#articles[paper['MedlineCitation']['Article']['ArticleTitle']] = ','.join(paper['MedlineCitation']['Article']['Abstract']['AbstractText'])
		if 'Abstract' in article['MedlineCitation']['Article'].keys():
			articles[article['MedlineCitation']['Article']['ArticleTitle']] = ','.join(article['MedlineCitation']['Article']['Abstract']['AbstractText'])
	#print(articles)
	return pd.DataFrame(articles, index=[0])


# Nettoyage du dataset
def clean_corpus(corpus):
	for i in range(len(corpus)):
		tmp = str(corpus[i])
		tmp = tmp.lower() # Convertir tout en miniscule
		tmp = tmp.replace("\n", " ") # Suppression des retours chariot
		tmp = tmp.translate(str.maketrans("","", '!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~')) # Suppimer les ponctuations
		#tmp = tmp.encode("utf-8").decode("utf-8") # suppression des accents
		tmp = unicodedata.normalize('NFD', tmp).encode('ascii', 'ignore') 
		tmp = str(tmp)[2:-1] # supprimer le b qui apparait lors de la suppression des accents
		
		# supprimer les caractères non-alphabetiques
		regex = re.compile('[^a-zA-Z]')
		tmp = regex.sub(' ', tmp)
		tmp = tmp.split(' ')
		# supprimer les caractères
		tmp = [word for word in tmp if len(word)>2]
		tmp = ' '.join(tmp)
		corpus[i] = tmp
	return corpus


def remove_stopwords_user(corpus, ajout_stopwords):
	stopwords = ""
	for i in range(len(ajout_stopwords)):
		stopwords = f'{stopwords}{ajout_stopwords[i]}'
	stopwords = stopwords.lower()
	stopwords = stopwords.replace("\n", "")
	stopwords = stopwords.replace(" ", "")
	stopwords=stopwords.split(",")

	for i in range(len(corpus)):
		texte = str(corpus[i])
		texte = texte.lower()
		for stopword in stopwords:
			texte = texte.replace(stopword, "")
		corpus[i] = texte
	return corpus

def remove_stopwords_basique(corpus):
	stopwords = get_stop_words('en')
	for i in range(len(corpus)):
		texte = str(corpus[i]).split()
		texte = [word for word in texte if word not in stopwords]
		corpus[i] = ' '.join(texte)
	return corpus

def pos_tagger(nltk_tag):
	if nltk_tag.startswith('J'):
		return wordnet.ADJ
	elif nltk_tag.startswith('V'):
		return wordnet.VERB
	elif nltk_tag.startswith('N'):
		return wordnet.NOUN
	elif nltk_tag.startswith('R'):
		return wordnet.ADV
	else:          
		return None

# Lemmatisation
def lemmatization(corpus):
	lem = lem = nltk.stem.WordNetLemmatizer()
	
	for i in range(len(corpus)):
		corpus[i] = corpus[i].lower()
		corpus[i] = re.sub(r'[!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~]', r'', corpus[i])
		
		words = nltk.word_tokenize(corpus[i])
		pos_tagged = nltk.pos_tag(words)
		words_tagged = list(map(lambda x: (x[0], pos_tagger(x[1]) ), pos_tagged))
		words_lemmatize = []
		for word, tag in words_tagged:
			if tag is None:
				words_lemmatize.append(word)
			else:
				word = lem.lemmatize(word, tag)
				words_lemmatize.append(word)
		corpus[i] = ' '.join(words_lemmatize)
	
	return corpus 
	
# Stemming
def stemmating(corpus):
	stem= nltk.stem.SnowballStemmer('english')
	#e = enchant.Dict('en') if e.check(stem.stem(word)
	
	for i in range(len(corpus)):
		corpus[i] = corpus[i].lower()
		corpus[i] = re.sub(r'[!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~]', r'', corpus[i])
		
		words = nltk.word_tokenize(corpus[i])
		words_stemmatize = []
		for word in words:
			words_stemmatize.append(stem.stem(word))
		corpus[i] = ' '.join(words_stemmatize)
	return corpus
		
		
		
def preprocessing(corpus, norm, clean, user_stopwords):
	if norm == 1: # Lemmatization
		corpus = lemmatization(corpus)
	if norm == 2: # Stemming
		corpus = stemmating(corpus)
	if user_stopwords is not None: # remove user's stopwords
		corpus = remove_stopwords_user(corpus, user_stopwords)
	if clean == 1: # remove stopwords
		corpus = remove_stopwords_basique(corpus)
	if clean == 2: # clean corpus
		corpus = clean_corpus(corpus)
	if str.isnumeric(str(clean))==False and len(clean)>0: # clean and remove stopwords
		corpus = clean_corpus(corpus)
		corpus = remove_stopwords_basique(corpus)
	return corpus	
	
			
# Fréquence des mots sur l'ensemble du corpus
def frequenceCorpus(corpus, norm, clean, user_stopwords):
	#corpus=preprocessing(corpus, norm, clean, user_stopwords)
	texts = '' 
	for text in corpus:
		texts = texts+' '+ str(text)
			
	corp = texts.split()
	freq = nltk.FreqDist(corp)
	dict_freq = {}
	for key, value in freq.items():
		dict_freq[key] = [key, value]
	
	data_frame_freq = pd.DataFrame(dict_freq)
	data_frame_freq = data_frame_freq.transpose()
	data_frame_freq.columns = ['word','count']
	return data_frame_freq
			
# Fréquence des mots ur chaque document
def frequenceDocument(df, norm, clean, user_stopwords):
	#corpus = preprocessing(df.iloc[0,:], norm, clean, user_stopwords)
	corpus = df.iloc[0,:]
	texts = ''
	df.iloc[0,:] = corpus
	# Initialiser
	vectorizer = CountVectorizer()
	doc_vec = vectorizer.fit_transform(df.iloc[0])
	
	words = doc_vec.toarray()
	
	
	df1 = pd.DataFrame(words.transpose(),index=vectorizer.get_feature_names())
	
	# Change column headers
	#df1.columns = df.columns
	return df1

# Document Term Matrix
def DTM(df):
	#corpus = preprocessing(df.iloc[0,:], norm, clean, user_stopwords)

	# Initialiser
	vectorizer = CountVectorizer()
	doc_vec = vectorizer.fit_transform(df.iloc[0,:])
	
	words = doc_vec.toarray()
	
	df1 = pd.DataFrame(words.transpose(),index=vectorizer.get_feature_names())
	
	# Change column headers
	df1.columns = df.columns
	return df1.transpose()

