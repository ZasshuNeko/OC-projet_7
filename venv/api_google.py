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
		self.carte_api = '&map_action=map'

	def search_api(self, demande):
		"""Créer la demande et permet d'obtenir la réponse avec la variable selection
		"""
		question_api = self.adresse_api + demande + self.carte_api
		r = requests.get(question_api)
		reponse = str(r.content)
		# Permet de sélectionner le lien vers l'image google map
		selection = selection_api(reponse)
		return selection


def selection_api(reponse):
	"""Cette fonction sélectionne l'image dans la réponse de l'API google
	"""
	liste_reponse = reponse.split()
	for x in liste_reponse:
		reponse_index = liste_reponse.index(x)
		if x.find('content="https') != -1:
			lock_reponse = x
			break
	if len(lock_reponse) == 0:
		lock_reponse = "None"
	# Permet de formater le lien html pour qu'il soit lisible par la template
	html = recuperation_html(lock_reponse)
	return html


def recuperation_html(selection):
	""" Formate le lien html
	"""
	html = selection.replace('content="', '')
	html = html.replace('"', '')
	html = html.replace('&amp;', '&')
	return html
