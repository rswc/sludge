from flask import Blueprint, request, jsonify
import sqlite3 as sql
from .util import get_db, make_dicts

role_api = Blueprint('role_api', __name__)

@role_api.route('/api/role', methods=['GET', 'POST'])
def api_roles():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('''
            SELECT role.*, COUNT(id_worker) AS num_workers
            FROM role LEFT JOIN roleOfWorker USING(id_role) 
            GROUP BY id_role
            ORDER BY role.name
        ''')

        res = cur.fetchall()

        return jsonify(res)
    
    elif request.method == 'POST':
        get_db().row_factory = make_dicts
        req_json = request.get_json()
        
        cur = get_db().cursor()

        try:
            cur.execute('''
                INSERT INTO `role` 
                (name, color)
                VALUES (?, ?)
                ''',
                (
                    req_json['name'],
                    req_json['color']
                ))
            
            get_db().commit()
        
        except sql.IntegrityError:
            get_db().rollback()
            return {'error': 'Role with this name already exists'}, 400

        except:
            get_db().rollback()
            raise
    
        return {'id_role': cur.lastrowid}, 201

@role_api.route('/api/role/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def api_role(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `role` WHERE id_role = ?', (id,))

        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        return jsonify(res)
    
    elif request.method == 'PATCH':
        get_db().row_factory = make_dicts
        req_json = request.get_json()

        cur = get_db().cursor()

        # Fetch current values
        cur.execute('SELECT * FROM `role` WHERE id_role = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        # Update potential new values, or leave old ones
        try:
            cur.execute('UPDATE `role` SET (name, color) = (?, ?) WHERE id_role = ?',
                (
                    req_json['name'] if 'name' in req_json else res['name'],
                    req_json['color'] if 'color' in req_json else res['color'],
                    id
                ))
            
            get_db().commit()
        
        except sql.IntegrityError:
            get_db().rollback()
            return {'error': 'Role with this name already exists'}, 400

        except:
            get_db().rollback()
            raise
        
        # Fetch updated values
        cur.execute('SELECT * FROM `role` WHERE id_role = ?', (id,))

        return jsonify(cur.fetchone())
    
    elif request.method == 'DELETE':
        cur = get_db().cursor()

        cur.execute('SELECT * FROM `role` WHERE id_role = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404
        
        try:
            cur.execute('DELETE FROM `role` WHERE id_role = ?', (id,))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise

        return {}, 200
