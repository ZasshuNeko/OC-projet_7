import requests
import sys
import json


class Api_google:


    def __init__(self):
    	self.adresse_api = 'https://www.google.com/maps/search/?api=1&query='
    	self.carte_api = '&map_action=map'

    def search_api(self,demande):
    	question_api = self.adresse_api + demande + self.carte_api
    	r = requests.get(question_api)
    	reponse = str(r.content)
    	selection = selection_api(reponse)
    	return selection

def selection_api(reponse):
	liste_reponse = reponse.split()
	for x in liste_reponse :
		reponse_index = liste_reponse.index(x)
		if x.find('content="https') != -1:
			lock_reponse = x
			break
	if len(lock_reponse) == 0:
		lock_reponse = "None"
	html = recuperation_html(lock_reponse)
	return html


def recuperation_html(selection):
	html = selection.replace('content="','')
	html = html.replace('"','')
	html = html.replace('&amp;','&')
	return html

