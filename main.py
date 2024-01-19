from flask import Flask, jsonify, request,g
import json
import random
#installer request pour la method post

app = Flask(__name__)
serveur_url = "http://localhost:3000/verif_login"
#Je charge les données de mes fichiers json
with open('films.json', 'r+', encoding='utf-8') as json_file:
    films = json.load(json_file)

with open('films_populaires.json', 'r+', encoding='utf-8') as json_file:
    films_populaires = json.load(json_file)

with open('genres.json', 'r+', encoding='utf-8') as json_file:
    genres = json.load(json_file)

with open('utilisateur.json', 'r+', encoding='utf-8') as json_file:
    utilisateurs = json.load(json_file)

with open('videotheque.json', 'r+', encoding='utf-8') as json_file:
    videotheque = json.load(json_file)

def charger_user():
    with open('utilisateur.json', 'r+') as file:
        user_data = json.load(file)
    return user_data

@app.before_request
def before_request():
    g.next_id = 3 #Le prochain utilisateur inscrit aura cet id

@app.route('/api/recherche/<string:chaine>')
def recherche(chaine):
    return chaine

#cette route vérifie si le user est dans la base de donnée
@app.route('/api/verif_user', methods=['POST'])
def verif_user():
    utilisateurs = charger_user()
    donnee = request.form
    print(donnee)
    #récuper les infos de la requête POST
    pseudo_user = donnee.get("username")
    password_user = donnee.get("password")
    #On vérifie si le user est bien dans le json
    for utilisateur in utilisateurs:
        print(utilisateur.get("pseudo"))
        print(utilisateur.get("mot_de_passe"))
        if utilisateur.get("pseudo") == pseudo_user and utilisateur.get("mot_de_passe") == password_user:
            return jsonify({"message": "Connexion OK"})
    #si on arrive la, alors aucun utilisateur ne correspond
    return jsonify({"message": "NON"})

@app.route('/api/register_user',methods=['POST'])
def register_user():
    dico_user = charger_user()
    donnee  = request.form
    new_user = {
        "id": g.next_id,
        "nom" : donnee.get("lastname"),
        "prenom": donnee.get("firstname"),
        "pseudo": donnee.get("pseudo"),
        "age": donnee.get("age"),
        "mot_de_passe": donnee.get("password"),
        "email": donnee.get("email")
    }
    g.next_id = g.next_id + 1
    dico_user.append(new_user) #ajoute au dico user le nouvel user

    #ouvre le fichier utilisateur.json en écriture et écrit le contenu de dico_user
    with open('utilisateur.json', 'w') as fichier: 
        json.dump(dico_user, fichier, indent=2)
    
    return jsonify({"message":"Utilisateur ajouté"})

@app.route('/api/films_populaires')
def films_populaires():
    return jsonify(films_populaires)

@app.route('/api/trouver_film/<int:film_id>')
def trouver_film(film_id): #prends l'id du film en paramètre, retrouve le film dans films_populaires.json
    for film in films_populaires:
        if film['id'] == film_id:
            print(film["title"])
            return jsonify(film)
    return "erreur film non trouve"

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("5000"),debug=True)
    print("api start")

