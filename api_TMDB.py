from flask import Flask, request,json,g
import json
import random
import requests
#installer request pour la method post
#post est utilisé pour modifier ou ajouter à la base de donnée
#alors que get est utilisé pour lire, extraire des données

app_TMDB = Flask(__name__)

def afficher_image():
    base_url = "https://image.tmdb.org/t/p/w500"
    film = {
        "adult": False,
        "backdrop_path": "/f1AQhx6ZfGhPZFTVKgxG91PhEYc.jpg",
        "genre_ids": [
        36,
        10752,
        18
        ],
        "id": 753342,
        "original_language": "en",
        "original_title": "Napoleon",
        "overview": "An epic that details the checkered rise and fall of French Emperor Napoleon Bonaparte and his relentless journey to power through the prism of his addictive, volatile relationship with his wife, Josephine.",
        "popularity": 2998.164,
        "poster_path": "/jE5o7y9K6pZtWNNMEw3IdpHuncR.jpg",
        "release_date": "2023-11-22",
        "title": "Napoleon",
        "video": False,
        "vote_average": 6.5,
        "vote_count": 1123
    }
    image_url = base_url + film["backdrop_path"]
    print("URL de l'image :", image_url)


def get_popular_movie():
    api_key = "8770fea03d8b0d550c4b50be1656d5cb"
    requete = "https://api.themoviedb.org/3/discover/movie?api_key=8770fea03d8b0d550c4b50be1656d5cb&sort_by=popularity.desc"
    url = "https://api.themoviedb.org/3/discover/movie?api_key=8770fea03d8b0d550c4b50be1656d5cb&sort_by=popularity.desc"

    reponse = requests.get(url)
    if reponse.status_code == 200:
        data = reponse.json()
        film_populaire = data.get('results', [])
        if film_populaire:
            with open('films_populaires.json', 'w', encoding='utf-8') as fichier:
                json.dump(film_populaire, fichier, indent=2)
            print("Fichier 'films_populaires.json' créé avec succès.")
        else:
            print("Échec de la récupération des films populaires.")
    else:
        print("Erreur lors de la requête")
        return None

if __name__ == '__main__':
    afficher_image()
    
