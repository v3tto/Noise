from src.db_connection import get_conn
from src.track import Track

class Track_list:
    def __init__(self, id_, titulo, usuario_id, tipo, lanzamiento, publico=True):
        self.id = id_
        self.titulo = titulo
        self.usuario_id = usuario_id
        self.tipo = tipo # "album" o "playlist"
        self.lanzamiento = lanzamiento
        self.publico = publico

    def agregar_track(self, track_id):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT COALESCE(MAX(position), 0) + 1
                FROM tracklist_tracks
                WHERE tracklist_id = %s
            """, (self.id,))
            siguiente_posicion = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO tracklist_tracks (tracklist_id, track_id, position)
                VALUES (%s, %s, %s)
            """, (self.id, track_id, siguiente_posicion))

            conn.commit()
            return True
        
        except Exception as e:
            print("Error al agregar track:", e)
            return False
        
        finally:
            cur.close()
            conn.close()
    
    def eliminar_track(self, track_id):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT position
                FROM tracklist_tracks
                WHERE tracklist_id = %s AND track_id = %s
            """, (self.id, track_id))

            result = cur.fetchone()
            if not result:
                return False

            position_eliminada = result[0]

            cur.execute("""
                DELETE FROM tracklist_tracks
                WHERE tracklist_id = %s AND track_id = %s
            """, (self.id, track_id))

            cur.execute("""
                UPDATE tracklist_tracks
                SET position = position - 1
                WHERE tracklist_id = %s AND position > %s
            """, (self.id, position_eliminada))

            conn.commit()
            return True

        except Exception as e:
            print("Error al eliminar track:", e)
            return False
        
        finally:
            cur.close()
            conn.close()

    def listar_tracks(self):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    tlt.position,
                    t.id,
                    t.title,
                    t.duration,
                    u.username
                FROM tracklist_tracks tlt
                JOIN tracks t ON t.id = tlt.track_id
                JOIN users u ON u.id = t.artist_id
                WHERE tlt.tracklist_id = %s
                ORDER BY tlt.position ASC
            """, (self.id,))
            
            rows = cur.fetchall()

            return [
                {
                    "position": r[0],
                    "track_id": r[1],
                    "title": r[2],
                    "duration": r[3],
                    "artist": r[4]
                }
                for r in rows
            ]

        finally:
            cur.close()
            conn.close()

