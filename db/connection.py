import sqlite3
import os
from contextlib import contextmanager

#create path 
db_path=os.path.join(
    os.path.dirname(__file__),
    "plan.db"
)
#connect path(open dtb file)
@contextmanager # cái này dùng để sử dụng with
def get_conn():
    conn = sqlite3.connect(db_path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_key=ON")
    conn.execute("PRAGMA journal_mode = WAL")
    try:    #dòng này để sử dụng with ở nơi khác 
        yield conn # cái dòng này đưa vào with get_conn() as conn same as return func
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()