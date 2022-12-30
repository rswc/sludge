from flask import Blueprint, request, jsonify
import sqlite3 as sql
from .util import get_db, make_dicts

rooms_api = Blueprint('rooms_api', __name__)

# Currently, you can only POST rooms to a specific facility
@rooms_api.route('/api/room', methods=['GET'])
def api_rooms():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `room`')

        res = cur.fetchall()

        return jsonify(res)

@rooms_api.route('/api/room/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def api_room(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `room` WHERE id_room = ?', (id,))

        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        return jsonify(res)
    
    elif request.method == 'PATCH':
        get_db().row_factory = make_dicts
        req_json = request.get_json()

        cur = get_db().cursor()

        # Fetch current values
        cur.execute('SELECT * FROM `room` WHERE id_room = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        # Update potential new values, or leave old ones
        try:
            cur.execute('UPDATE `room` SET name = ? WHERE id_room = ?',
                (
                    req_json['name'] if 'name' in req_json else res['name'],
                    id
                ))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise
        
        # Fetch updated values
        cur.execute('SELECT * FROM `room` WHERE id_room = ?', (id,))

        return jsonify(cur.fetchone())
    
    elif request.method == 'DELETE':
        cur = get_db().cursor()

        cur.execute('SELECT * FROM `room` WHERE id_room = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404
        
        try:
            cur.execute('DELETE FROM `room` WHERE id_room = ?', (id,))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise

        return {}, 200
