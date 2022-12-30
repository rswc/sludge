from flask import Blueprint, request, jsonify
import sqlite3 as sql
from .util import get_db, make_dicts

door_api = Blueprint('door_api', __name__)

@door_api.route('/api/door', methods=['GET', 'POST'])
def api_doors():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `door`')

        res = cur.fetchall()

        return jsonify(res)
    
    elif request.method == 'POST':
        get_db().row_factory = make_dicts
        req_json = request.get_json()
        
        cur = get_db().cursor()

        if 'id_room_src' not in req_json:
            return {'error': 'Missing parameter: source room'}, 400
        if 'id_room_dst' not in req_json:
            return {'error': 'Missing parameter: destination room'}, 400

        try:
            cur.execute('''
                INSERT INTO `door` 
                (id_room_src, id_room_dst)
                VALUES (?, ?)
                ''',
                (
                    req_json['id_room_src'],
                    req_json['id_room_dst']
                ))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise
    
        return {'id_door': cur.lastrowid}, 201

@door_api.route('/api/door/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def api_door(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `door` WHERE id_door = ?', (id,))

        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        return jsonify(res)
    
    elif request.method == 'PATCH':
        get_db().row_factory = make_dicts
        req_json = request.get_json()

        cur = get_db().cursor()

        # Fetch current values
        cur.execute('SELECT * FROM `door` WHERE id_door = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        # Update potential new values, or leave old ones
        try:
            cur.execute('UPDATE `door` SET (name, address) = (?, ?) WHERE id_door = ?',
                (
                    req_json['name'] if 'name' in req_json else res['name'],
                    req_json['address'] if 'address' in req_json else res['address'],
                    id
                ))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise
        
        # Fetch updated values
        cur.execute('SELECT * FROM `door` WHERE id_door = ?', (id,))

        return jsonify(cur.fetchone())
    
    elif request.method == 'DELETE':
        cur = get_db().cursor()

        cur.execute('SELECT * FROM `door` WHERE id_door = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404
        
        try:
            cur.execute('DELETE FROM `door` WHERE id_door = ?', (id,))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise

        return {}, 200
