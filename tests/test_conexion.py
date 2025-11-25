from src.db_connection import get_conn
from mysql.connector import Error

def test_database_connection():
    try:
        conn = get_conn()
        assert conn.is_connected(), "No se pudo conectar a la db :c."
    except Error as e:
        assert False, f"Error al conectar: {e}"
    finally:
        try:
            conn.close()
        except:
            pass
