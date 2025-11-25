from src.db_connection import get_conn
from mysql.connector import Error

def test_database_connection():
    print("=== CONEXION ===")
    try:
        conn = get_conn()
        assert conn.is_connected(), "No se pudo conectar a la base de datos."
    finally:
        conn.close()
