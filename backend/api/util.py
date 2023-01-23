import psycopg as sql
from flask import g, current_app

from typing import Any, Sequence
from psycopg import Cursor

def make_dicts(cursor: Cursor[Any]):
    fields = [c.name for c in cursor.description]

    def make_row(values: Sequence[Any]) -> "dict[str, Any]":
        return dict(zip(fields, values))

    return make_row

def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sql.connect(
            dbname = current_app.config['DB_NAME'],
            host = current_app.config['DB_HOST'],
            user = current_app.config['DB_USER'],
            password = current_app.config['DB_PASS'],
            port = current_app.config['DB_PORT'],
        )
    
    return db
