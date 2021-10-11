import logging
import os

import sqlalchemy
from flask import Flask


app = Flask(__name__)

logger = logging.getLogger()


def init_connection_engine():
    db_config = {
        "pool_size": 5,
        "max_overflow": 2,
        "pool_timeout": 30,
        "pool_recycle": 1800,
    }

    if os.environ.get("DB_HOST"):
        return init_tcp_connection_engine(db_config)
    else:
        return init_unix_connection_engine(db_config)


def init_tcp_connection_engine(db_config):
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]
    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgresql+psycopg2://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+psycopg2",
            username=db_user,
            password=db_pass,
            host=db_hostname,
            port=db_port,
            database=db_name
        ),
        **db_config
    )
    pool.dialect.description_encoding = None
    return pool


def init_unix_connection_engine(db_config):
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgresql+psycopg2://<db_user>:<db_pass>@/<db_name>
        #                         ?unix_sock=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+psycopg2",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={
                "host": "{}/{}".format(
                    db_socket_dir,
                    cloud_sql_connection_name)
            }
        ),
        **db_config
    )
    pool.dialect.description_encoding = None
    return pool
