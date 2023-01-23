from flask import Blueprint, request, jsonify
import sqlite3 as sql
from .util import get_db, make_dicts

stats_api = Blueprint('stats_api', __name__)

@stats_api.route('/api/stats', methods=['GET'])
def api_doors():
    if request.method == 'GET':
        get_db().row_factory = make_dicts

        cur = get_db().cursor()
        cur.execute('''
            SELECT
                w.c AS num_workers,
                r.c AS num_rooms,
                d.c AS num_doors, 
                a.c AS num_aps,
                acc_granted.c AS times_granted,
                acc_denied.c AS times_denied
            FROM 
                (SELECT COUNT(*) AS c FROM "worker") w,
                (SELECT COUNT(*) AS c FROM "room") r,
                (SELECT COUNT(*) AS c FROM "door") d,
                (SELECT COUNT(*) AS c FROM "accesspoint") a,
                (
                    SELECT COUNT(*) AS c FROM "event"
                    WHERE EXTRACT(DAY FROM (CURRENT_TIMESTAMP - timestamp)) < 1 AND type = 0
                ) acc_granted,
                (
                    SELECT COUNT(*) AS c FROM "event"
                    WHERE EXTRACT(DAY FROM (CURRENT_TIMESTAMP - timestamp)) < 1 AND type = 1
                ) acc_denied
        ''')

        res = cur.fetchone()

        return jsonify(res)
