# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient le corp de l'application
"""

import json
import unicodedata

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
	Permet de charger la page d'accueille
	"""
	discution = "Hooooo ! Tu es venu voir papy ? Tu sais j'ai vécu très longtemps et je connais beaucoup de choses !"
	return render_template(
		'accueil.html',
		titre="Bienvenue !",
		corps=discution)

@app.route('/search_api', methods= ['POST'])
def search_api():
	"""
	Permet de charger la page après un "POST"
	"""
	demande = request.form.get('demande');
	gestion_demande = gestion_question(demande);
	reponse_json = creation_json(demande,gestion_demande)
	return jsonify(reponse_json)

def gestion_question(demande):
	"""
	Charge la question de l'utilisateur et de la traiter et de l'envoyer vers les API google et wikipedia
	"""
	# Appel la fonction qui corrige l'orthographe des mots important et ramène s'il y a une salutation
	correctif_demande = correction_demande(demande)
	liste_demande = correctif_demande[0]
	# Retire les stopword de la liste des mots fait à partir de la demande
	filtered_words = [
		word for word in liste_demande if word not in stopwords.words('French')]
	for index, mot in enumerate(filtered_words):
		search_wiki = chercher_termes(mot) #, filtered_words
		if mot == 'où' or mot == "adresse" or search_wiki == 1:
			if search_wiki == 1:
				reponse_wiki = api_wiki("N_o_", filtered_words[index + 1], search_wiki,"N_o_")
				reponse_apigoogle = "None"
			else:
				reponse_apigoogle = api_google(filtered_words[index + 1])
				reponse_wiki = api_wiki(reponse_apigoogle[2], filtered_words[index + 1], search_wiki,reponse_apigoogle[2])
	return [reponse_apigoogle, reponse_wiki, correctif_demande[1]]

def correction_demande(demande):
	""" 
	En utilisant nltk nous scindons la demande de l'utilisateur en liste de terme, nous profitons d'appliquer
	des corrections pour l'orthorgraphe de certain mots. Nous ramenons aussi la capacité de déterminer si
	l'utilisateur à saluer papy
	"""
	tokenizer = nltk.RegexpTokenizer(r'\w+')
	demande_minuscule = demande.lower()
	demande_minuscule = "".join((c for c in unicodedata.normalize('NFD', demande_minuscule) if unicodedata.category(c) != 'Mn'))
	liste_demande = tokenizer.tokenize(demande_minuscule)
	for index, mot in enumerate(liste_demande):
		if index + 1 >= len(liste_demande):
			break
		elif mot == "ou" and liste_demande[index + 1] == "est" or liste_demande[index + 1] == "sont":
			liste_demande[index] = "où"
	salutation = salutation_utilisateur(liste_demande[0])
	return [liste_demande, salutation]

def salutation_utilisateur(terme):
	"""
	Gérer si utilisateur à salué papy
	"""
	if terme == "salut" or terme == "bonjour" or terme == "yo":
		salutation = 1
	else:
		salutation = 0
	return salutation

def creation_json(demande,gestion_demande):
	if len(gestion_demande[0]) == 3:
		demande = "<li class='list-group-item list-group-item-warning'>Vous : " + demande + "</li>";
		url_google = "<li class='list-group-item list-group-item-success'><img src=" + gestion_demande[0][0] + " class='img-fluid' /></li>"
		reponse_papy = papy_reponse(gestion_demande[0][1])
		papy_wiki = "<li class='list-group-item list-group-item-success'><p>" + gestion_demande[1] + "</p></li>"
		dictionnaire = {'resultat' : demande, 'url_google' : url_google, 'localisation' : reponse_papy, 'wiki' : papy_wiki}
		fichier_json = json.dumps(dictionnaire)
		return fichier_json
	else:
		demande = "<li class='list-group-item list-group-item-warning'>Vous : " + demande + "</li>";
		papy_wiki = "<li class='list-group-item list-group-item-success'><p>" + gestion_demande[1] + "</p></li>"
		dictionnaire = {'resultat' : demande, 'url_google' : "", 'localisation' : "", 'wiki' : papy_wiki}
		fichier_json = json.dumps(dictionnaire)
		return fichier_json

def papy_reponse(adresse):
	"""
	Génère la réponse de papy
	"""
	ss_chaine = str(adresse[0:1])
	if ss_chaine.isalpha() == False:
		indication_papy = reponse_add(adresse)
	else:
		indication_papy = reponse_nom(adresse)	
	indication_papy = "<li class='list-group-item list-group-item-success'>Papy : " + indication_papy + "</li>"	
	return indication_papy

def reponse_nom(adresse):
	"""
	Réponse formaté avec nom devant l'adresse
	"""
	texte_papy = adresse.split(",")
	x = 0
	if len(texte_papy) > 1:
		while x <= len(adresse):
			if x == 0:
				indication_papy = "Alors mon petit ! Sache que " + texte_papy[x]
			elif x == 1:
				indication_papy = indication_papy + " est situé " + texte_papy[x]
			elif x == 2:
				indication_papy = indication_papy +  " code postal " + texte_papy[x]
			x += 1
	elif len(texte_papy) == 1:
		indication_papy = "Mon petit il y a trop d'adresse !"
	return indication_papy

def reponse_add(adresse):
	"""
	Réponse formaté sans le nom de la recherche
	"""
	texte_papy = adresse.split(",")
	x = 0
	if len(texte_papy) > 1:
		while x <= len(adresse):
			if x == 0:
				indication_papy = "Alors mon petit ! Sache que cela est situé " + texte_papy[x]
			elif x == 1:
				indication_papy = indication_papy +  " code postal " + texte_papy[x]
			x += 1
	return indication_papy

def api_google(terme_important):
	"""
	Permet d'initialiser la classe gérant l'api google et de l'intéroger avec le terme important
	de la question.
	"""
	apigoogle = Api_google()
	resultat = apigoogle.search_api(terme_important)
	return resultat

def api_wiki(terme_important,demande, search_wiki,rue_google):
	"""
	Permet d'initialiser la classe gérant l'api wikipedia et de l'intéroger avec le terme important
	de la question.
	"""
	apiwiki = Api_wiki()
	resultat = apiwiki.search_api(terme_important,demande, search_wiki,rue_google)
	return resultat

def chercher_termes(mot):
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

@app.context_processor
def titre_page():
	"""
	Permet d'utiliser 'titre_page' pour introduire le nom de la page sur le template
	"""
	return dict(titre_page="OC-Projet N°7")


if __name__ == '__main__':
	app.run(debug=True)
