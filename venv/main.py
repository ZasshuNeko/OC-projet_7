# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient le corp de l'application
"""

import json

import nltk
from flask import Flask, render_template, request, jsonify
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer

from api_google import Api_google
from api_wiki import Api_wiki

#nltk.download('stopwords')
app = Flask(__name__, static_url_path='/static')


@app.route('/', methods= ['GET'])
def index():
	"""
	Permet de charger la page d'accueille en get lors du chargement et en post lors de la demande
	"""
	discution = "Hooooo ! Tu es venu voir papy ? Tu sais j'ai vécu très longtemps et je connais beaucoup de choses !"
	return render_template(
		'accueil.html',
		titre="Bienvenue !",
		corps=discution)

@app.route('/search_api', methods= ['POST'])
def search_api():
	demande = request.form.get('demande');
	gestion_demande = gestion_question(demande);
	demande = "<li class='list-group-item list-group-item-success'>Vous : " + demande + "</li>";
	print(gestion_demande)
	return jsonify({'resultat' : "'" + demande + "'", 'url_google' : "'" + gestion_demande[0] + "'"})

def gestion_question(demande):
	"""
	Charge la question de l'utilisateur et de la traiter et de l'envoyer vers les API google et wikipedia
	"""
	# Appel la fonction qui corrige l'orthographe des mots important et ramène s'il y a une salutation
	# Ramène la liste des mots de la demande
	correctif_demande = correction_demande(demande)
	liste_demande = correctif_demande[0]
	# Retire les stopword de la liste des mots fait à partir de la demande
	filtered_words = [
		word for word in liste_demande if word not in stopwords.words('French')]
	for index, mot in enumerate(filtered_words):
		#search_wiki = chercher_termes(mot, filtered_words)
		if mot == 'où' or mot == "adresse":
			reponse_apigoogle = api_google(filtered_words[index + 1])
	return [reponse_apigoogle, correctif_demande[1]]

def correction_demande(demande):
	""" 
	En utilisant nltk nous scindons la demande de l'utilisateur en liste de terme, nous profitons d'appliquer
	des corrections pour l'orthorgraphe de certain mots. Nous ramenons aussi la capacité de déterminer si
	l'utilisateur à saluer papy
	"""
	tokenizer = nltk.RegexpTokenizer(r'\w+')
	demande_minuscule = demande.lower()
	liste_demande = tokenizer.tokenize(demande_minuscule)
	for index, mot in enumerate(liste_demande):
		if index + 1 >= len(liste_demande):
			break
		elif mot == "ou" and liste_demande[index + 1] == "est" or liste_demande[index + 1] == "sont":
			liste_demande[index] = "où"

	if liste_demande[0] == "salut" or liste_demande[0] == "bonjour" or liste_demande[0] == "yo":
		salutation = 1
	else:
		salutation = 0
	return [liste_demande, salutation]

def api_google(terme_important):
	"""
	Permet d'initialiser la classe gérant l'api google et de l'intéroger avec le terme important
	de la question.
	"""
	apigoogle = Api_google()
	resultat = apigoogle.search_api(terme_important)
	return resultat

@app.context_processor
def titre_page():
	"""
	Permet d'utiliser 'titre_page' pour introduire le nom de la page sur le template
	"""
	return dict(titre_page="OC-Projet N°7")


if __name__ == '__main__':
	app.run(debug=True)
