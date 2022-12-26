from flask import Blueprint, request, jsonify
from .util import get_db, make_dicts

worker_api = Blueprint('worker_api', __name__)

@worker_api.route('/api/worker', methods=['GET', 'POST'])
def api_workers():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM worker')

        res = cur.fetchall()

        return jsonify(res)
    
    elif request.method == 'POST':
        get_db().row_factory = make_dicts
        req_json = request.get_json()
        
        cur = get_db().cursor()

        try:
            cur.execute('''
                INSERT INTO worker 
                (name, surname, date_of_birth, job_title, date_of_expiration, rolling_secret, rolling_counter, otp_secret)
                VALUES (?, ?, ?, ?, ?, 0, 0, 0)
                ''',
                (
                    req_json['name'],
                    req_json['surname'],
                    req_json['date_of_birth'],
                    req_json['job_title'],
                    req_json['date_of_expiration'],
                ))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise
    
        return {'id_worker': cur.lastrowid}, 201


@worker_api.route('/api/worker/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def api_worker(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM worker WHERE id_worker = ?', (id,))

        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        return jsonify(res)
    
    elif request.method == 'PATCH':
        get_db().row_factory = make_dicts
        req_json = request.get_json()

        cur = get_db().cursor()

        # Fetch current values
        cur.execute('SELECT * FROM worker WHERE id_worker = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        # Update potential new values, or leave old ones
        try:
            cur.execute('UPDATE worker SET (name, surname, date_of_birth, job_title, date_of_expiration) = (?, ?, ?, ?, ?) WHERE id_worker = ?',
                (
                    req_json['name'] if 'name' in req_json else res['name'],
                    req_json['surname'] if 'surname' in req_json else res['surname'],
                    req_json['date_of_birth'] if 'date_of_birth' in req_json else res['date_of_birth'],
                    req_json['job_title'] if 'job_title' in req_json else res['job_title'],
                    req_json['date_of_expiration'] if 'date_of_expiration' in req_json else res['date_of_expiration'],
                    id
                ))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise
        
        # Fetch updated values
        cur.execute('SELECT * FROM worker WHERE id_worker = ?', (id,))

        return jsonify(cur.fetchone())
    
    elif request.method == 'DELETE':
        cur = get_db().cursor()

        cur.execute('SELECT * FROM worker WHERE id_worker = ?', (id,))
        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404
        
        try:
            cur.execute('DELETE FROM worker WHERE id_worker = ?', (id,))
            
            get_db().commit()

        except:
            get_db().rollback()
            raise

        return {}, 200
