from flask import Flask, request,json,g
import json
import random
import requests
#installer request pour la method post
#post est utilisé pour modifier ou ajouter à la base de donnée
#alors que get est utilisé pour lire, extraire des données

app_TMDB = Flask(__name__)
api_key_TMDB = "8770fea03d8b0d550c4b50be1656d5cb"

#permet de recuperer des films dans l'api de TMDB, lorsqu'on envoie
#une requête avec de grands résultats, l'api TMDB divise les films en
#groupe de pages, j'en prends seulement 3 pour éviter d'avoir trop de films
#dans mon film.json
def get_film():
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key_TMDB}&language=fr&page=1"
    liste_films = []
    for i in range(1,4):
        params = {
            'vote_average.gte': 7,
            'vote_count.gte': 100,
            'page': i #je recupere 3 pages de films
        }
        response = requests.get(url, params=params)
        data = response.json()
        if response.status_code == 200:
            films = data.get('results', [])
            if films:
                with open('films.json', 'w', encoding='utf-8') as fichier:
                    json.dump(films, fichier, indent=2)
                    print("ecriture sur films.json")
            else:
                print("Échec de la récupération des films.")
        else:
            print(f"Erreur {response.status_code}: Impossible de récupérer la liste des films.")

    print("Les données ont été enregistrées dans films.json")


def genre_film():
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key_TMDB}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        genres = data['genres']
        with open('genres.json', 'w', encoding='utf-8') as fichier:
            json.dump(genres, fichier, indent=2)
    else:
        print(f"Erreur {response.status_code}: Impossible de récupérer la liste des genres.")


   
def trouver_film(id): #prends l'id du film en paramètre, retrouve le film dans films_populaires.json
    with open('films_populaires.json', 'r', encoding='utf-8') as fichier:
         films = json.load(fichier)
         for film in films:
             if film['id'] == id:
                  print(film["title"])
                  return 
    return "erreur film non trouve"
    


def afficher_image():
    base_url = "https://image.tmdb.org/t/p/w342"
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
    image_url2 = base_url + film["poster_path"]
    print("URL de l'image :", image_url)
    print("URL de l'image 2 :", image_url2)

#renvoie les films populaires du moment à afficher sur la page home
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
    get_film()
    get_popular_movie()