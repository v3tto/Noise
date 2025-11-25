from src.db_connection import get_conn
from src.usuario import Usuario
from src.artista import Artista

def test_crear_usuario(clean_db):
    print("=== CREAR USUARIO ===")
    u = Usuario.crear("UsuarioA", "1234")
    print(f"Usuario creado -> id={u.id}, nombre={u.nombre}, tipo={u.tipo}")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, user_type FROM users WHERE id=%s", (u.id,))
    row = cur.fetchone()
    print("Fila encontrada en BD:", row)

    assert row is not None
    assert row[1] == "UsuarioA"
    assert row[2] == "usuario"

    cur.close()
    conn.close()

def test_crear_artista_visual(clean_db):
    print("=== CREAR ARTISTA ===")
    a = Artista.crear("ArtistaA", "1234", bio="BioA")
    print(f"Artista creado -> id={a.id}, nombre={a.nombre}, bio={a.bio}")

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, username, user_type FROM users WHERE id=%s", (a.id,))
    user_row = cur.fetchone()
    print("Fila en `users`:", user_row)

    cur.execute("SELECT bio, followers FROM artists WHERE id=%s", (a.id,))
    artist_row = cur.fetchone()
    print("Fila en `artists`:", artist_row)

    assert user_row is not None
    assert user_row[1] == "ArtistaA"
    assert user_row[2] == "artista"

    assert artist_row is not None
    assert artist_row[0] == "BioA"
    assert artist_row[1] == 0

    cur.close()
    conn.close()
