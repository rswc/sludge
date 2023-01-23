from flask import Blueprint, request, jsonify
from .util import get_db, make_dicts

test_api = Blueprint('test_api', __name__)

@test_api.route('/api/test/door', methods=['POST'])
def api_test_door():
    req_json = request.get_json()

    if 'id_worker' not in req_json or 'id_door' not in req_json:
        return 'Missing parameter: id_worker', 400

    if 'id_door' not in req_json:
        return 'Missing parameter: id_door', 400

    cur = get_db().cursor()
    cur.execute(
        'SELECT HasDoorAccess(%s, %s) AS access',
        (req_json['id_worker'], req_json['id_door'])
    )

    res = cur.fetchone()

    return {'granted': bool(res[0])}, 200

@test_api.route('/api/test/accesspoint', methods=['POST'])
def api_test_ap():
    req_json = request.get_json()

    if 'id_worker' not in req_json or 'id_ap' not in req_json:
        return 'Missing parameter: id_worker', 400

    if 'id_ap' not in req_json:
        return 'Missing parameter: id_ap', 400

    cur = get_db().cursor()
    cur.execute(
        'SELECT HasAPAccess(%s, %s) AS access',
        (req_json['id_worker'], req_json['id_ap'])
    )

    res = cur.fetchone()

    return {'granted': bool(res[0])}, 200