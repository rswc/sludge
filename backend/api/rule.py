from flask import Blueprint, request, jsonify
import psycopg as sql
from .util import get_db, make_dicts

rule_api = Blueprint('rule_api', __name__)

@rule_api.route('/api/accessrule', methods=['GET', 'POST'])
def api_roles():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        group = request.args.get('group')

        if group:
            cur = get_db().cursor()
            cur.execute('SELECT * FROM accessrule WHERE id_group = %s', (group,))
        
        else:
            cur = get_db().cursor()
            cur.execute('SELECT * FROM accessrule')

        res = cur.fetchall()

        for rule in res:
            cur.execute(
                '''SELECT role.*
                FROM accessrule JOIN role USING(id_role)
                WHERE id_role = %s AND id_group = %s''', (rule['id_role'], rule['id_group'])
            )

            rule['role'] = cur.fetchone()

        return jsonify(res)
    
    elif request.method == 'POST':
        get_db().row_factory = make_dicts
        req_json = request.get_json()
        
        cur = get_db().cursor()

        try:
            cur.execute('''
                INSERT INTO "accessrule" 
                (id_role, id_group, policy)
                VALUES (%s, %s, %s)
                ''',
                (
                    req_json['id_role'],
                    req_json['id_group'],
                    req_json['policy']
                ))
            
            get_db().commit()
        
        except sql.errors.UniqueViolation:
            get_db().rollback()
            return {'error': 'Rule binding these two objects already exists'}, 400

        except:
            get_db().rollback()
            raise
    
        return {'id_role': req_json['id_role'], 'id_group': req_json['id_group']}, 201

@rule_api.route('/api/accessrule/<int:id_role>/<int:id_group>', methods=['GET', 'PATCH', 'DELETE'])
def api_role(id_role, id_group):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM "accessrule" WHERE id_role = %s AND id_group = %s', (id_role, id_group))

        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        return jsonify(res)
    
    elif request.method == 'PATCH':
        get_db().row_factory = make_dicts
        req_json = request.get_json()

        cur = get_db().cursor()

        # Fetch current values
        cur.execute('SELECT * FROM "accessrule" WHERE id_role = %s AND id_group = %s', (id_role, id_group))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        # Update potential new values, or leave old ones
        try:
            cur.execute('UPDATE "accessrule" SET (policy) = (%s) WHERE WHERE id_role = %s AND id_group = %s',
                (
                    req_json['policy'] if 'policy' in req_json else res['policy'],
                    id_role,
                    id_group
                ))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise
        
        # Fetch updated values
        cur.execute('SELECT * FROM "accessrule" WHERE id_role = %s AND id_group = %s', (id_role, id_group))

        return jsonify(cur.fetchone())
    
    elif request.method == 'DELETE':
        cur = get_db().cursor()

        cur.execute('SELECT * FROM "accessrule" WHERE id_role = %s AND id_group = %s', (id_role, id_group))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404
        
        try:
            cur.execute('DELETE FROM "accessrule" WHERE id_role = %s AND id_group = %s', (id_role, id_group))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise

        return {}, 200
