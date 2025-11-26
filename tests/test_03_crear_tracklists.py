from src.db_connection import get_conn
from src.usuario import Usuario
from src.artista import Artista

def crear_tracklist(clean_db):
    print("=== CREAR TRACKLISTS ===")

    u = Usuario.crear("Usuario", "1234")
    print(f"Usuario creado -> id={u.id}, nombre={u.nombre}")
    a = Artista.crear("Artista", "1234")
    print(f"Artista creado -> id={a.id}, nombre={a.nombre}")

    u.crear_tracklist("Playlist usuario")
    a.crear_tracklist("Playlist artista")
    a.crear_album("Album artista")
    print("tracklists creadas")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("")