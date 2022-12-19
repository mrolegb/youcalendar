import sqlite3
from datetime import datetime
from flask import jsonify
from flask.wrappers import Response
from typing import Any, List


def get_formatted_date(date: datetime):
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")


def create_connection(path: str) -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect(path)
        return conn
    except sqlite3.Error as e:
        raise e


def execute(conn: sqlite3.Connection, sql: str) -> List[Any]:
    try:
        c = conn.cursor()
        return c.execute(sql).fetchall()
    except sqlite3.Error as e:
        raise e


def get_response(status: str, msg: str | dict | List[dict]) -> Response:
    return jsonify(
        {
            "status": status,
            "message": msg,
        }
    )
