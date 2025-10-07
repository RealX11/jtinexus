
import sqlite3

def get_conn(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    return conn

def infer_table_and_columns(conn):
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
    tables = [r["name"] for r in cur.fetchall()]
    table = tables[0] if tables else None
    if not table:
        return None, []
    cur = conn.execute(f"PRAGMA table_info({table})")
    cols = [r["name"] for r in cur.fetchall()]
    return table, cols

def pick_material_col(cols):
    targets = {"material_code","materialcode","malzeme_kodu","malzemekodu"}
    for c in cols:
        if c.lower() in targets:
            return c
    return cols[0] if cols else None
