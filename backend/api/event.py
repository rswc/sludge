from flask import Blueprint, request, jsonify
import sqlite3 as sql
from .util import get_db, make_dicts

event_api = Blueprint('event_api', __name__)

@event_api.route('/api/event', methods=['GET', 'POST'])
def api_events():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        limit = request.args.get('limit', type=int)

        cur = get_db().cursor()
        cur.execute(f'''
            SELECT "event".* FROM "event" JOIN worker USING(id_worker)
            WHERE (worker.name LIKE %s OR worker.surname LIKE %s)
            AND (event.type = %s OR CAST(%s AS INTEGER) IS NULL)
            ORDER BY timestamp DESC
            { f'LIMIT {limit}' if limit else '' }
        ''', (
            f"%{request.args.get('employee', '')}%",
            f"%{request.args.get('employee', '')}%",
            request.args.get('type', None),
            request.args.get('type', None),
        ))

        res = cur.fetchall()

        for event in res:
            cur.execute(
                        '''SELECT *
                        FROM "worker"
                        WHERE id_worker = %s''', 
                        (event['id_worker'],)
                    )
            event['worker'] = cur.fetchone()

            if event['id_door'] is not None:
                cur.execute(
                    '''SELECT door.*, src.name AS src_name, dst.name AS dst_name
                    FROM door JOIN room src ON door.id_room_src = src.id_room JOIN room dst ON door.id_room_dst = dst.id_room
                    WHERE id_door = %s''', 
                    (event['id_door'],)
                )

                event['door'] = cur.fetchone()
            
            elif event['id_ap'] is not None:
                cur.execute(
                    '''SELECT *
                    FROM "accesspoint"
                    WHERE id_ap = %s''', 
                    (event['id_ap'],)
                )

                event['ap'] = cur.fetchone()

        return jsonify(res)
    
    elif request.method == 'POST':
        get_db().row_factory = make_dicts
        req_json = request.get_json()
        
        cur = get_db().cursor()

        try:
            cur.execute('''
                INSERT INTO "event" 
                (timestamp, type, id_worker, payload, id_ap, id_door)
                VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s, %s)
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
        cur.execute('SELECT * FROM "event" WHERE id_event = %s', (id,))

        res = cur.fetchone()

        cur.execute(
                    '''SELECT *
                    FROM "worker"
                    WHERE id_worker = %s''', 
                    (res['id_worker'],)
                )
        res['worker'] = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

