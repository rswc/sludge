from flask import Blueprint, request, jsonify
import psycopg as sql
from .util import get_db, make_dicts

resource_api = Blueprint('resource_api', __name__)

@resource_api.route('/api/resource', methods=['GET', 'POST'])
def api_resources():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM "Resource"')

        res = cur.fetchall()

        return jsonify(res)
    
    elif request.method == 'POST':
        get_db().row_factory = make_dicts
        req_json = request.get_json()
        
        cur = get_db().cursor()

        try:
            cur.execute('''
                INSERT INTO "Resource" 
                (id_resource, name)
                VALUES (NEXTVAL('resource_sequence'), %s)
                RETURNING *
                ''',
                (
                    req_json['name'],
                ))
            
            get_db().commit()
        
        except sql.errors.UniqueViolation:
            get_db().rollback()
            return {'error': 'Resource with this name already exists'}, 400

        except:
            get_db().rollback()
            raise
    
        resource = cur.fetchone()
    
        return resource, 201

@resource_api.route('/api/resource/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def api_resource(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM "Resource" WHERE id_resource = %s', (id,))

        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        return jsonify(res)
    
    elif request.method == 'PATCH':
        get_db().row_factory = make_dicts
        req_json = request.get_json()

        cur = get_db().cursor()

        # Fetch current values
        cur.execute('SELECT * FROM "Resource" WHERE id_resource = %s', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        # Update potential new values, or leave old ones
        try:
            cur.execute('UPDATE "Resource" SET name = %s WHERE id_resource = %s',
                (
                    req_json['name'] if 'name' in req_json else res['name'],
                    id
                ))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise
        
        # Fetch updated values
        cur.execute('SELECT * FROM "Resource" WHERE id_resource = %s', (id,))

        return jsonify(cur.fetchone())
    
    elif request.method == 'DELETE':
        cur = get_db().cursor()

        cur.execute('SELECT * FROM "Resource" WHERE id_resource = %s', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404
        
        try:
            cur.execute('DELETE FROM "Resource" WHERE id_resource = %s', (id,))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise

        return {}, 200
