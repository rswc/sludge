from flask import Blueprint, request, jsonify
import sqlite3 as sql
from .util import get_db, make_dicts

group_api = Blueprint('group_api', __name__)

@group_api.route('/api/group', methods=['GET', 'POST'])
def api_roles():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('''
            SELECT id_group, name, severity, COUNT(id_door) AS num_doors, COUNT(id_ap) AS num_aps FROM (
            SELECT `group`.*, NULL AS id_door, id_ap
            FROM `Group` JOIN accesspointingroup USING(id_group)
            UNION ALL 
            SELECT `group`.*, id_door, NULL AS id_ap FROM `Group` JOIN dooringroup USING(id_group))
            GROUP BY id_group
        ''')

        res = cur.fetchall()

        return jsonify(res)
    
    elif request.method == 'POST':
        get_db().row_factory = make_dicts
        req_json = request.get_json()
        
        cur = get_db().cursor()

        try:
            cur.execute('''
                INSERT INTO `group` 
                (name, severity)
                VALUES (?, ?)
                ''',
                (
                    req_json['name'],
                    req_json['severity']
                ))
            
            get_db().commit()
        
        except sql.IntegrityError:
            get_db().rollback()
            return {'error': 'Group with this name already exists'}, 400

        except:
            get_db().rollback()
            raise
    
        return {'id_group': cur.lastrowid}, 201

@group_api.route('/api/group/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def api_role(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `group` WHERE id_group = ?', (id,))

        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        return jsonify(res)
    
    elif request.method == 'PATCH':
        get_db().row_factory = make_dicts
        req_json = request.get_json()

        cur = get_db().cursor()

        # Fetch current values
        cur.execute('SELECT * FROM `group` WHERE id_group = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        # Update potential new values, or leave old ones
        try:
            cur.execute('UPDATE `group` SET (name, severity) = (?, ?) WHERE id_group = ?',
                (
                    req_json['name'] if 'name' in req_json else res['name'],
                    req_json['severity'] if 'severity' in req_json else res['severity'],
                    id
                ))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise
        
        # Fetch updated values
        cur.execute('SELECT * FROM `group` WHERE id_group = ?', (id,))

        return jsonify(cur.fetchone())
    
    elif request.method == 'DELETE':
        cur = get_db().cursor()

        cur.execute('SELECT * FROM `group` WHERE id_group = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404
        
        try:
            cur.execute('DELETE FROM `group` WHERE id_group = ?', (id,))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise

        return {}, 200
