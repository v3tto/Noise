import pytest
from src.db_connection import get_conn

@pytest.fixture
def clean_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM followers")
    cur.execute("DELETE FROM favorites")
    cur.execute("DELETE FROM tracklist_tracks")
    cur.execute("DELETE FROM tracklists")
    cur.execute("DELETE FROM tracks")
    cur.execute("DELETE FROM artists")
    cur.execute("DELETE FROM users")
    conn.commit()

    cur.close()
    conn.close()
    yield

    # Limpieza final
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM followers")
    cur.execute("DELETE FROM favorites")
    cur.execute("DELETE FROM tracklist_tracks")
    cur.execute("DELETE FROM tracklists")
    cur.execute("DELETE FROM tracks")
    cur.execute("DELETE FROM artists")
    cur.execute("DELETE FROM users")
    conn.commit()
    cur.close()
    conn.close()
