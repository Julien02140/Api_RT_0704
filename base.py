from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
db = SQLAlchemy(app)

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255))
    annee = db.Column(db.Integer)
    realisateur = db.Column(db.String(255))
    synopsis = db.Column(db.Text)

class Acteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255))
    prenom = db.Column(db.String(255))
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'))

# Route pour récupérer les informations d'un film par son ID
@app.route('/film/<int:film_id>', methods=['GET'])
def get_film(film_id):
    film = Film.query.get(film_id)
    if film:
        acteurs = Acteur.query.filter_by(film_id=film.id).all()
        acteurs_liste = [{'nom': acteur.nom, 'prénom': acteur.prenom} for acteur in acteurs]
        return jsonify({
            'titre': film.titre,
            'année': film.annee,
            'réalisateur': film.realisateur,
            'acteurs': acteurs_liste,
            'synopsis': film.synopsis
        })
    else:
        return jsonify({'message': 'Film non trouvé'}), 404

if __name__ == '__main__':
    app.run(debug=True)
