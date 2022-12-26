import json
import sqlite3 as sql
from flask import Flask, render_template, g, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources=[r'/api/*'])

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def parse_widget(widget: dict, media):
    widget.update(json.loads(widget['options']))
    del widget['options']
    
    if media is not None and media['id'] is not None:
        widget['media'] = media

    return widget

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect('database.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def home():
    return app.send_static_file("index.html")

@app.route('/assets/<path:subpath>')
def assets(subpath):
    return app.send_static_file(f'assets/{subpath}')


@app.route('/api/worker', methods=['GET', 'POST'])
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


@app.route('/api/worker/<int:id>', methods=['GET', 'PATCH'])
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

if __name__=='__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=True)

