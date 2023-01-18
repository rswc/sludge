from flask import Blueprint, request, jsonify
from .util import get_db, make_dicts

worker_api = Blueprint('worker_api', __name__)

@worker_api.route('/api/worker', methods=['GET', 'POST'])
def api_workers():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        roles_filter = request.args.getlist('role')

        cur = get_db().cursor()

        if roles_filter:
            cur.execute(
                f'''SELECT DISTINCT worker.* FROM worker JOIN roleOfWorker USING(id_worker) 
                WHERE id_role IN ({','.join(['?'] * len(roles_filter))}) AND LOWER(name) LIKE ? 
                AND LOWER(surname) LIKE ? AND LOWER(job_title) LIKE ?''',
                (
                    *roles_filter,
                    f"%{request.args.get('name', '')}%",
                    f"%{request.args.get('surname', '')}%",
                    f"%{request.args.get('job_title', '')}%",
                )
            )

        else:
            cur.execute(
                '''SELECT * FROM worker WHERE LOWER(name) LIKE ? AND LOWER(surname) LIKE ?
                AND LOWER(job_title) LIKE ?''',
                (
                    f"%{request.args.get('name', '')}%",
                    f"%{request.args.get('surname', '')}%",
                    f"%{request.args.get('job_title', '')}%",
                )
            )

        res = cur.fetchall()

        for worker in res:
            cur.execute(
                '''SELECT role.id_role AS id_role, role.name AS name, role.color AS color
                FROM worker JOIN roleOfWorker USING(id_worker) JOIN role USING(id_role)
                WHERE id_worker = ?''', 
                (worker['id_worker'],)
            )

            worker['roles'] = cur.fetchall()

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

            worker_id = cur.lastrowid

        except:
            get_db().rollback()
            raise

        if 'roles' in req_json:
            try:
                for role in req_json['roles']:
                    cur.execute('INSERT INTO roleOfWorker (id_worker, id_role) VALUES (?, ?)', (worker_id, role['id_role']))
                
                get_db().commit()

            except:
                get_db().rollback()
                raise
    
        return {'id_worker': worker_id}, 201


@worker_api.route('/api/worker/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def api_worker(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM worker WHERE id_worker = ?', (id,))

        res = cur.fetchone()

        cur.execute(
            '''SELECT role.id_role AS id_role, role.name AS name, role.color AS color
            FROM worker JOIN roleOfWorker USING(id_worker) JOIN role USING(id_role)
            WHERE id_worker = ?''', 
            (id,)
        )

        res['roles'] = cur.fetchall()

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
        
        # If request contains the 'roles' field, fetch those as well
        roles = []
        req_roles = []
        if 'roles' in req_json:
            cur.execute(
                '''SELECT id_role
                FROM roleOfWorker 
                WHERE id_worker = ?''', 
                (id,)
            )

            roles = [role['id_role'] for role in cur.fetchall()]
            req_roles = [role['id_role'] for role in req_json['roles']]

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
            
            # Only modify roles if the request mentions them
            if 'roles' in req_json:

                # If role is assigned to worker in the database, but not in the request, remove it 
                for role in roles:
                    if role not in req_roles:
                        cur.execute('DELETE FROM roleOfWorker WHERE id_worker = ? AND id_role = ?', (id, role))
                
                # If role is not assigned to worker in the database, but is in the request, add it 
                for role in req_roles:
                    if role not in roles:
                        cur.execute('INSERT INTO roleOfWorker (id_worker, id_role) VALUES  (?, ?)', (id, role))
            
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

@worker_api.route('/api/worker/<int:id>/stats', methods=['GET', 'PATCH', 'DELETE'])
def api_worker_stats(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        res = {'id_worker': id}

        cur = get_db().cursor()        

        cur.execute('SELECT COUNT(*) AS num_events FROM event WHERE id_worker = ?', (id,))
        res['num_events'] = cur.fetchone()['num_events']

        cur.execute('SELECT COUNT(*) AS num_transfers FROM transfer WHERE id_worker = ?', (id,))
        res['num_transfers'] = cur.fetchone()['num_transfers']

        if res is None:
            return {'error': 'Not found'}, 404

        return jsonify(res)
