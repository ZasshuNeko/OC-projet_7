# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les fonctionnalités de l'API wikipedia."""

from bs4 import BeautifulSoup
import requests


class Api_wiki:
    """Cette classe permet d'émettre une demande via l'API wikipédia à
    l'initialisation nous chargeons les différentes variable dont on a
    besoin."""

    def __init__(self):
        self.adresse_api = 'https://fr.wikipedia.org/w/api.php'
        self.action = "query"
        self.format = "json"
        self.liste = "search"

        self.session = requests.Session()

    def search_api(self, terme_recherche, autres):
        """Permet d'éffectuer la recherche représenté par la variable
        demande."""
        reponse = api_wikipedia(
            terme_recherche,
            self.action,
            self.liste,
            self.format,
            self.adresse_api,
            self.session,
            autres)
        # Permet de tester la réponse
        chaine_content = try_content(reponse, terme_recherche)
        if chaine_content[1]:
            print('Il est vide !')
        else:
            tab_reponse_papy = creation_tableau_reponse(
                chaine_content[0], terme_recherche, autres)
            reponse_papy = " ".join(tab_reponse_papy)

        if not chaine_content[1]:
            # Permet de gérer la réponse
            chaine_finale = reponse_papy
        else:
            chaine_finale = chaine_content[1]

        return chaine_finale


def informations(information, pageid, nbr):
    """Création de la réponse de papy à partir de la réponse api."""
    information_papy = gestion_chaine(information)
    if nbr > 0:
        information_papy = "Holalala je peux même te dire encore plus de chose ..." + information_papy
    information_complementaire = ". Suit ce <a href='https://fr.wikipedia.org/?curid=" + \
        pageid + "' >lien</a> et plus d'informaiton tu trouvera !"
    reponse_papy = information_papy + information_complementaire + "</br>"

    return reponse_papy


def creation_tableau_reponse(reponse_information, demande, *autres):
    """Création du tableau pour générer la réponse."""
    x = 0
    tab_reponse_papy = []
    for information in reponse_information:
        if str(information.get("title")).lower() == demande:
            reponse_papy = recuperation_information(information, x)
            tab_reponse_papy.append(reponse_papy)
            x += 1
        else:
            if len(autres[0]) > 0:
                if str(information.get("title")).lower(
                ) == autres[0][0] or information.get("snippet").find(autres[0][0]):
                    reponse_papy = recuperation_information(
                        information, x)
                    tab_reponse_papy.append(reponse_papy)
                    x += 1
        if x > 1:
            break
    return tab_reponse_papy


def recuperation_information(information, x):
    """Récupération des informations dans le json."""
    information_selection = information.get("snippet")
    pageid = str(information.get("pageid"))
    reponse_papy = informations(information_selection, pageid, x)
    return reponse_papy


def config_request_demande(chaine, action, liste, format_self):
    """Paramétre de l'API."""
    parametres = {
        "action": action,
        "format": format_self,
        "list": liste,
        "srsearch": chaine
    }
    return parametres


def api_wikipedia(
        terme_recherche,
        action,
        liste,
        format_api,
        adresse_api,
        session,
        *autres):
    """Envoie de la requête à l'API."""
    if len(autres[0]) == 0:
        parametres = config_request_demande(
            terme_recherche, action, liste, format_api)
        r = session.get(url=adresse_api, params=parametres)
    else:
        parametres = config_request_demande(
            autres[0], action, liste, format_api)
        r = session.get(url=adresse_api, params=parametres)
    reponse = r.json()
    return reponse


def try_content(reponse, demande):
    """Cette fonction effectue un test sur les réponses de l'API."""
    try:
        chaine_content = reponse['query']['search']
    except KeyError:
        error = True
        chaine_content = "Mais... je n'ai rien à te dire sur " + demande + " !"
    else:
        error = False

    return [chaine_content, error]


def gestion_chaine(chaine):
    """Permet de récupérer la totalité ou partie de la réponse selon la demande
    de l'utilisateur."""
    if chaine.find('homonymes') != - \
            1 or chaine.find('homonymie') != -1:
        homonyme_chaine = chaine.split(".")
        del homonyme_chaine[0]
        s = "."
        chaine = s.join(homonyme_chaine)
    chaine_parser = BeautifulSoup(chaine, 'html.parser')
    chaine_finale = chaine_parser.get_text()
    return chaine_finale
