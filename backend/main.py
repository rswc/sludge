from flask import Flask, render_template, g, request, jsonify
from flask_cors import CORS
import yaml
from api.util import get_db
from api.role import role_api
from api.worker import worker_api
from api.group import group_api
from api.resource import resource_api
from api.facility import facility_api
from api.rooms import rooms_api
from api.door import door_api
from api.accesspoint import accesspoint_api
from api.transfer import transfer_api
from api.event import event_api
from api.test import test_api
from api.rule import rule_api
from api.stats import stats_api

app = Flask(__name__)
CORS(app, resources=[r'/api/*'])

app.config.from_file('config.yaml', load=yaml.safe_load)


app.register_blueprint(role_api)
app.register_blueprint(worker_api)
app.register_blueprint(group_api)
app.register_blueprint(resource_api)
app.register_blueprint(facility_api)
app.register_blueprint(rooms_api)
app.register_blueprint(door_api)
app.register_blueprint(accesspoint_api)
app.register_blueprint(transfer_api)
app.register_blueprint(event_api)
app.register_blueprint(test_api)
app.register_blueprint(rule_api)
app.register_blueprint(stats_api)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
@app.errorhandler(404)
def home(*args, **kwargs):
    return app.send_static_file("index.html")

@app.route('/assets/<path:subpath>')
def assets(subpath):
    return app.send_static_file(f'assets/{subpath}')


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

