from flask import Blueprint, request, jsonify
import sqlite3 as sql
from .util import get_db, make_dicts

transfer_api = Blueprint('transfer_api', __name__)

@transfer_api.route('/api/transfer', methods=['GET', 'POST', 'DELETE'])
def api_transfers():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `transfer`')

        res = cur.fetchall()

        for transfer in res:
            cur.execute(
                        '''SELECT *
                        FROM `worker`
                        WHERE id_worker = ?''', 
                        (transfer['id_worker'],)
                    )
            transfer['worker'] = cur.fetchone()
            
            cur.execute(
                        '''SELECT *
                        FROM `resource`
                        WHERE id_resource = ?''', 
                        (transfer['id_resource'],)
                    )
            transfer['resource'] = cur.fetchone()
            
            cur.execute(
                        '''SELECT *
                        FROM `facility`
                        WHERE id_facility = ?''', 
                        (transfer['id_facility_src'],)
                    )
            transfer['facility_src'] = cur.fetchone()
            
            cur.execute(
                        '''SELECT *
                        FROM `facility`
                        WHERE id_facility = ?''', 
                        (transfer['id_facility_dst'],)
                    )
            transfer['facility_dst'] = cur.fetchone()

        return jsonify(res)
    
    elif request.method == 'POST':
        get_db().row_factory = make_dicts
        req_json = request.get_json()
        
        cur = get_db().cursor()

        try:
            cur.execute('''
                INSERT INTO `transfer` 
                (timestamp, id_resource, id_worker, amount, id_facility_src, id_facility_dst)
                VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)
                ''',
                (
                    req_json['id_resource'],
                    req_json['id_worker'],
                    req_json['amount'],
                    req_json['id_facility_src'],
                    req_json['id_facility_dst']
                ))
            
            get_db().commit()
        
        except sql.IntegrityError:
            get_db().rollback()
            return {'error': 'Transfer with these parameters already exists'}, 400

        except:
            get_db().rollback()
            raise
    
        return {'id_transfer': cur.lastrowid}, 201
    
    elif request.method == 'DELETE':
        cur = get_db().cursor()
        cur.execute('DELETE FROM `transfer`') # SQLite has no TRUNCATE
        get_db().commit()

        return {}, 200

@transfer_api.route('/api/transfer/<int:id>', methods=['GET'])
def api_transfer(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `transfer` WHERE id_transfer = ?', (id,))

        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        cur.execute(
                    '''SELECT *
                    FROM `worker`
                    WHERE id_worker = ?''', 
                    (res['id_worker'],)
                )
        res['worker'] = cur.fetchone()
        
        cur.execute(
                    '''SELECT *
                    FROM `resource`
                    WHERE id_resource = ?''', 
                    (res['id_resource'],)
                )
        res['resource'] = cur.fetchone()
        
        cur.execute(
                    '''SELECT *
                    FROM `facility`
                    WHERE id_facility = ?''', 
                    (res['id_facility_src'],)
                )
        res['facility_src'] = cur.fetchone()
        
        cur.execute(
                    '''SELECT *
                    FROM `facility`
                    WHERE id_facility = ?''', 
                    (res['id_facility_dst'],)
                )
        res['facility_dst'] = cur.fetchone()

        return jsonify(res)
