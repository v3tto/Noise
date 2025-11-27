from src.db_connection import get_conn
from src.usuario import Usuario, hash_password

class Admin(Usuario):

    @classmethod
    def crear(cls, nombre, password, tipo="admin"):
        conn = get_conn()
        try:
            cur = conn.cursor()
            pwd_hash = hash_password(password)

            cur.execute("""
                INSERT INTO users (username, user_type, password)
                VALUES (%s, %s, %s)
            """, (nombre, tipo, pwd_hash))

            conn.commit()
            return cls(cur.lastrowid, nombre, tipo, pwd_hash)

        finally:
            cur.close()
            conn.close()

    def eliminar_track(self, track_id):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                DELETE FROM tracklist_tracks WHERE track_id = %s
            """, (track_id,))

            cur.execute("""
                DELETE FROM tracks WHERE id = %s
            """, (track_id,))

            conn.commit()
            print(f"Track {track_id} eliminado por admin.")
            return True

        except Exception as e:
            print("Error al eliminar track:", e)
            return False

        finally:
            cur.close()
            conn.close()

    def eliminar_tracklist(self, tracklist_id):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                DELETE FROM tracklist_tracks WHERE tracklist_id = %s
            """, (tracklist_id,))

            cur.execute("""
                DELETE FROM tracklists WHERE id = %s
            """, (tracklist_id,))

            conn.commit()
            print(f"Tracklist {tracklist_id} eliminada por admin.")
            return True

        except Exception as e:
            print("Error al eliminar tracklist:", e)
            return False

        finally:
            cur.close()
            conn.close()
