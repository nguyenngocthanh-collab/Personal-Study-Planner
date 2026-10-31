from db import schema,connection

def add_plan(subject_id: int, title: str, duration: int, status: str = "pending"):
    schema.init_db()
    with connection.get_conn() as conn:
        # 1. Kiểm tra subject tồn tại
        exists = conn.execute(
            "SELECT 1 FROM subjects WHERE id = ?", (subject_id,)
        ).fetchone()
        if not exists:
            raise ValueError(f"Môn id={subject_id} không tồn tại")

        # 2. Insert plan
        cur = conn.execute(
            "INSERT INTO plans (subject_id, title, planned_duration, status) "
            "VALUES (?, ?, ?, ?)",
            (subject_id, title, duration, status),
        )
        return cur.lastrowid

def remove_plan(plan_id):
    #kiểm tra có tồn tại plan không-nếu có xóa plan
    schema.init_db()
    with connection.get_conn() as conn:
        #kiểm tra xem có tồn tại không
        exists=conn.execute(
            "SELECT 1 FROM plans WHERE id = ?",(plan_id,)
        ).fetchone()
        if not exists:
            raise ValueError(f"plan id={plan_id} n/a")
        cur = conn.execute(
            "DELETE FROM plans WHERE id=?",(plan_id,)
        )

def set_status(plan_id,status):
    schema.init_db()
    with connection.get_conn() as conn:
        exsist=conn.execute(
            "SELECT 1 FROM plans WHERE id = ?", (plan_id,)
        ).fetchone()
        if not exsist:
            raise ValueError(f"plan id={plan_id} n/a")
        cur = conn.execute(
            "UPDATE plans SET status=? WHERE id=?",(status,plan_id,)
            )

