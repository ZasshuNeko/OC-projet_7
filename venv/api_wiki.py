import requests
import sys
import json


class Api_wiki:

    def __init__(self):
        self.adresse_api = 'https://fr.wikipedia.org/w/api.php'
        self.action = "opensearch"
        self.action_parse = "parse"
        self.prop = "wikitext"
        self.limite = "5"
        self.format = "json"

    def search_api(self, demande, search_wiki):
        parametres = {
            "action": self.action_parse,
            "page": demande,
            "prop": self.prop,
            "section": 5,
            "format": self.format
        }
        r = requests.get(url=self.adresse_api, params=parametres)
        reponse = r.json()
        chaine_content = try_content(reponse, demande)
        split_chaine = chaine_content[0].split("\n")
        if chaine_content[1] == "None":
            chaine_finale = gestion_chaine(split_chaine,search_wiki)
        else :
            chaine_finale = chaine_content[1]
        return chaine_finale


def recuperation_text(chaine_content):
    chaine_selecte = chaine_content.replace("[[", "")
    chaine_selecte = chaine_selecte.replace("]]", "")
    correction_chaine = chaine_selecte.split(" ")
    terme_retirer = modification_chaine(correction_chaine)
    chaine_finale = []
    print(terme_retirer[0])
    for index, mot in enumerate(terme_retirer[1]):
        if index not in terme_retirer[0]:
            chaine_finale.append(mot)
    return chaine_finale

def modification_chaine(correction_chaine):
    terme_remplacer = {'{{': "",'}}' : "",'nombre|' : "" ,'|' : " "}
    terme_retirer = []
    for index, mot in enumerate(correction_chaine):
        for terme in terme_remplacer.keys():
            mot = mot.replace(terme,terme_remplacer.get(terme))
            correction_chaine[index] = mot
        if mot.find('<ref') != -1 or mot.find('</ref') != -1:
            terme_retirer = terme_jeter(index,correction_chaine,terme_retirer)
    return [terme_retirer,correction_chaine]


def try_content(reponse,demande):
    try:
        chaine_content = reponse['parse']['wikitext']['*']
    except KeyError:
        error = "Mais... je n'ai rien à te dire sur " + demande + " !"
        chaine_content = "None"
    else:
        error = "None"

    return [chaine_content,error]

def gestion_chaine(split_chaine,search_wiki):
    for index, x in enumerate(split_chaine):
        if search_wiki == 0:
            if x[0:2].find('=') == -1:
                index_selecte = index
                correction_chaine = recuperation_text(split_chaine[index_selecte])
                break
        elif search_wiki == 1:
            s = " "
            all_chaine = s.join(split_chaine)
            all_chaine = all_chaine.replace("<", " <")
            correction_chaine = recuperation_text(all_chaine)
    s = " "
    chaine_finale = s.join(correction_chaine)
    return chaine_finale

def terme_jeter(index,correction_chaine,terme_retirer):
    x = 0
    while correction_chaine[index+x].find('</ref>') == -1:
        terme_retirer.append(index+x)
        x += 1
    if x == 0:
        terme_retirer.append(index)
    else:
        terme_retirer.append(index+x+1)
    return terme_retirer

