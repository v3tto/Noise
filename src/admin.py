from src.usuario import Usuario
from src.db_connection import get_conn

class Admin(Usuario):

    @classmethod
    def crear(cls, nombre, password, tipo="admin"):
        return super().crear(nombre, password, tipo="admin")

    def crear_track(self, titulo, duracion):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO tracks (title, duration, artist_id)
                VALUES (%s, %s, %s)
            """, (titulo, duracion, self.id))
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            print("Admin: error al crear track:", e)
            return None
        finally:
            cur.close()
            conn.close()

    def eliminar_track(self, track_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM tracks WHERE id = %s", (track_id,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print("Admin: error al eliminar track:", e)
            return False
        finally:
            cur.close()
            conn.close()

    def crear_album(self, titulo):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO tracklists (title, user_id, tracklist_type)
                VALUES (%s, %s, 'album')
            """, (titulo, self.id))
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            print("Admin: error al crear album:", e)
            return None
        finally:
            cur.close()
            conn.close()

    def eliminar_tracklist(self, tracklist_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM tracklists WHERE id = %s", (tracklist_id,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print("Admin: error al eliminar tracklist:", e)
            return False
        finally:
            cur.close()
            conn.close()
