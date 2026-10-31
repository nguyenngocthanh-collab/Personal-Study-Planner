from db import schema, connection


def done_plan(plan_id: int):
    schema.init_db()

    with connection.get_conn() as conn:

        exists = conn.execute(
            "SELECT 1 FROM plans WHERE id = ?",
            (plan_id,)
        ).fetchone()

        if not exists:
            raise ValueError(
                f"Plan id={plan_id} không tồn tại"
            )

        cur = conn.execute(
            """
            UPDATE plans
            SET status = ?
            WHERE id = ?
            """,
            ("done", plan_id)
        )

        return cur.rowcount

def check_undone():
    schema.init_db()

    with connection.get_conn() as conn:
        rows=conn.execute(
            "SELECT * FROM plans WHERE status=?",("in_progress",)
            ).fetchall()
        return rows
        

def history():
    schema.init_db()
    
    with connection.get_conn() as conn:
        rows=conn.execute(
            "SELECT * FROM logs",
            ).fetchall()
        return rows


