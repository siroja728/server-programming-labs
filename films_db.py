from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
db = SQLAlchemy(app)

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    director = db.Column(db.String(120), nullable=False)

@app.route('/films', methods=['GET'])
def get_films():
    films = Film.query.all()
    return jsonify([{'id': film.id, 'title': film.title, 'director': film.director} for film in films]), 200

@app.route('/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    film = Film.query.get(film_id)
    if film is None:
        return jsonify({'message': 'Фільм не знайдено'}), 404
    return jsonify({'id': film.id, 'title': film.title, 'director': film.director}), 200

@app.route('/films', methods=['POST'])
def create_film():
    data = request.get_json()
    new_film = Film(title=data['title'], director=data['director'])
    db.session.add(new_film)
    db.session.commit()
    return jsonify({'id': new_film.id, 'title': new_film.title, 'director': new_film.director}), 201

@app.route('/films/<int:film_id>', methods=['PUT'])
def update_film(film_id):
    film = Film.query.get(film_id)
    if film is None:
        return jsonify({'message': 'Фільм не знайдено'}), 404

    data = request.get_json()
    film.title = data['title']
    film.director = data['director']

    db.session.commit()
    return jsonify({'id': film.id, 'title': film.title, 'director': film.director}), 200

@app.route('/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    film = Film.query.get(film_id)
    if film is None:
        return jsonify({'message': 'Фільм не знайдено'}), 404

    db.session.delete(film)
    db.session.commit()

    return jsonify({'id': film.id, 'title': film.title, 'director': film.director}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
