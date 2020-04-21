from flask import Flask
from flask import render_template
from flask import request
import nltk
import json
from api_google import Api_google
from api_wiki import Api_wiki
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import stopwords

nltk.download('stopwords')
app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET','POST'])
def index():
	global discution
	gestion_reponse = ""
	if request.method == 'POST':
		demande = request.form['discution']
		brute_reponse = gestion_question(demande)
		gestion_reponse = brute_reponse
		historique_discution = gerer_discution(discution,demande,gestion_reponse, brute_reponse[2])
		return render_template('accueil.html', titre="Bienvenue !",corps=historique_discution)
	elif request.method == 'GET':
		discution = ["Hooooo ! Tu es venu voir papy ? Tu sais j'ai vécu très longtemps et je connais beaucoup de choses !"]
		return render_template('accueil.html', titre="Bienvenue !",corps=discution)

def gestion_question(demande):
	correctif_demande = correction_demande(demande)
	liste_demande = correctif_demande[0] 
	filtered_words = [word for word in liste_demande if word not in stopwords.words('French')]
	for index, mot in enumerate(filtered_words):
		search_wiki = chercher_termes(mot,filtered_words)
		print(search_wiki)
		if mot == 'où':
			reponse_apigoogle = api_google(filtered_words[index+1])
			reponse_wiki = api_wiki(filtered_words[index+1],search_wiki)
		elif len(filtered_words) == 1:
			reponse_apigoogle = api_google(filtered_words[0])
			reponse_wiki = api_wiki(filtered_words[index+1],search_wiki)
		elif search_wiki == 1:
			reponse_wiki = api_wiki(filtered_words[index+1],search_wiki)
			reponse_apigoogle = "None"


	return [reponse_apigoogle,reponse_wiki,correctif_demande[1]]

def api_google(terme_important):
	apigoogle = Api_google()
	resultat = apigoogle.search_api(terme_important)
	return resultat

def api_wiki(terme_important,search_wiki):
	apiwiki = Api_wiki()
	resultat = apiwiki.search_api(terme_important,search_wiki)
	return resultat

def chercher_termes(mot,demande):
	wiki = 0
	liste_terme = ["connais", "connaitre", "connait", "sais", "sait", "savoir", "quoi"]
	if mot in liste_terme:
		wiki = 1
	return wiki

def correction_demande(demande):
	tokenizer = nltk.RegexpTokenizer(r'\w+')
	demande_minuscule = demande.lower()
	liste_demande = tokenizer.tokenize(demande_minuscule)
	print(liste_demande)
	for index, mot in enumerate(liste_demande):
		if index + 1 >= len(liste_demande):
			break
		elif mot == "ou" and liste_demande[index+1] == "est" or liste_demande[index+1] == "sont":
			liste_demande[index] = "où"

	if liste_demande[0] == "salut" or liste_demande[0] == "bonjour" or liste_demande[0] == "yo":
		salutation = 1
	else :
		salutation = 0
	return [liste_demande,salutation]

def gerer_discution(liste_discution,demande,api_google,salutation):
	demande = 'vous : ' + demande
	reponse_papy = gerer_salutation(salutation)

	if api_google[0] != "None":
		reponse = 'papy : ' + reponse_papy + ' Bien sur que je sais où ça se trouve ! Tu me prends pour qui jeune homme ?'
		liste_discution.append(demande)
		liste_discution.append(reponse)
		x = 0
		while x < len(api_google):
			if type(api_google[x]) != int:
				if len(api_google[x]) > 0:
					liste_discution.append(api_google[x])
			x += 1
	elif api_google[0] == "None" and api_google[1] != "None" : #Réponse si uniquement réponse wiki
		reponse = 'papy : ' + reponse_papy + ' Bien sur que je sais voyons ! Sache que ...'
		liste_discution.append(demande)
		liste_discution.append(reponse)
		x = 0
		while x < len(api_google):
			if type(api_google[x]) != int:
				if len(api_google[x]) > 0:
					if api_google[x] != "None":
						liste_discution.append(api_google[x])
			x += 1

	return liste_discution

def gerer_salutation(salutation):
	if salutation == 1:
		reponse = "Un jeune bien élevé ! "
	else:
		reponse = "Petit malotrue ! soit plus polie avec les anciens ! "
	return reponse



@app.context_processor
def titre_page():
	return dict(titre_page="OC-Projet N°7")

if __name__ == '__main__':
	app.run(debug=True)