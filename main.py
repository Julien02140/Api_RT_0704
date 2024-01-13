from flask import Flask, jsonify, request
import json
import random
#installer request pour la method post

app = Flask(__name__)
serveur_url = "http://localhost:3000/verif_login"
#Je charge les données de mon fichier utilisateur.json
def charger_user():
    with open('utilisateur.json', 'r') as file:
        user_data = json.load(file)
    return user_data

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

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("5000"),debug=True)
    print("api start")

