from flask import Blueprint, request, jsonify
import sqlite3 as sql
from .util import get_db, make_dicts

facility_api = Blueprint('facility_api', __name__)

@facility_api.route('/api/facility', methods=['GET', 'POST'])
def api_facilitys():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `facility`')

        res = cur.fetchall()

        return jsonify(res)
    
    elif request.method == 'POST':
        get_db().row_factory = make_dicts
        req_json = request.get_json()
        
        cur = get_db().cursor()

        try:
            cur.execute('''
                INSERT INTO `facility` 
                (name, address)
                VALUES (?, ?)
                ''',
                (
                    req_json['name'],
                    req_json['address']
                ))
            
            get_db().commit()
        
        except sql.IntegrityError:
            get_db().rollback()
            return {'error': 'Facility with this name already exists'}, 400

        except:
            get_db().rollback()
            raise
    
        return {'id_facility': cur.lastrowid}, 201

@facility_api.route('/api/facility/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def api_facility(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `facility` WHERE id_facility = ?', (id,))

        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        return jsonify(res)
    
    elif request.method == 'PATCH':
        get_db().row_factory = make_dicts
        req_json = request.get_json()

        cur = get_db().cursor()

        # Fetch current values
        cur.execute('SELECT * FROM `facility` WHERE id_facility = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        # Update potential new values, or leave old ones
        try:
            cur.execute('UPDATE `facility` SET (name, address) = (?, ?) WHERE id_facility = ?',
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
        cur.execute('SELECT * FROM `facility` WHERE id_facility = ?', (id,))

        return jsonify(cur.fetchone())
    
    elif request.method == 'DELETE':
        cur = get_db().cursor()

        cur.execute('SELECT * FROM `facility` WHERE id_facility = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404
        
        try:
            cur.execute('DELETE FROM `facility` WHERE id_facility = ?', (id,))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise

        return {}, 200
