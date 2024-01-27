from flask import Flask, jsonify, request,g
import json
import hashlib
import os
#installer request pour la method post

app = Flask(__name__)

videotheque = []
films = []
#films_populaires= []
genres = []
utilisateurs = []

def lire_fichier_json(nom_fichier):
    chemin_fichier = os.path.join(os.path.dirname(__file__), '..', 'data', nom_fichier)

    with open(chemin_fichier, 'r+') as fichier:
        contenu_json = json.load(fichier)

    return contenu_json

def modifier_fichier_json(dico,nom_fichier):
    chemin_fichier = os.path.join(os.path.dirname(__file__), '..', 'data', nom_fichier)

    with open(chemin_fichier, 'r+') as fichier:
        fichier.seek(0)
        json.dump(dico, fichier, indent=2)
        fichier.truncate()
    return

videotheque = lire_fichier_json('videotheque.json')
films = lire_fichier_json('films.json')
#films_populaires = lire_fichier_json('films_populaires.json')
genres = lire_fichier_json('genres.json')
utilisateurs = lire_fichier_json('utilisateur.json')


def creer_videotheque(user_id):
    nouv_video = {

        "id_utilisateur": user_id,
        "liste_films": []
    }
    
    videotheque.append(nouv_video)

    modifier_fichier_json(videotheque,"videotheque.json")


@app.route('/get_user/<int:user_id>')
def get_user(user_id):
    for utilisateur in utilisateurs:
        if utilisateur['id'] == user_id:
            return jsonify(utilisateur)


@app.route('/recherche/<string:chaine>')
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

@app.route('/videotheque/<int:id>') #id de l'utilisateur
def ma_videotheque(id):
    liste_films = []
    print("dans la fonction videotheque ")
    for video in videotheque:
        id_video = video.get("id_utilisateur")
        print("id video videotheque :",id_video)
        if id_video == id:
            liste_films = video.get("liste_films")
            print(liste_films)
            return jsonify({"liste_films": liste_films})
    return jsonify({"liste_films": liste_films})
    
#cette route vérifie si le user est dans la base de donnée
@app.route('/verif_user', methods=['POST'])
def verif_user():
    donnee = request.form
    print(donnee)
    #récuper les infos de la requête POST
    pseudo_user = donnee.get("username")
    password_user = donnee.get("password")
    #On vérifie si le user est bien dans le json
    for utilisateur in utilisateurs:
        print(utilisateur.get("pseudo"))
        print(utilisateur.get("mot_de_passe"))
        password_chiffrer = hashlib.sha256(password_user.encode('utf-8')).hexdigest()
        print("mot de passe : ",password_chiffrer)
        if utilisateur.get("pseudo") == pseudo_user and password_chiffrer == utilisateur.get("mot_de_passe"):
            id = utilisateur.get("id")
            return jsonify({"message": "Connexion OK","id": id})
    #si on arrive la, alors aucun utilisateur ne correspond
    return jsonify({"message": "NON"})

def verif_donnee(pseudo,email):
    message_pseudo = "OK"
    message_mail = "OK"
    for utilisateur in utilisateurs:
        if utilisateur['pseudo'] == pseudo:
            message_pseudo = "pseudo déja utilisé"
        if utilisateur['email'] == email:
            message_mail = "mail déja utilisé"              
    return {"message_pseudo" : message_pseudo, "message_mail": message_mail}


@app.route('/register_user',methods=['POST'])
def register_user():
    donnee = request.form
    #verification du pseudo, on regarde si le nom n'est pas deja pris
    pseudo = donnee.get("pseudo")
    email = donnee.get("email")
    print("PSEUDO UTILISATEUR API",pseudo)
    verification = verif_donnee(pseudo,email)
    #si le bool est false, le pseudo n'estpas dans la base de donnée
    #on peut creer l'utilisateur
    if verification["message_pseudo"] == "OK" and  verification["message_mail"] == "OK":
        dernier_user = utilisateurs[-1]
        next_id = dernier_user["id"] + 1
        donnee  = request.form
        password = donnee.get("password")
        password_chiffrer = hashlib.sha256(password.encode('utf-8')).hexdigest()
        new_user = {
            "id": next_id,
            "nom" : donnee.get("lastname"),
            "prenom": donnee.get("firstname"),
            "pseudo": donnee.get("pseudo"),
            "age": donnee.get("age"),
            "mot_de_passe": password_chiffrer,
            "email": donnee.get("email")
        }
        utilisateurs.append(new_user) #ajoute au dico user le nouvel user

        modifier_fichier_json(utilisateurs,"utilisateur.json")

        creer_videotheque(next_id)
        
        return jsonify({"message":"Utilisateur ajouté"})
    else:
        return jsonify({"message" : "problème","message_pseudo" : verification['message_pseudo'],"message_mail": verification['message_mail']},)

@app.route('/films_populaires')
def get_films_populaires():
    films_populaires = films[:20]
    return jsonify(films_populaires)

