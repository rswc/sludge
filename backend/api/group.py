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
            SELECT id_group, MAX(name) AS name, MAX(severity) AS severity, COUNT(id_door) AS num_doors, COUNT(id_ap) AS num_aps FROM
            (
                SELECT "Group".*, NULL AS id_door, id_ap
                FROM ("Group" LEFT JOIN accesspointingroup USING(id_group))

                UNION ALL 
                SELECT "Group".*, id_door, NULL AS id_ap FROM ("Group" LEFT JOIN dooringroup USING(id_group))
            ) q
            GROUP BY id_group
            ORDER BY name
        ''')

        res = cur.fetchall()

        return jsonify(res)
    
    elif request.method == 'POST':
        get_db().row_factory = make_dicts
        req_json = request.get_json()
        
        cur = get_db().cursor()

        try:
            cur.execute('''
                INSERT INTO "Group" 
                (id_group, name, severity)
                VALUES (NEXTVAL('group_sequence'), %s, %s)
                RETURNING *
                ''',
                (
                    req_json['name'],
                    req_json['severity']
                ))
            
            get_db().commit()
        
        except sql.errors.UniqueViolation:
            get_db().rollback()
            return {'error': 'Group with this name already exists'}, 400

        except:
            get_db().rollback()
            raise

        group = cur.fetchone()
    
        return group, 201

@group_api.route('/api/group/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def api_role(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM "Group" WHERE id_group = %s', (id,))

        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        return jsonify(res)
    
    elif request.method == 'PATCH':
        get_db().row_factory = make_dicts
        req_json = request.get_json()

        cur = get_db().cursor()

        # Fetch current values
        cur.execute('SELECT * FROM "Group" WHERE id_group = %s', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        # Update potential new values, or leave old ones
        try:
            cur.execute('UPDATE "Group" SET (name, severity) = (%s, %s) WHERE id_group = %s',
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
        cur.execute('SELECT * FROM "Group" WHERE id_group = %s', (id,))

        return jsonify(cur.fetchone())
    
    elif request.method == 'DELETE':
        cur = get_db().cursor()

        cur.execute('SELECT * FROM "Group" WHERE id_group = %s', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404
        
        try:
            cur.execute('DELETE FROM "Group" WHERE id_group = %s', (id,))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise

        return {}, 200
