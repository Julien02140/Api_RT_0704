from flask import Flask, request
import json
import random
import requests
#installer request pour la method post
#post est utilisé pour modifier ou ajouter à la base de donnée
#alors que get est utilisé pour lire, extraire des données

app = Flask(__name__)

@app.route("/add-film", methods=['POST'])

def addPlayer():
    filmList = []

    data = request.get_json
    if "filmname" in data:
        filmList.append(data["filmname"])
        return "created"
    else:
        return "bad request"



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("5000"),debug=True)
    print("api start")

