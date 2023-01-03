from flask import Blueprint, request, jsonify
import sqlite3 as sql
from .util import get_db, make_dicts

event_api = Blueprint('event_api', __name__)

@event_api.route('/api/event', methods=['GET', 'POST'])
def api_events():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `event`')

        res = cur.fetchall()

        for event in res:
            cur.execute(
                        '''SELECT *
                        FROM `worker`
                        WHERE id_worker = ?''', 
                        (event['id_worker'],)
                    )
            event['worker'] = cur.fetchone()

        return jsonify(res)
    
    elif request.method == 'POST':
        get_db().row_factory = make_dicts
        req_json = request.get_json()
        
        cur = get_db().cursor()

        try:
            cur.execute('''
                INSERT INTO `event` 
                (timestamp, type, id_worker, payload, id_ap, id_door)
                VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)
                ''',
                (
                    req_json['type'],
                    req_json['id_worker'],
                    req_json['payload'],
                    req_json['id_ap'],
                    req_json['id_door']
                ))
            
            get_db().commit()
        
        except sql.IntegrityError:
            get_db().rollback()
            return {'error': 'event with this name already exists'}, 400

        except:
            get_db().rollback()
            raise
    
        return {'id_event': cur.lastrowid}, 201

@event_api.route('/api/event/<int:id>', methods=['GET'])
def api_event(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM `event` WHERE id_event = ?', (id,))

        res = cur.fetchone()

        cur.execute(
                    '''SELECT *
                    FROM `worker`
                    WHERE id_worker = ?''', 
                    (res['id_worker'],)
                )
        res['worker'] = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

