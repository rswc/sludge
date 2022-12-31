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

        include = request.args.getlist('include')

        if 'groups' in include:
            cur.execute(
                    '''SELECT `Group`.name, `Group`.severity
                    FROM `Group` JOIN doorInGroup USING(id_group)
                    WHERE id_door = ?''', 
                    (res['id_door'],)
                )

            res['groups'] = cur.fetchall()

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
        
        # If request contains the 'groups' field, fetch those as well
        groups = []
        req_groups = []
        if 'groups' in req_json:
            cur.execute(
                '''SELECT id_group
                FROM doorInGroup
                WHERE id_door = ?''', 
                (id,)
            )

            groups = [role['id_group'] for role in cur.fetchall()]
            req_groups = [role['id_group'] for role in req_json['groups']]

        try:
            # You can't modify a door's source or destination
            # Just make a new door 4head
            
            # Only modify groups if the request mentions them
            if 'groups' in req_json:

                # If group is assigned to door in the database, but not in the request, remove it 
                for group in groups:
                    if group not in req_groups:
                        cur.execute('DELETE FROM doorInGroup WHERE id_door = ? AND id_group = ?', (id, group))
                
                # If group is not assigned to door in the database, but is in the request, add it 
                for group in req_groups:
                    if group not in groups:
                        cur.execute('INSERT INTO doorInGroup (id_door, id_group) VALUES (?, ?)', (id, group))
            
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
