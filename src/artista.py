from src.db_connection import get_conn
from src.usuario import Usuario, hash_password

class Artista(Usuario):
    def __init__(self, id_, nombre, tipo, password_hash=None, bio=None, followers=0):
        super().__init__(id_, nombre, tipo, password_hash)
        self.bio = bio
        self.followers = followers

    @classmethod
    def crear(cls, nombre, password, tipo="artista", bio=""):
        conn = get_conn()
        try:
            cur = conn.cursor()

            pwd_hash = hash_password(password)
            cur.execute(
                "INSERT INTO users (username, user_type, password) VALUES (%s, %s, %s)",
                (nombre, tipo, pwd_hash)
            )
            user_id = cur.lastrowid

            cur.execute(
                "INSERT INTO artists (id, bio) VALUES (%s, %s)",
                (user_id, bio)
            )

            conn.commit()
            return cls(user_id, nombre, tipo, pwd_hash, bio, 0)
        finally:
            cur.close()
            conn.close()


    @classmethod
    def listar_todos(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT u.id, u.username, u.user_type, a.bio, a.followers
                FROM users u
                JOIN artists a ON u.id = a.id
            """)
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4]) for r in rows]
        finally:
            cur.close()
            conn.close()


    @classmethod
    def buscar_por_id(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT u.id, u.username, u.user_type, a.bio, a.followers
                FROM users u
                JOIN artists a ON u.id = a.id
                WHERE u.id=%s
            """, (id_,))
            r = cur.fetchone()

            if not r:
                return None

            return cls(r[0], r[1], r[2], r[3], r[4])
        finally:
            cur.close()
            conn.close()


    @classmethod
    def buscar_por_username(cls, username):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT u.id, u.username, u.user_type, a.bio, a.followers
                FROM users u
                JOIN artists a ON u.id = a.id
                WHERE u.username=%s
            """, (username,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3], r[4] if r else None)
        finally:
            cur.close()
            conn.close()
    
'''
# Cosas que va a hacer artista:
- crear un track
- crear un tracklist
- listar_followers
'''