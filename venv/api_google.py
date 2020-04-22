# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les fonctionnalités de l'API google
"""

import json
import sys

import requests


class Api_google:
	"""Cette classe permet de créer les demandes avec l'API google
	"""

	def __init__(self):
		self.adresse_api = 'https://www.google.com/maps/search/?api=1&query='
		#self.carte_api = '&map_action=map'

	def search_api(self, demande):
		"""Créer la demande et permet d'obtenir la réponse avec la variable selection
		"""
		question_api = self.adresse_api + demande #+ self.carte_api
		r = requests.get(question_api)
		reponse = str(r.content)
		#print(reponse)
		
		#print(test_split, len(test_split))
		# Permet de sélectionner le lien vers l'image google map
		selection = selection_api(reponse)
		return selection


def selection_api(reponse):
	"""Cette fonction sélectionne l'image dans la réponse de l'API google
	"""
	liste_reponse = reponse.split('"')
	reponse_tab = []
	for n in liste_reponse:
		if n.startswith("https://www.google") == True and n.find("/preview/") != -1:
			reponse_tab.append(n)
		elif n.startswith("https://maps.google") == True and n.find("&") != -1:
			if n not in reponse_tab:
				reponse_tab.append(n)

	print(reponse_tab)
	if len(reponse_tab) >= 1:
		lock_reponse = reponse_tab
		html = recuperation_html(lock_reponse)
	return html


def recuperation_html(selection):
	""" Formate le lien html
	"""
	localisation = ""
	for index, mot in enumerate(selection):
		if mot.find("https://www.google") != -1:
			html = mot.replace('\\', '')
			html = html.replace('u003d', '=')
			html = html.replace('%C3%A9', 'é')
			adresse_html = html.split("/")
			for index,terme in enumerate(adresse_html):
				if terme == "place":
					localisation = adresse_html[index+1]
					break
			localisation = localisation.replace("+", " ")
		elif mot.find("https://maps.google") != -1:
			html = mot.replace('&amp;', '&')
			lien = html
	if len(localisation) == 0:
		localisation = "None" 


	return [lien,localisation]
