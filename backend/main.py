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
            cur.execute('INSERT INTO profiles (name) VALUES (?)',
                (
                    req_json['name'] if 'name' in req_json else None,
                ))
            
            if 'widgets' in req_json:
                profile_id = cur.lastrowid
                
                rows = []
                for widget in req_json['widgets']:
                    if 'media' in widget:
                        cur.execute('SELECT * FROM media WHERE (type, platform, key) = (?, ?, ?)', 
                            (
                                widget['media']['type'],
                                widget['media']['platform'],
                                widget['media']['key']
                            ))
                        res = cur.fetchone()

                        if res is None:
                            cur.execute('INSERT INTO media (type, platform, key) VALUES (?, ?, ?)',
                            (
                                widget['media']['type'],
                                widget['media']['platform'],
                                widget['media']['key']
                            ))

                            media = cur.lastrowid
                        
                        else:
                            media = res['id']
                        
                        del widget['media']
                
                    if 'added' in widget:
                        del widget['added']
                
                    if 'edited' in widget:
                        del widget['edited']
                
                    if 'id' in widget:
                        del widget['id']
                    
                    if 'template' in widget and widget['template'] == 'player' and 'keybindings' not in widget:
                        widget['keybindings'] = {'play': None}
                    
                    rows.append((str(profile_id), str(media), json.dumps(widget)))
                
                cur.executemany('INSERT INTO widgets (profile, media, options) VALUES (?, ?, ?)', rows)
            
            get_db().commit()

        except:
            get_db().rollback()
            raise
    
        return {'id': cur.lastrowid}, 201


@app.route('/api/worker/<int:id>', methods=['GET', 'POST'])
def api_worker(id):
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('SELECT * FROM worker WHERE id_worker = ?', (id,))

        res = cur.fetchone()

        if res is None:
            return {'error': 'Not found'}, 404

        return jsonify(res)

if __name__=='__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=True)

