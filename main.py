import json
from flask import Flask, jsonify
from flask_cors import CORS
import logging
import os

root_dir = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join(root_dir, 'app.log'),
)

app = Flask(__name__)
CORS(app)


def load_data(entity_name):
    """Carrega os dados de um arquivo JSON na pasta 'data'."""
    try:
        entity_dir = os.path.join(root_dir, f'data/{entity_name}.json')
        logger.info(f"Carregando dados de {entity_dir}")
        with open(entity_dir, 'r') as f:
            data = json.load(f)
        return {item['id']: item for item in data}
    except FileNotFoundError:
        logger.error(
            f"Erro: Arquivo data/{entity_name}.json não encontrado."
        )
        return {}
    except json.JSONDecodeError:
        logger.error(
            f"Erro: Arquivo data/{entity_name}.json não é um JSON válido."
        )
        return {}


cages_by_id = load_data('cage')
drones_by_id = load_data('drone')
users_by_id = load_data('user')
missions_by_id = load_data('mission')


@app.route("/")
def hello_world():
    return 'its working'


@app.route("/logs")
def logs():
    log_file = os.path.join(root_dir, './app.log')
    if not os.path.exists(log_file):
        logger.error("Log file not found")
        return jsonify({"error": "Log file not found"}), 404

    with open(log_file, 'r') as f:
        logs = f.readlines()
    logs = [log.strip() for log in logs]
    logs_str = "<br>".join(logs)
    return logs_str, 200, {'Content-Type': 'text/html'}


@app.route("/cages")
def cages():
    logger.info("Cages endpoint called")
    return jsonify(list(cages_by_id.values()))


@app.route("/cages/<int:cage_id>", methods=["GET"])
def cage(cage_id):
    if cage_id in cages_by_id:
        logger.info(f"Cage {cage_id} found")
        return jsonify(cages_by_id[cage_id])
    logger.warning(f"Cage {cage_id} not found")
    return jsonify({"message": "Gaiola não encontrada"}), 404


@app.route("/drones")
def drones():
    logger.info("Drones endpoint called")
    return jsonify(list(drones_by_id.values()))


@app.route("/drones/<int:drone_id>")
def drone(drone_id):
    if drone_id in drones_by_id:
        logger.info(f"Drone {drone_id} found")
        return jsonify(drones_by_id[drone_id])
    logger.warning(f"Drone {drone_id} not found")
    return jsonify({"message": "Drone não encontrado"}), 404


@app.route("/users/<int:user_id>")
def user(user_id):
    if user_id in users_by_id:
        logger.info(f"User {user_id} found")
        return jsonify(users_by_id[user_id])
    logger.warning(f"User {user_id} not found")
    return jsonify({"message": "Usuário não encontrado"}), 404


@app.route("/missions")
def missions():
    logger.info("Missions endpoint called")
    return jsonify(list(missions_by_id.values()))


@app.route("/missions/<int:mission_id>")
def mission(mission_id):
    if mission_id in missions_by_id:
        logger.info(f"Mission {mission_id} found")
        return jsonify(missions_by_id[mission_id])
    logger.warning(f"Mission {mission_id} not found")
    return jsonify({"message": "Missão não encontrada"}), 404


if __name__ == '__main__':
    app.run(debug=True)
