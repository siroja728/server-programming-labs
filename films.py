from flask import Flask, jsonify, request

app = Flask(__name__)

films = [
    {'id': 1, 'title': 'Inception', 'director': 'Christopher Nolan'},
    {'id': 2, 'title': 'The Shawshank Redemption', 'director': 'Frank Darabont'},
    # інші фільми...
]

@app.route('/films', methods=['GET'])
def get_films():
    return jsonify(films)

@app.route('/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    film = next((film for film in films if film['id'] == film_id), None)
    if film is None:
        return jsonify({'message': 'Фільм не знайдено'}), 404
    return jsonify(film)

@app.route('/films', methods=['POST'])
def create_film():
    data = request.get_json()
    new_film = {'id': len(films) + 1, 'title': data['title'], 'director': data['director']}
    films.append(new_film)
    return jsonify(new_film), 201

@app.route('/films/<int:film_id>', methods=['PUT'])
def update_film(film_id):
    film = next((film for film in films if film['id'] == film_id), None)
    if film is None:
        return jsonify({'message': 'Фільм не знайдено'}), 404
    data = request.get_json()
    film['title'] = data['title']
    film['director'] = data['director']
    return jsonify(film)

@app.route('/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    film = next((film for film in films if film['id'] == film_id), None)
    if film is None:
        return jsonify({'message': 'Фільм не знайдено'}), 404
    films.remove(film)
    return jsonify(film)

if __name__ == '__main__':
    app.run(debug=True)
