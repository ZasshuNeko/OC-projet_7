# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient le corp de l'application
"""

import json

import nltk
from flask import Flask, render_template, request
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer

from api_google import Api_google
from api_wiki import Api_wiki

nltk.download('stopwords')
app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=['GET', 'POST'])
def index():
	"""
	Permet de charger la page d'accueille en get lors du chargement et en post lors de la demande
	"""
	global discution
	gestion_reponse = ""
	if request.method == 'POST':
		demande = request.form['discution']
		# Permet de ramener les réponses de l'API et s'il y a une salutation
		brute_reponse = gestion_question(demande)
		# Génère l'historique de la discution
		historique_discution = gerer_discution(
			discution, demande, brute_reponse)
		return render_template(
			'accueil.html',
			titre="Bienvenue !",
			corps=historique_discution)
	elif request.method == 'GET':
		discution = [
			"Hooooo ! Tu es venu voir papy ? Tu sais j'ai vécu très longtemps et je connais beaucoup de choses !"]
		return render_template(
			'accueil.html',
			titre="Bienvenue !",
			corps=discution)


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
		search_wiki = chercher_termes(mot, filtered_words)
		if mot == 'où':
			reponse_apigoogle = api_google(filtered_words[index + 1])
			reponse_wiki = api_wiki(filtered_words[index + 1], search_wiki)
		elif len(filtered_words) == 1:
			reponse_apigoogle = api_google(filtered_words[0])
			reponse_wiki = api_wiki(filtered_words[index + 1], search_wiki)
		elif search_wiki == 1:
			reponse_wiki = api_wiki(filtered_words[index + 1], search_wiki)
			reponse_apigoogle = "None"
	return [reponse_apigoogle, reponse_wiki, correctif_demande[1]]


def api_google(terme_important):
	"""
	Permet d'initialiser la classe gérant l'api google et de l'intéroger avec le terme important
	de la question.
	"""
	apigoogle = Api_google()
	resultat = apigoogle.search_api(terme_important)
	return resultat


def api_wiki(terme_important, search_wiki):
	"""
	Permet d'initialiser la classe gérant l'api wikipedia et de l'intéroger avec le terme important
	de la question.
	"""
	apiwiki = Api_wiki()
	resultat = apiwiki.search_api(terme_important, search_wiki)
	return resultat


def chercher_termes(mot, demande):
	""" 
	Permet de déterminer s'il y a un terme intéréssant pour l'API wikipedia, cela se base sur
	différent terme que l'on va chercher
	"""
	wiki = 0
	liste_terme = [
		"connais",
		"connaitre",
		"connait",
		"sais",
		"sait",
		"savoir",
		"quoi"]
	if mot in liste_terme:
		wiki = 1
	return wiki


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


def gerer_discution(liste_discution, demande, api_google):
	"""
	Permet de former la réponse et la demande pour ainsi sauvegarder chaque échange
	Cette sauvegarde est fournis à la classe index pour reformer la page de la discution
	"""
	demande = 'vous : ' + demande
	reponse_papy = gerer_salutation(api_google[2])

	if api_google[0] != "None":
		reponse = 'papy : ' + reponse_papy + \
			' Bien sur que je sais où ça se trouve ! Tu me prends pour qui jeune homme ?'
		liste_discution.append(demande)
		liste_discution.append(reponse)
		x = 0
		while x < len(api_google):
			if not isinstance(api_google[x], int):
				if len(api_google[x]) > 0:
					liste_discution.append(api_google[x])
			x += 1
	# Réponse si uniquement réponse wiki
	elif api_google[0] == "None" and api_google[1] != "None":
		reponse = 'papy : ' + reponse_papy + \
			' Bien sur que je sais voyons ! Sache que ...'
		liste_discution.append(demande)
		liste_discution.append(reponse)
		x = 0
		while x < len(api_google):
			if not isinstance(api_google[x], int):
				if len(api_google[x]) > 0:
					if api_google[x] != "None":
						liste_discution.append(api_google[x])
			x += 1
	return liste_discution


def gerer_salutation(salutation):
	"""
	Permet d'ajouter le mécontentement de papy si vous ne lui dite pas bonjour
	"""
	if salutation == 1:
		reponse = "Un jeune bien élevé ! "
	else:
		reponse = "Petit malotrue ! soit plus polie avec les anciens ! "
	return reponse


@app.context_processor
def titre_page():
	"""
	Permet d'utiliser 'titre_page' pour introduire le nom de la page sur le template
	"""
	return dict(titre_page="OC-Projet N°7")


if __name__ == '__main__':
	app.run(debug=True)
