from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
import logging

# Ініціалізація додатку та підключення до БД
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
db = SQLAlchemy(app)

# Логування вхідних запитів
logging.basicConfig(level=logging.INFO)

# Модель для фільмів
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    director = db.Column(db.String(120), nullable=False)

# Функція для перевірки чи є користувач авторизованим
def authenticate(username, password):
    # Перевірка логіну та паролю (спрощено, для прикладу)
    return username == 'admin' and password == 'admin'

# Захищені CRUD для фільмів
@app.route('/films', methods=['POST'])
def create_film():
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = data['username']
        password = request.args.get('password')  # Приклад параметра
        if authenticate(username, password):
            new_film = Film(title=request.json['title'], director=request.json['director'])
            db.session.add(new_film)
            db.session.commit()
            return jsonify({'message': 'Фільм створено'}), 201
        else:
            return jsonify({'message': 'Невірні дані для входу'}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Срок дії токену минув'}), 401
    except jwt.DecodeError:
        return jsonify({'message': 'Невірний токен'}), 401

@app.route('/films', methods=['GET'])
def get_films():
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        films = Film.query.all()
        return jsonify([{'id': film.id, 'title': film.title, 'director': film.director} for film in films]), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Срок дії токену минув'}), 401
    except jwt.DecodeError:
        return jsonify({'message': 'Невірний токен'}), 401

@app.route('/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        film = Film.query.get(film_id)
        if film is None:
            return jsonify({'message': 'Фільм не знайдено'}), 404
        return jsonify({'id': film.id, 'title': film.title, 'director': film.director}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Срок дії токену минув'}), 401
    except jwt.DecodeError:
        return jsonify({'message': 'Невірний токен'}), 401

@app.route('/films/<int:film_id>', methods=['PUT'])
def update_film(film_id):
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = data['username']
        password = request.args.get('password')  # Приклад параметра
        if authenticate(username, password):
            film = Film.query.get(film_id)
            if film is None:
                return jsonify({'message': 'Фільм не знайдено'}), 404

            film.title = request.json['title']
            film.director = request.json['director']

            db.session.commit()
            return jsonify({'id': film.id, 'title': film.title, 'director': film.director}), 200
        else:
            return jsonify({'message': 'Невірні дані для входу'}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Срок дії токену минув'}), 401
    except jwt.DecodeError:
        return jsonify({'message': 'Невірний токен'}), 401

@app.route('/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = data['username']
        password = request.args.get('password')  # Приклад параметра
        if authenticate(username, password):
            film = Film.query.get(film_id)
            if film is None:
                return jsonify({'message': 'Фільм не знайдено'}), 404

            db.session.delete(film)
            db.session.commit()

            return jsonify({'id': film.id, 'title': film.title, 'director': film.director}), 200
        else:
            return jsonify({'message': 'Невірні дані для входу'}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Срок дії токену минув'}), 401
    except jwt.DecodeError:
        return jsonify({'message': 'Невірний токен'}), 401

# ...

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
