from flask import Blueprint, request, jsonify
import sqlite3 as sql
from .util import get_db, make_dicts

accesspoint_api = Blueprint('accesspoint_api', __name__)

@accesspoint_api.route('/api/accesspoint', methods=['GET', 'POST'])
def api_accesspoints():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `accesspoint`')

        res = cur.fetchall()

        include = request.args.getlist('include')

        if 'groups' in include:
            for ap in res:
                cur.execute(
                        '''SELECT `Group`.*
                        FROM `Group` JOIN accesspointInGroup USING(id_group)
                        WHERE id_ap = ?''', 
                        (res['id_ap'],)
                    )

                ap['groups'] = cur.fetchall()

        return jsonify(res)
    
    elif request.method == 'POST':
        get_db().row_factory = make_dicts
        req_json = request.get_json()
        
        cur = get_db().cursor()

        if 'id_room' not in req_json:
            return {'error': 'Missing parameter: Room'}, 400

        try:
            cur.execute('''
                INSERT INTO `accesspoint` 
                (id_room, name, icon)
                VALUES (?, ?, ?)
                ''',
                (
                    req_json['id_room'],
                    req_json['name'],
                    req_json['icon']
                ))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise
    
        return {'id_ap': cur.lastrowid}, 201

@accesspoint_api.route('/api/accesspoint/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def api_accesspoint(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `accesspoint` WHERE id_ap = ?', (id,))

        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        include = request.args.getlist('include')

        if 'groups' in include:
            cur.execute(
                    '''SELECT `Group`.*
                    FROM `Group` JOIN accesspointInGroup USING(id_group)
                    WHERE id_ap = ?''', 
                    (res['id_ap'],)
                )

            res['groups'] = cur.fetchall()

        return jsonify(res)
    
    elif request.method == 'PATCH':
        get_db().row_factory = make_dicts
        req_json = request.get_json()

        cur = get_db().cursor()

        # Fetch current values
        cur.execute('SELECT * FROM `accesspoint` WHERE id_ap = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404
        
        # If request contains the 'groups' field, fetch those as well
        groups = []
        req_groups = []
        if 'groups' in req_json:
            cur.execute(
                '''SELECT id_group
                FROM accesspointInGroup
                WHERE id_ap = ?''', 
                (id,)
            )

            groups = [role['id_group'] for role in cur.fetchall()]
            req_groups = [role['id_group'] for role in req_json['groups']]

        try:
            cur.execute('UPDATE `accesspoint` SET (name, icon) = (?, ?) WHERE id_ap = ?',
                (
                    req_json['name'] if 'name' in req_json else res['name'],
                    req_json['icon'] if 'icon' in req_json else res['icon'],
                    id
                ))
            
            # Only modify groups if the request mentions them
            if 'groups' in req_json:

                # If group is assigned to accesspoint in the database, but not in the request, remove it 
                for group in groups:
                    if group not in req_groups:
                        cur.execute('DELETE FROM accesspointInGroup WHERE id_ap = ? AND id_group = ?', (id, group))
                
                # If group is not assigned to accesspoint in the database, but is in the request, add it 
                for group in req_groups:
                    if group not in groups:
                        cur.execute('INSERT INTO accesspointInGroup (id_ap, id_group) VALUES (?, ?)', (id, group))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise
        
        # Fetch updated values
        cur.execute('SELECT * FROM `accesspoint` WHERE id_ap = ?', (id,))

        return jsonify(cur.fetchone())
    
    elif request.method == 'DELETE':
        cur = get_db().cursor()

        cur.execute('SELECT * FROM `accesspoint` WHERE id_ap = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404
        
        try:
            cur.execute('DELETE FROM `accesspoint` WHERE id_ap = ?', (id,))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise

        return {}, 200
