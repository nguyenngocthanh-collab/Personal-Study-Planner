from db import schema, connection

def add_subject(name:str, description=None):
    schema.init_db()
    with connection.get_conn() as conn:
        cur=conn.execute(
        "insert into subjects "
        "(name, description, status) "
        "values (?,?,?)",
        (name, description, "pending")
        )
        return cur.lastrowid 
    
def subject_list():
    schema.init_db()
    with connection.get_conn() as conn:
        cur=conn.execute(
            "select * from subjects"
        )
        rows = cur.fetchall()
    return [dict(r) for r in rows]

def subject_edit(subject_id:int, name:str, description=None):
    schema.init_db()
    with connection.get_conn() as conn:
        cur = conn.execute(
            "update subjects "
            "set name=?, description=? where id=?",
            (name, description, subject_id)
        )
        return cur.rowcount


def delete_subject(subject_id):
    schema.init_db()
    with connection.get_conn() as conn:
        cur=conn.execute(
            "delete from subjects "
            "where id=?",
            (subject_id,),
        )
        return cur.rowcount


