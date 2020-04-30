# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les tests du fichier main
"""

import json
import sys

import requests
import requests_mock

import main as script
import api_wiki as script_api

class Testmain:

	def setup_method(self):
		self.correction = script.correction_demande("Ou est OpenClassrooms ?")
		self.salutation = script.salutation_utilisateur("bonjour")

	def test_reponse_papy_add(self):
		reponse_papy = script.papy_reponse('test',False,["lien","25 rue test,75000 Paris","add"])
		assert reponse_papy == "<li class='list-group-item list-group-item-success'>Papy : test</br>Alors mon petit ! Sache que cela est situé 25 rue test code postal 75000 Paris</li>"	

	def test_reponse_papy_nom(self):
		reponse_papy = script.papy_reponse("TrucTruc,25 rue test,75000 Paris")
		assert reponse_papy == "<li class='list-group-item list-group-item-success'>Papy : Alors mon petit ! Sache que TrucTruc est situé 25 rue test code postal 75000 Paris</li>"	

	def test_correction_demande(self):
		assert self.correction == [["où","est","openclassrooms"],0]

	def test_salutation(self):
		assert self.salutation == 1

	def test_chercher_terme(self):
		terme = script.chercher_termes("quoi")
		assert terme == 1

def test_request(monkeypatch):

	class MockResponse(object):
		def __init__(self):
			self.status_code = 200
			self.url = "https://fr.wikipedia.org/w/api.php"
			self.headers = {"test":'1234'}
		def json(self):
			return {'Pytest' : 'Réponse test'}

	def mock_get(url):
		return MockResponse

	monkeypatch.setattr(requests,"get",mock_get)
	result = script_api.api_wikipedia("TEST","query","search","json","https://fr.wikipedia.org/w/api.php",requests.Session(),[])
	assert result == {'Pytest' : 'Réponse test'}
