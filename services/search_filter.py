from db import schema, connection

def search_plans(
    title=None,
    subject_id=None,
    status=None,
    planned_date=None
):
    schema.init_db()

    sql = "SELECT * FROM plans WHERE 1=1"
    params = []

    if title:
        sql += " AND title LIKE ?"
        params.append(f"%{title}%")

    if subject_id:
        sql += " AND subject_id = ?"
        params.append(subject_id)

    if status:
        sql += " AND status = ?"
        params.append(status)

    if planned_date:
        sql += " AND planned_date = ?"
        params.append(planned_date)

    with connection.get_conn() as conn:
        return conn.execute(
            sql,
            tuple(params)
        ).fetchall()