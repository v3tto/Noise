import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    "port": int(os.getenv('DB_PORT', 3306)),
    'database': os.getenv('DB_NAME', 'noise_db'),
    "user": os.getenv('DB_USER', 'root'),
    "password": os.getenv('DB_PASSWORD', ''),
    "autocommit": False,
    "charset": "utf8mb4",
}

POOL_NAME = os.getenv('DB_POOL_NAME', 'bip_pool')
POOL_SIZE = int(os.getenv('DB_POOL_SIZE', 5))

pool = pooling.MySQLConnectionPool(
    pool_name=POOL_NAME,
    pool_size=POOL_SIZE,
    **DB_CONFIG
)

def get_conn():
    return pool.get_connection()
