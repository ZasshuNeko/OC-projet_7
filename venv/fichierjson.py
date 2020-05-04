# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient le corp de l'application."""

import json


class Sourcejson():
    def __init__(self):
        self.warning = "<li class='list-group-item list-group-item-warning'>Vous : "
        self.success = "<li class='list-group-item list-group-item-success'>"
        self.end = "</li>"

    def creation_json(self, demande, gestion_demande):
        if len(gestion_demande[0]) >= 1:
            demande = self.warning + demande + self.end
            url_google = self.success + "<img src=" + \
                gestion_demande[0][0] + " class='img-fluid' />" + self.end
            reponse_papy = self.papy_reponse(
                gestion_demande[2], gestion_demande[3], gestion_demande[0])
            papy_wiki = self.success + "<p>Papy :" + \
                gestion_demande[1] + "</p>" + self.end
        else:
            demande = self.warning + demande + self.end
            papy_wiki = self.success + "<p>Papy :" + \
                gestion_demande[1] + "</p>" + self.end
            url_google = ""
            reponse_papy = self.papy_reponse(
                gestion_demande[2], gestion_demande[3])

        dictionnaire = {
            'resultat': demande,
            'url_google': url_google,
            'localisation': reponse_papy,
            'wiki': papy_wiki}
        fichier_json = json.dumps(dictionnaire)
        return fichier_json

    def papy_reponse(self, salutation, boolean_error,
                     *adresse):
        """Génère la réponse de papy."""
        if boolean_error:
            indication_papy = self.success + \
                "Papy : Hmmmm attends ...heu..." + self.end
        else:
            selection_adresse = adresse[0]
            if len(selection_adresse) >= 2:
                lieu = selection_adresse[1]
                ss_chaine = str(lieu[0:1])
                if ss_chaine.isalpha() == False:
                    indication_papy = self.reponse_add(lieu)
                else:
                    indication_papy = self.reponse_nom(lieu)
            else:
                indication_papy = "Voyons, il y a beaucoup d'endroit pour tous te les citer"
            indication_papy = self.success + "Papy : " + \
                salutation + "</br>" + indication_papy + self.end
        return indication_papy

    def reponse_nom(self, adresse):
        """Réponse formaté avec nom devant l'adresse."""
        texte_papy = adresse.split(",")
        x = 0
        if len(texte_papy) > 1:
            while x <= len(adresse):
                if x == 0:
                    indication_papy = "Alors mon petit ! Sache que " + \
                        texte_papy[x]
                elif x == 1:
                    indication_papy = indication_papy + \
                        " est situé " + texte_papy[x]
                elif x == 2:
                    indication_papy = indication_papy + \
                        " code postal " + texte_papy[x]
                x += 1
        return indication_papy

    def reponse_add(self, adresse):
        """Réponse formaté sans le nom de la recherche."""
        texte_papy = adresse.split(",")
        x = 0
        if len(texte_papy) > 1:
            while x <= len(adresse):
                if x == 0:
                    indication_papy = "Alors mon petit ! Sache que cela est situé " + \
                        texte_papy[x]
                elif x == 1:
                    indication_papy = indication_papy + \
                        " code postal " + texte_papy[x]
                x += 1
        return indication_papy
