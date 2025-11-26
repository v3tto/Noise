from src.db_connection import get_conn
from src.artista import Artista

def test_crear_tracks(clean_db):
    print("=== CREAR TRACKS ===")
    
    a = Artista.crear("ArtistaA", "1234")
    print(f"Artista creado -> id={a.id}, nombre={a.nombre}")

    a.crear_track("CancionA", 180)
    a.crear_track("CancionB", 170)
    a.crear_track("CancionC", 190)
    print("Tracks creados: CancionA, CancionB, CancionC")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, duration, artist_id FROM tracks WHERE artist_id=%s ORDER BY id ASC", (a.id,))
    rows = cur.fetchall()

    print("Filas encontradas en BD:")
    for row in rows:
        print(row)

    assert len(rows) == 3
    assert rows[0][1] == "CancionA"
    assert rows[1][1] == "CancionB"
    assert rows[2][1] == "CancionC"

    assert rows[0][3] == a.id
    assert rows[1][3] == a.id
    assert rows[2][3] == a.id

    cur.close()
    conn.close()
