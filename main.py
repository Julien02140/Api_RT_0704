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
#A change

@app.route('/api/recherche/<string:chaine>')
def recherche(chaine):
    return chaine

def chercher_videotheque(user_id):
    for video in videotheque:
        id_video = video.get("id_utilisateur")   
        print("id video :",id_video) 
        if id_video == user_id:
            print("videotheque trouve",video)
            return video
    return "erreur, ne trouve pas la videotheque du user"  

@app.route('/api/ma_videotheque/<int:id>') #id de l'utilisateur
def ma_videotheque(id):
    print("dans la fonction videotheque ")
    for video in videotheque:
        id_video = video.get("id_utilisateur")
        print("id video :",id_video)
        if id_video == id:
            liste_films = video.get("liste_films")
            print(liste_films)
            return jsonify({"liste_films": liste_films})
    return "pas trouve id utilisateur"
    
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
            id = utilisateur.get("id")
            return jsonify({"message": "Connexion OK","id": id})
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
def get_films_populaires():
    return jsonify(films_populaires)

@app.route('/api/trouver_film/<int:film_id>')
def trouver_film(film_id): #prends l'id du film en paramètre, retrouve le film dans films_populaires.json
    # Affiche tous les IDs dans la liste de films
    print("voici l'id du film",film_id)
    for film in films:
        if film['id'] == film_id:
            print(film["title"])
            return jsonify(film)
    for film in films_populaires:
        if film['id'] == film_id:
            print(film["title"])
            return jsonify(film)
        
    print("film pas trouve")
    return "erreur film non trouve"

@app.route('/api/ajout_film/<int:user_id>/<int:film_id>')
def ajout_film(user_id,film_id):
    print("AJOUT D UN FILM")
    film = trouver_film(film_id)
    video = chercher_videotheque(user_id)
    for film in video.get("liste_films"):
        if film == film_id:
            print("film deja dans la videothequ")
            return jsonify({"message" : "Deja dans la videotheque"})
    print("AJOUT DU FILM ID", film_id)
    print(video)
    nouv_video = video.get("liste_films")
    nouv_video.append(film_id)
    print("nouv_video ajouter")
    with open('videotheque.json', 'r+', encoding='utf-8') as json_file:
        json.dump(videotheque, json_file, ensure_ascii=False, indent=4)
    
    return jsonify({"message": "film ajouté"})
    
@app.route('/api/supprimer_film/<int:user_id>/<int:film_id>')
def supprimer_film(user_id,film_id):
    print("SUPPRIMER FILM DANS LA VIDEOTHEQUE, ID FILM :", film_id)
    film = trouver_film(film_id)
    for user in videotheque:
        if user["id_utilisateur"] == user_id:
            if film_id in user["liste_films"]:
                user["liste_films"].remove(film_id)
                print("film supprimé")
                with open('videotheque.json', 'r+', encoding='utf-8') as json_file:
                    json_file.seek(0)
                    json.dump(videotheque, json_file, ensure_ascii=False, indent=4)
                    json_file.truncate()
                return jsonify({"message" : "film supprimé"})  
            else:
                #normalement impossible de tomber dans cette condition
                print("l'id n'a pas été trouvé")
                return jsonify({"message": "pas trouvé"})
            
@app.route('/api/recherche_film/<string:mot>')
def recherche_film(mot):
    liste_films = []
    for film in films:
        if film["title"].lower().startswith(mot.lower()):
            liste_films.append(film)
    return jsonify({"liste_films" : liste_films})


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("5000"),debug=True)
    print("api start")

