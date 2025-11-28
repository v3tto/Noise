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
            cur.execute("""
                SELECT id, username, user_type, password
                FROM users
                WHERE username = %s
            """, (nombre,))
            
            r = cur.fetchone()
            if not r:
                return None

            stored_hash = r[3]
            if hash_password(password) != stored_hash:
                return None

            user_id, username, tipo, _ = r

            # Para evitar import circular
            from src.artista import Artista
            from src.admin import Admin
            # esta puede ser la peor funcion que he programado
            # pero funciona

            if tipo == "usuario":
                return Usuario(user_id, username, tipo, stored_hash)
            elif tipo == "artista":
                cur.execute("SELECT bio, followers FROM artists WHERE id=%s", (user_id,))
                a = cur.fetchone()
                bio = a[0] if a else ""
                followers = a[1] if a else 0
                return Artista(user_id, username, tipo, stored_hash, bio, followers)
            elif tipo == "admin":
                return Admin(user_id, username, tipo, stored_hash)
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
    
    def crear_tracklist(self, titulo):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO tracklists (title, user_id, tracklist_type)
                VALUES (%s, %s, 'playlist')
            """, (titulo, self.id))
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            print("Error al crear playlist:", e)
            return None
        finally:
            cur.close()
            conn.close()
    
    def eliminar_tracklist(self, tracklist_id):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id FROM tracklists 
                WHERE id = %s AND user_id = %s
            """, (tracklist_id, self.id))
            
            row = cur.fetchone()
            if not row:
                print("No tienes permiso para eliminar esta tracklist.")
                return False
            
            cur.execute("""
                DELETE FROM tracklists WHERE id = %s
            """, (tracklist_id,))
            conn.commit()

            print("Tracklist eliminada correctamente.")
            return True

        except Exception as e:
            print("Error al eliminar tracklist:", e)
            return False

        finally:
            cur.close()
            conn.close()

'''
# Falta:
- agregar a favorites
- un hijo admin que pueda borrar cualquier tracklist y track
'''