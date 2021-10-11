from flask import Flask, jsonify, request

from db.db_connect import init_connection_engine
from db.tables_init import create_tables, delete_tables
from db.db_crud import start_psql_session, upsert_contact, select_all_contact

import os

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"Status": "OK"}), 200


@app.route("/db", methods=["GET"])
def get_db():
    if init_connection_engine():
        return jsonify({
            "Status": "OK",
            "Details":
                [{
                    "Database": os.environ["DB_NAME"],
                }]
        }), 200
    else:
        return jsonify({
            "Status": "failed",
            "Details":
                [{
                    "Database": os.environ["DB_NAME"],
                }]
        }), 400


@app.route("/table", methods=["POST"])
def create_tables_():
    response = create_tables()
    if response:
        return jsonify({
            "Status": "OK",
            "Details":
                [{
                    "Contact": "created"
                }]
        }), 200
    else:
        return jsonify({
            "Status": "failed",
            "Details":
                [{
                    "Contact": "failed"
                }]
        }), 400


@app.route("/table", methods=["DELETE"])
def delete_tables_():
    response = delete_tables()
    if response:
        return jsonify({
            "Status": "OK",
            "Details":
                [{
                    "Contact": "deleted"
                }]
        }), 200
    else:
        return jsonify({
            "Status": "failed",
            "Details":
                [{
                    "Contact": "failed"
                }]
        }), 400


@app.route("/contact", methods=["POST"])
def upsert_contact_():
    # set force = False for development and testing
    # in production set force = True
    data = request.get_json(force=False)
    with start_psql_session() as session:
        response = upsert_contact(data=data, session_=session)
    response_status = response[0]
    response_count = response[1]
    if response_status and isinstance(response_status, bool):
        return jsonify({
            "Status": "OK",
            "Details":
                [{
                    "Database": os.environ["DB_NAME"],
                    "Table": "Contact",
                }],
            "Count": [response_count]
        }), 200
    if not response_status and isinstance(response_status, bool):
        return jsonify({
            "Status": "failed",
            "Details":
                [{
                    "Database": os.environ["DB_NAME"],
                    "Table": "Contact"
                }],
            "Count": None
        }), 400
    if response_status is None:
        return jsonify({
            "Status": "OK",
            "Warning": "Request body does not contain data",
            "Details":
                [{
                    "Database": os.environ["DB_NAME"],
                    "Table": "Contact"
                }],
            "Count": [response_count]
        }), 200


@app.route("/contact", methods=["GET"])
def get_contact():
    with start_psql_session() as session:
        data = select_all_contact(session_=session)
    if data:
        return jsonify({
            "Status": "OK",
            "Details":
                [{
                    "Database": os.environ["DB_NAME"],
                    "Table": "Contact",
                    "Result": data
                }],
            "Count": len(data)
        }), 200
    else:
        return jsonify({
            "Status": "OK",
            "Details":
                [{
                    "Database": os.environ["DB_NAME"],
                    "Table": "Contact",
                    "Result": []
                }],
            "Count": 0
        }), 200


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)