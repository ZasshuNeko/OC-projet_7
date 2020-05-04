# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient le corp de l'application."""

from api_google import Api_google
from api_wiki import Api_wiki
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer
import unicodedata

import nltk


class Traitement:
    def __init__(self):
        self.liste_terme = [
            "connais",
            "connaitre",
            "connait",
            "sais",
            "sait",
            "savoir",
            "quoi",
            "où",
            "adresse"]

    def gestion_question(self, demande):
        """Charge la question de l'utilisateur et de la traiter et de l'envoyer
        vers les API google et wikipedia."""
        # Appel la fonction qui corrige l'orthographe des mots
        # important et ramène s'il y a une salutation
        correctif_demande = self.correction_demande(demande)
        liste_demande = correctif_demande[0]
        terme_selection = self.chercher_termes(liste_demande)
        search_terme = terme_selection[0]

        if terme_selection[1]:
            reponse_apigoogle = []
            reponse_wiki = search_terme
        else:
            reponse_apigoogle = self.api_google(search_terme)
            if len(reponse_apigoogle) >= 3:
                reponse_wiki = self.api_wiki(
                    search_terme, reponse_apigoogle[2])
            else:
                reponse_wiki = self.api_wiki(search_terme)
        return [
            reponse_apigoogle,
            reponse_wiki,
            correctif_demande[1],
            terme_selection[1]]

    def correction_demande(self, demande):
        """En utilisant nltk nous scindons la demande de l'utilisateur en liste
        de terme, nous profitons d'appliquer des corrections pour
        l'orthorgraphe de certain mots.

        Nous ramenons aussi la capacité de déterminer si l'utilisateur à
        saluer papy
        """
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        demande_minuscule = demande.lower()
        demande_minuscule = "".join((c for c in unicodedata.normalize(
            'NFD', demande_minuscule) if unicodedata.category(c) != 'Mn'))
        liste_demande = tokenizer.tokenize(demande_minuscule)
        for index, mot in enumerate(liste_demande):
            if index + 1 >= len(liste_demande):
                break
            elif mot == "ou" and liste_demande[index + 1] == "est" or liste_demande[index + 1] == "sont":
                liste_demande[index] = "où"
        salutation = self.salutation_utilisateur(liste_demande[0])
        return [liste_demande, salutation]

    def chercher_termes(self, liste_demande):
        """Permet de déterminer s'il y a un terme intéréssant pour l'API
        wikipedia, cela se base sur différent terme que l'on va chercher."""
        error = False
        # Retire les stopword de la liste des mots fait à partir de la
        # demande
        filtered_words = [
            word for word in liste_demande if word not in stopwords.words('French')]
        for index, mot in enumerate(filtered_words):
            if mot in self.liste_terme:

                try:
                    terme = filtered_words[index + 1]
                except BaseException:
                    terme = " Quoi répète plus fort ?!!"
                    error = True
                break
        return [terme, error]

    def api_google(self, terme_important):
        """Permet d'initialiser la classe gérant l'api google et de l'intéroger
        avec le terme important de la question."""
        apigoogle = Api_google()
        resultat = apigoogle.search_api(terme_important)
        return resultat

    def api_wiki(self, terme_important, *autres):
        """Permet d'initialiser la classe gérant l'api wikipedia et de
        l'intéroger avec le terme important de la question."""
        apiwiki = Api_wiki()
        resultat = apiwiki.search_api(terme_important, autres)
        return resultat

    def salutation_utilisateur(self, terme):
        """Gérer si utilisateur à salué papy."""
        if terme == "salut" or terme == "bonjour" or terme == "yo":
            salutation = "Un jeune bien élevé comme on les apprécie tant ! "
        else:
            salutation = "Petit malotrue ! On salut son ainé avant de demander ... "
        return salutation
