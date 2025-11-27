from src.db_connection import get_conn

class Track():
    def __init__(self, id_, titulo, duracion, artista_id):
        self.id = id_
        self.titulo = titulo
        self.duracion = duracion
        self.artista_id = artista_id

    @classmethod
    def listar_todos(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, title, duration, artist_id FROM tracks ORDER BY title")
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3]) for r in rows]
        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_por_id(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, title, duration, artist_id FROM tracks WHERE id = %s
            """, (id_,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3]) if r else None
        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_por_titulo(cls, titulo):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, title, duration, artist_id FROM tracks WHERE title = %s
            """, (titulo,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3]) if r else None
        finally:
            cur.close()
            conn.close()