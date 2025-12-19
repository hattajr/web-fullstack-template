import psycopg2
from core.config import settings


def get_connection():
    host = settings.db_host
    port = settings.db_port
    username = settings.db_username
    password = settings.db_password
    database = settings.db_name
    return psycopg2.connect(
        f"host={host} dbname={database} user={username} password={password} port={port}"
    )
