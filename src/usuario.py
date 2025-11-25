from src.db_connection import get_conn
import hashlib

def hash_password(password: str):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

class Usuario:
    def __init__(self, id_, nombre, tipo, password_hash=None):
        self.id = id_
        self.nombre = nombre
        self.tipo = tipo  # "usuario" , "artista" o "admin"
        self.password_hash = password_hash

    @classmethod
    def crear(cls, nombre, password, tipo="usuario"):
        conn = get_conn()
        try:
            cur = conn.cursor()
            pwd_hash = hash_password(password)
            cur.execute(
                "INSERT INTO users (username, user_type, password) VALUES (%s, %s, %s)",
                (nombre, tipo, pwd_hash)
            )
            conn.commit()
            return cls(cur.lastrowid, nombre, tipo)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def autenticar(cls, nombre, password):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, username, user_type, password FROM users WHERE username = %s",
                (nombre,)
            )
            r = cur.fetchone()
            if not r:
                return None
            if hash_password(password) == r[3]:
                return cls(r[0], r[1], r[2], r[3])
            return None
        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_todos(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, username, user_type FROM users")
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2]) for r in rows]
        finally:
            cur.close()
            conn.close()


    @classmethod
    def buscar_por_id(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, username, user_type FROM users WHERE id=%s", (id_,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2]) if r else None
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

    @classmethod
    def buscar_por_username(cls, username):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, username, user_type FROM users WHERE username=%s", (username,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2]) if r else None
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

'''
# Falta:
- agregar a favorites
'''