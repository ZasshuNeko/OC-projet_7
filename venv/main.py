# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient le corp de l'application."""

from flask import Flask, render_template, request, jsonify
import json

from traitement import Traitement
from fichierjson import Sourcejson

# nltk.download('stopwords')
app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=['GET'])
def index():
    """Permet de charger la page d'accueille."""
    discution = "Hooooo ! Tu es venu voir papy ? Tu sais j'ai vécu très longtemps et je connais beaucoup de choses !"
    return render_template(
        'accueil.html',
        titre="Bienvenue !",
        corps=discution)


@app.route('/search_api', methods=['POST'])
def search_api():
    """Permet de charger la page après un "POST"."""
    demande = request.form.get('demande')

    traitement = Traitement()
    gestion_demande = traitement.gestion_question(demande)

    creationJSON = Sourcejson()
    reponse_json = creationJSON.creation_json(
        demande, gestion_demande)

    return jsonify(reponse_json)


@app.context_processor
def titre_page():
    """Permet d'utiliser 'titre_page' pour introduire le nom de la page sur le
    template."""
    return dict(titre_page="OC-Projet N°7")


if __name__ == '__main__':
    app.run(debug=True)