@app.route('/trouver_film/<int:film_id>')
def trouver_film(film_id): #prends l'id du film en paramètre, retrouve le film dans films_populaires.json
    # Affiche tous les IDs dans la liste de films
    print("voici l'id du film",film_id)
    for film in films:
        if film['id'] == film_id:
            print(film["title"])
            return jsonify(film)
    """for film in films_populaires:
        if film['id'] == film_id:
            print(film["title"])
            return jsonify(film)"""
        
    print("film pas trouve")
    return "erreur film non trouve"

@app.route('/ajout_film/<int:user_id>/<int:film_id>')
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
    modifier_fichier_json(videotheque,"videotheque.json")    
    return jsonify({"message": "film ajouté"})
    
@app.route('/supprimer_film/<int:user_id>/<int:film_id>')
def supprimer_film(user_id,film_id):
    print("SUPPRIMER FILM DANS LA VIDEOTHEQUE, ID FILM :", film_id)
    film = trouver_film(film_id)
    for user in videotheque:
        if user["id_utilisateur"] == user_id:
            if film_id in user["liste_films"]:
                user["liste_films"].remove(film_id)
                print("film supprimé")
                modifier_fichier_json(videotheque,"videotheque.json")
                return jsonify({"message" : "film supprimé"})  
            else:
                #normalement impossible de tomber dans cette condition
                print("l'id n'a pas été trouvé")
                return jsonify({"message": "pas trouvé"})
            
@app.route('/recherche_film/<string:mot>')
def recherche_film(mot):
    liste_films = []
    for film in films:
        if film["title"].lower().startswith(mot.lower()):
            liste_films.append(film)
    print("liste des films trouvés api :",liste_films)
    return jsonify({"liste_films" : liste_films})

@app.route('/recherche_genre/<int:id>')
def recherche_genre(id):
    liste_films = []
    for film in films:
        liste_id = film["genre_ids"]
        for film_id in liste_id:
            if film_id == id:
                liste_films.append(film)
    return jsonify({"message" : liste_films})
        
"""@app.route('/ajout_note/<int:user_id>/<int:id_film>/<int:note>')
def ajout_note(user_id,id_film,note):
    deja_note = False
    nouvelle_evaluation = {"user_id": user_id, "vote": note}
    for film in films:
        if film['id'] == id_film:
            liste_evaluation = film.get('evaluation')
            liste_id = liste_evaluation['user_id']
            liste_note = liste_evaluation['vote']
            i = 0
            for id in liste_id:
                if id == user_id:
                    deja_note = True
                    liste_note[i] = note
                else:
                    i = i + 1
            if deja_note == False:
                film["evaluation"].append(nouvelle_evaluation)       

    modifier_fichier_json(films,"films.json")
    if deja_note == False:
        return jsonify({"message" : "Note ajouté"})
    else:
        return jsonify({"message" : "Note modifié"})"""

@app.route('/ajout_note/<int:user_id>/<int:id_film>/<int:note>')
def ajout_note(user_id, id_film, note):
    deja_note = False
    nouvelle_evaluation = {"user_id": user_id, "vote": note}
    for film in films:
        if film['id'] == id_film:
            liste_evaluation = film.get('evaluation', [])  # Utilisation de get avec une valeur par défaut vide si 'evaluation' n'existe pas
            liste_id = [item['user_id'] for item in liste_evaluation]
            i = 0
            for idx, user_id_eval in enumerate(liste_id):
                if user_id_eval == user_id:
                    deja_note = True
                    film["evaluation"][idx]["vote"] = note
                else:
                    i = i + 1
            if not deja_note:
                film['nb_vote'] = film['nb_vote'] + 1
                film["evaluation"].append(nouvelle_evaluation)
            calculer_moyenne(film)
            film_note = film

    modifier_fichier_json(films, "films.json")
    
    if not deja_note:
        return jsonify({"message": "Note ajoutée", "film_note" : film_note})
    else:
        return jsonify({"message": "Note modifiée", "film_note" : film_note})

def calculer_moyenne(film):
    vote_average = film['vote_average']
    vote_count_TMDB = film['vote_count']
    nb_vote = film['nb_vote']
    evaluation = film.get("evaluation")
    somme_notes = 0
    for notes in evaluation:
        somme_notes = somme_notes + notes['vote']
    moyenne = ((vote_average * vote_count_TMDB) + somme_notes) / (vote_count_TMDB + nb_vote)
    film['moyenne'] = round(moyenne,2)
    return

@app.route('/admin_liste_user')
def admin_liste_user():
    liste_user = []
    for utilisateur in utilisateurs:
        liste_user.append(utilisateur)
    return jsonify(liste_user)

@app.route('/supprimer_utilisateur/<int:user_id>')
def supprimer_utilisateur(user_id):
    liste_user = utilisateurs
    for utilisateur in utilisateurs:
        if utilisateur['id'] == user_id:
            liste_user.remove(utilisateur)

    modifier_fichier_json(utilisateurs,"utilisateur.json")
    return jsonify({"message" : "Utilisateur supprimé"})



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("5000"),debug=True)
    print("api start")

