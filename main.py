from flask import Flask
import json
import random
#installer request pour la method post

app = Flask(__name__)

@app.route('/get-film', methods=['GET'])

def getFilm():

    listFilm = ['james bond', 'titanic','ratatouille']
    choix_film = listFilm[random.randint(0,2)]

    return json.dumps({"film" : choix_film})

@app.route('/get/<name>/<years>',methods=['GET'])
#exemple pour recuperer l info dans l'url
def getInfo(name, years):
    return "tu t appelle " + name + "et tu as " + years



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("5000"),debug=True)
    print("api start")

