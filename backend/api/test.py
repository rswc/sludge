from flask import Blueprint, request, jsonify
import sqlite3 as sql
from .util import get_db, make_dicts
import random

test_api = Blueprint('test_api', __name__)

@test_api.route('/api/test/door', methods=['POST'])
def api_test_door():
    req_json = request.get_json()

    if random.random() > 0.5:
        return {'granted': True}, 200
    
    else:
        return {'granted': False}, 200

@test_api.route('/api/test/accesspoint', methods=['POST'])
def api_test_ap():
    req_json = request.get_json()

    if random.random() > 0.5:
        return {'granted': True}, 200
    
    else:
        return {'granted': False}, 200