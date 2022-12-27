from flask import Blueprint, request, jsonify
import sqlite3 as sql
from .util import get_db, make_dicts

resource_api = Blueprint('resource_api', __name__)

@resource_api.route('/api/resource', methods=['GET', 'POST'])
def api_resources():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `resource`')

        res = cur.fetchall()

        return jsonify(res)
    
    elif request.method == 'POST':
        get_db().row_factory = make_dicts
        req_json = request.get_json()
        
        cur = get_db().cursor()

        try:
            cur.execute('''
                INSERT INTO `resource` 
                (name)
                VALUES (?)
                ''',
                (
                    req_json['name'],
                ))
            
            get_db().commit()
        
        except sql.IntegrityError:
            get_db().rollback()
            return {'error': 'Resource with this name already exists'}, 400

        except:
            get_db().rollback()
            raise
    
        return {'id_resource': cur.lastrowid}, 201

@resource_api.route('/api/resource/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def api_resource(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `resource` WHERE id_resource = ?', (id,))

        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        return jsonify(res)
    
    elif request.method == 'PATCH':
        get_db().row_factory = make_dicts
        req_json = request.get_json()

        cur = get_db().cursor()

        # Fetch current values
        cur.execute('SELECT * FROM `resource` WHERE id_resource = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        # Update potential new values, or leave old ones
        try:
            cur.execute('UPDATE `resource` SET name = ? WHERE id_resource = ?',
                (
                    req_json['name'] if 'name' in req_json else res['name'],
                    id
                ))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise
        
        # Fetch updated values
        cur.execute('SELECT * FROM `resource` WHERE id_resource = ?', (id,))

        return jsonify(cur.fetchone())
    
    elif request.method == 'DELETE':
        cur = get_db().cursor()

        cur.execute('SELECT * FROM `resource` WHERE id_resource = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404
        
        try:
            cur.execute('DELETE FROM `resource` WHERE id_resource = ?', (id,))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise

        return {}, 200
