from src.db_connection import get_conn
from src.usuario import Usuario
from src.artista import Artista
from src.tracklist import Tracklist

def test_crear_tracklists(clean_db):
    print("=== CREAR TRACKLISTS ===")

    u = Usuario.crear("UsuarioA", "1234")
    print(f"Usuario creado -> id={u.id}, nombre={u.nombre}")

    a = Artista.crear("ArtistaA", "1234")
    print(f"Artista creado -> id={a.id}, nombre={a.nombre}")

    id_pl_u = u.crear_tracklist("Playlist Usuario")
    id_pl_a = a.crear_tracklist("Playlist Artista")
    id_al_a = a.crear_album("Album Artista")

    print("Tracklists creadas con IDs:", id_pl_u, id_pl_a, id_al_a)

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, user_id, tracklist_type
        FROM tracklists
        ORDER BY id ASC
    """)
    rows = cur.fetchall()

    print("Filas encontradas en BD:")
    for row in rows:
        print(row)

    assert len(rows) == 3

    assert rows[0][0] == id_pl_u
    assert rows[0][1] == "Playlist Usuario"
    assert rows[0][2] == u.id
    assert rows[0][3] == "playlist"

    assert rows[1][0] == id_pl_a
    assert rows[1][1] == "Playlist Artista"
    assert rows[1][2] == a.id
    assert rows[1][3] == "playlist"

    assert rows[2][0] == id_al_a
    assert rows[2][1] == "Album Artista"
    assert rows[2][2] == a.id
    assert rows[2][3] == "album"

    cur.close()
    conn.close()