# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les tests du fichier api_wiki
"""

import json
import sys

import requests

class test_api_wiki:
	def test_request(monkeypatch):
		results = "Test"

		def mockreturn(request):
			return results

		monkeypatch.setattr(session,'get',mockreturn)
		assert script.api_wikipedia("Darty","où est darty","query","search","json","test","https://fr.wikipedia.org/w/api.php",requests.Session()) == results