from datetime import datetime

from db import schema, connection


def make_session(
    subject_id: int,
    plan_id: int = 0,
    actual_duration: int = 0,
):
    schema.init_db()

    with connection.get_conn() as conn:

        # Kiểm tra subject tồn tại
        subject_exists = conn.execute(
            """
            SELECT 1
            FROM subjects
            WHERE id = ?
            """,
            (subject_id,)
        ).fetchone()

        if not subject_exists:
            raise ValueError(
                f"Subject id={subject_id} không tồn tại"
            )

        # Nếu truyền plan_id thì kiểm tra plan
        if plan_id != 0:
            plan_exists = conn.execute(
                """
                SELECT 1
                FROM plans
                WHERE id = ?
                """,
                (plan_id,)
            ).fetchone()

            if not plan_exists:
                raise ValueError(
                    f"Plan id={plan_id} không tồn tại"
                )        
        # Tạo session học
        cur = conn.execute(
            """
            INSERT INTO log
            (
                subject_id,
                plan_id,
                study_date,
                actual_duration
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                subject_id,
                plan_id,
                datetime.now(),
                actual_duration,
            )
        )

        # Trả về id session vừa tạo
        return cur.lastrowid