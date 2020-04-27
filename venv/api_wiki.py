# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les fonctionnalités de l'API wikipedia
"""

import json
import sys

import requests


class Api_wiki:
	""" Cette classe permet d'émettre une demande via l'API wikipédia
	à l'initialisation nous chargeons les différentes variable dont on a besoin
	"""
	def __init__(self):
		self.adresse_api = 'https://fr.wikipedia.org/w/api.php'
		self.action =  "query"
		self.format = "json"
		self.liste = "search"

		self.session = requests.Session()

	def search_api(self, demande,question, search_wiki,rue_google):
		""" Permet d'éffectuer la recherche représenté par la variable demande
		"""
		x = 0
		r = api_wikipedia(demande,question,self.action,self.liste,self.format,rue_google,self.adresse_api,self.session)
		reponse = r.json()
		print(reponse)
		# Permet de tester la réponse
		chaine_content = try_content(reponse, demande)
		if chaine_content[0] == "None":
			print('Il est vide !')
		else:
			tab_reponse_papy = []
			for information in chaine_content[0]:
				if information.get("title") == demande and rue_google != "None" or  str(information.get("title")).lower() == question:
					information_selection = information.get("snippet")
					pageid = str(information.get("pageid"))
					reponse_papy = informations(information_selection,pageid,x,search_wiki)
					tab_reponse_papy.append(reponse_papy)
					x += 1
				elif search_wiki == 1 and information.get("snippet").find(question):
					information_selection = information.get("snippet")
					pageid = str(information.get("pageid"))
					reponse_papy = informations(information_selection,pageid,x,search_wiki)
					tab_reponse_papy.append(reponse_papy)
					break
			reponse_papy = " ".join(tab_reponse_papy)

		if chaine_content[1] == "None":
			# Permet de gérer la réponse
			chaine_finale = reponse_papy
		else:
			chaine_finale = chaine_content[1]
		return chaine_finale

def informations(information,pageid,nbr,search_wiki):
	information_papy = gestion_chaine(information,search_wiki)
	if nbr > 0:
		information_papy = "Holalala je peux même te dire encore plus de chose ..." + information_papy
	information_complementaire = ". Suit ce <a href='https://fr.wikipedia.org/?curid=" + pageid +"' >lien</a> et plus d'informaiton tu trouvera !"
	reponse_papy = information_papy + information_complementaire + "</br>"

	return reponse_papy

def config_request_demande(chaine,action,liste,format_self):
	parametres = {
		"action": action,
		"format": format_self,
		"list" : liste,
		"srsearch" : chaine
	}
	return parametres

def api_wikipedia(demande,question,action,liste,format_api,rue_google,adresse_api,session):
	if rue_google != "N_o_":
		parametres =  config_request_demande(demande,action,liste,format_api)
		r = session.get(url=adresse_api, params=parametres)
	else:
		parametres =  config_request_demande(question,action,liste,format_api)
		r = session.get(url=adresse_api, params=parametres)

	return r

def modification_chaine(correction_chaine):
	""" Permet de retirer les signes inutiles dût au formatage de la réponse
	"""
	terme_remplacer = {'{{': "", '}}': "", 'nombre|': "", '|': " "}
	terme_retirer = []
	for index, mot in enumerate(correction_chaine):
		for terme in terme_remplacer.keys():
			mot = mot.replace(terme, terme_remplacer.get(terme))
			correction_chaine[index] = mot
		if mot.find('<ref') != -1 or mot.find('</ref') != -1:
			# Permet de créer une liste d'entrée à retirer de la liste finale
			terme_retirer = terme_jeter(
				index, correction_chaine, terme_retirer)
	return [terme_retirer, correction_chaine]


def try_content(reponse, demande):
	""" Cette fonction effectue un test sur les réponses de l'API
	"""
	try:
		chaine_content = reponse['query']['search']
	except KeyError:
		error = "Mais... je n'ai rien à te dire sur " + demande + " !"
		chaine_content = "None"
	else:
		error = "None"

	return [chaine_content, error]

def gestion_chaine(chaine, search_wiki):
	"""Permet de récupérer la totalité ou partie de la réponse selon la demande de l'utilisateur
	"""
	if chaine.find('homonymes') != -1 or chaine.find('homonymie') != -1:
		homonyme_chaine = chaine.split(".")
		del homonyme_chaine[0]
		s = "."
		chaine = s.join(homonyme_chaine)
	chaine_selecte = chaine.replace("<", " <")
	chaine_selecte = chaine_selecte.replace(">", "> ")
	chaine_finale = chaine_selecte.split(" ")
	tableau_nw_chaine = []
	for index, mot in enumerate(chaine_finale):
		if mot.find('span') == -1 and mot.find('class') == -1 :
			tableau_nw_chaine.append(mot)
	s = " "
	chaine_finale = s.join(tableau_nw_chaine)
	return chaine_finale



