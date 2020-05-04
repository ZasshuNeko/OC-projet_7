# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les tests du projet 7
"""

import json
import sys

import mock
import requests
import requests_mock
from io import BytesIO

import main as script
import api_wiki as script_wiki
import api_google as script_google


class Testmain:

    def setup_method(self):
        self.correction = script.correction_demande(
            "Ou est OpenClassrooms ?")
        self.salutation = script.salutation_utilisateur("bonjour")

    def test_reponse_papy_add(self):
        reponse_papy = script.papy_reponse(
            'test', False, [
                "lien", "25 rue test,75000 Paris", "add"])
        assert reponse_papy == "<li class='list-group-item list-group-item-success'>Papy : test</br>Alors mon petit ! Sache que cela est situé 25 rue test code postal 75000 Paris</li>"

    def test_reponse_papy_nom(self):
        reponse_papy = script.papy_reponse(
            "test", False, [
                "lien", "TrucTruc,25 rue test,75000 Paris", "add"])
        assert reponse_papy == "<li class='list-group-item list-group-item-success'>Papy : test</br>Alors mon petit ! Sache que TrucTruc est situé 25 rue test code postal 75000 Paris</li>"

    def test_correction_demande(self):
        assert self.correction == [["où", "est", "openclassrooms"],
                                   'Petit malotrue ! On salut son ainé avant de demander ... ']

    def test_salutation(self):
        assert self.salutation == 'Un jeune bien élevé comme on les apprécie tant ! '

    def test_chercher_terme(self):
        terme = script.chercher_termes(["quoi", "velo"])
        assert terme == ["velo", False]


class MockReponseWiki:
    @staticmethod
    def json():
        return {'Pytest': 'Réponse test'}


def test_request_wiki(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockReponseWiki()

    monkeypatch.setattr(requests, "get", mock_get)
    result = script_wiki.api_wikipedia(
        "TEST",
        "query",
        "search",
        "json",
        "https://fr.wikipedia.org/w/api.php",
        requests,
        ((),
         ))
    assert result['Pytest'] == 'Réponse test'


def test_request_google(monkeypatch):

    with mock.patch("requests.get") as patch_get:
        patch_get.return_value.content = "https://www.google/test, https://autrehtml"

        result = script_google.Api_google()
        resultsecond = result.search_api("OpenClassrooms")
        assert resultsecond == "Mes cartes ne trouvent pas ce que tu désire"
