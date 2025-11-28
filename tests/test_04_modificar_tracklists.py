from src.db_connection import get_conn
from src.usuario import Usuario
from src.artista import Artista
from src.tracklist import Tracklist


def test_modificar_tracklists(clean_db):
    print("=== MODIFICAR TRACKLISTS ===")

    u = Usuario.crear("UsuarioTest", "1234")
    a = Artista.crear("ArtistaTest", "1234")
    print(f"Usuario creado -> id={u.id}, nombre={u.nombre}")
    print(f"Artista creado -> id={a.id}, nombre={a.nombre}")

    id_pl = u.crear_tracklist("PlaylistTest")
    id_al = a.crear_album("AlbumTest")

    playlist = Tracklist.buscar_por_id(id_pl)
    album = Tracklist.buscar_por_id(id_al)

    t1_id = a.crear_track("Canción 1", 120)
    t2_id = a.crear_track("Canción 2", 150)
    t3_id = a.crear_track("Canción 3", 180)
    print("Tracks creados (ids):", t1_id, t2_id, t3_id)

    assert playlist.agregar_track(t1_id) is True
    assert playlist.agregar_track(t2_id) is True
    assert playlist.agregar_track(t3_id) is True

    assert album.agregar_track(t1_id) is True
    assert album.agregar_track(t2_id) is True

    ok = playlist.eliminar_track(t2_id)
    assert ok is True

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT track_id
        FROM tracklist_tracks
        WHERE tracklist_id = %s
    """, (playlist.id,))
    after_delete = [r[0] for r in cur.fetchall()]

    print("Tracks en playlist después de eliminar:", after_delete)
    assert t2_id not in after_delete
    assert set(after_delete) == {t1_id, t3_id}

    assert playlist.eliminar_track(999999) is False

    cur.execute("""
        SELECT track_id
        FROM tracklist_tracks
        WHERE tracklist_id = %s
        ORDER BY track_id ASC
    """, (album.id,))
    album_tracks = [r[0] for r in cur.fetchall()]

    print("Tracks en álbum:", album_tracks)
    assert set(album_tracks) == {t1_id, t2_id}

    cur.close()
    conn.close()
