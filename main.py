import json
from flask import Flask, jsonify, request

app = Flask(__name__)

modders = [
    {'rid': 1, 'name': 'Joey', 'modmenu': 'Stand'}
]

nextModderRid = 2


@app.route('/modders', methods=['GET'])
def get_modders():
    # Fetch query parameters
    rid_query = request.args.get('rid')
    name_query = request.args.get('name')
    modmenu_query = request.args.get('modmenu')

    # Filter modders based on query parameters
    filtered_modders = modders

    if rid_query:
        try:
            rid_query = int(rid_query)
            filtered_modders = [m for m in modders if m['rid'] == rid_query]
        except ValueError:
            return jsonify({'error': 'Invalid rid format. It should be an integer.'}), 400

    if name_query:
        filtered_modders = [m for m in filtered_modders if name_query.lower() in m['name'].lower()]

    if modmenu_query:
        filtered_modders = [m for m in filtered_modders if modmenu_query.lower() in m['modmenu'].lower()]

    return jsonify(filtered_modders)


@app.route('/modders/<int:rid>', methods=['GET'])
def get_modder_by_rid(rid: int):
    modder = get_modder(rid)
    if modder is None:
        return jsonify({'error': 'Modder does not exist'}), 404
    return jsonify(modder)


def get_modder(rid):
    return next((m for m in modders if m['rid'] == rid), None)


def modder_is_valid(modder):
    # Ensure 'name' is a non-empty string and 'modmenu' is a string (it can be empty)
    if 'name' in modder and isinstance(modder['name'], str) and modder['name'].strip() and 'modmenu' in modder and isinstance(modder['modmenu'], str):
        return True
    return False


@app.route('/modders', methods=['POST'])
def create_modder():
    global nextModderRid
    try:
        modder = json.loads(request.data)
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format.'}), 400

    if not modder_is_valid(modder):
        return jsonify({'error': 'Invalid modder properties.'}), 400

    modder['rid'] = nextModderRid
    nextModderRid += 1
    modders.append(modder)

    return jsonify(modder), 201, {'location': f'/modders/{modder["rid"]}'}


@app.route('/modders/<int:rid>', methods=['PUT'])
def update_modder(rid: int):
    modder = get_modder(rid)
    if modder is None:
        return jsonify({'error': 'Modder does not exist.'}), 404

    try:
        updated_modder = json.loads(request.data)
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format.'}), 400

    if not modder_is_valid(updated_modder):
        return jsonify({'error': 'Invalid modder properties.'}), 400

    modder.update(updated_modder)
    return jsonify(modder)


@app.route('/modders/<int:rid>', methods=['DELETE'])
def delete_modder(rid: int):
    global modders
    modder = get_modder(rid)
    if modder is None:
        return jsonify({'error': 'Modder does not exist.'}), 404

    modders = [m for m in modders if m['rid'] != rid]
    return jsonify({'message': 'Modder deleted successfully'}), 200


if __name__ == '__main__':
    app.run(port=5500)
