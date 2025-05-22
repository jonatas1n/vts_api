import json
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def load_data(entity_name):
    """Carrega os dados de um arquivo JSON na pasta 'data'."""
    try:
        with open(f'data/{entity_name}.json', 'r') as f:
            data = json.load(f)
        # Cria um dicionário para facilitar a busca por ID
        return {item['id']: item for item in data}
    except FileNotFoundError:
        print(f"Erro: Arquivo data/{entity_name}.json não encontrado.")
        return {}
    except json.JSONDecodeError:
        print(
            f"Erro: Falha ao decodificar JSON de data/{entity_name}.json."
        )
        return {}


cages_by_id = load_data('cage')
drones_by_id = load_data('drone')
users_by_id = load_data('user')
missions_by_id = load_data('mission')


@app.route("/")
def hello_world():
    return 'its working'


@app.route("/cages")
def cages():
    return jsonify(list(cages_by_id.values()))


@app.route("/cages/<int:cage_id>", methods=["GET"])
def cage(cage_id):
    if cage_id in cages_by_id:
        return jsonify(cages_by_id[cage_id])
    return jsonify({"message": "Gaiola não encontrada"}), 404


@app.route("/drones")
def drones():
    return jsonify(list(drones_by_id.values()))


@app.route("/drones/<int:drone_id>")
def drone(drone_id):
    if drone_id in drones_by_id:
        return jsonify(drones_by_id[drone_id])
    return jsonify({"message": "Drone não encontrado"}), 404


@app.route("/users/<int:user_id>")
def user(user_id):
    if user_id in users_by_id:
        return jsonify(users_by_id[user_id])
    return jsonify({"message": "Usuário não encontrado"}), 404


@app.route("/missions")
def missions():
    return jsonify(list(missions_by_id.values()))


@app.route("/missions/<int:mission_id>")
def mission(mission_id):
    if mission_id in missions_by_id:
        return jsonify(missions_by_id[mission_id])
    return jsonify({"message": "Missão não encontrada"}), 404


if __name__ == '__main__':
    app.run(debug=True)
