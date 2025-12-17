import os
import psycopg2 
from core.config import settings

def get_connection():
    host = settings.DB_HOST
    port = settings.DB_PORT
    username = settings.DB_USERNAME
    password = settings.DB_PASSWORD
    database = settings.DB_NAME
    return psycopg2.connect(f"host={host} dbname={database} user={username} password={password} port={port}")