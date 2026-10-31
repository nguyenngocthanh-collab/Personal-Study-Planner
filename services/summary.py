# db/models.py (thêm vào cuối file)
from db import connection


def total_hour():
    """Tổng số phút đã học thực tế (toàn bộ logs)."""
    with connection.get_conn() as conn:
        row = conn.execute(
            "SELECT COALESCE(SUM(actual_duration), 0) AS total FROM logs"
        ).fetchone()
        return row["total"]


def totalhr_each():
    """Số phút đã học của từng môn. Trả về list[dict]."""
    with connection.get_conn() as conn:
        rows = conn.execute("""
            SELECT s.id, s.name,
                   COALESCE(SUM(l.actual_duration), 0) AS minutes,
                   COUNT(l.id) AS sessions
            FROM subjects s
            LEFT JOIN logs l ON l.subject_id = s.id
            GROUP BY s.id
            ORDER BY minutes DESC
        """).fetchall()
        return [dict(r) for r in rows]


def completed():
    """Đếm plan đã hoàn thành / tổng số plan."""
    with connection.get_conn() as conn:
        row = conn.execute("""
            SELECT
                SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END) AS done,
                COUNT(*) AS total
            FROM plans
        """).fetchone()
        return {"done": row["done"] or 0, "total": row["total"] or 0}


def comrate():
    """Tỷ lệ hoàn thành plan (%). = done / total * 100."""
    c = completed()
    if c["total"] == 0:
        return 0.0
    return round(c["done"] * 100.0 / c["total"], 1)


def compare():
    """
    So sánh thời lượng KẾ HOẠCH vs THỰC TẾ cho từng môn.
    Trả về list[dict]: mỗi môn có planned và actual.
    """
    with connection.get_conn() as conn:
        rows = conn.execute("""
            SELECT
                s.id,
                s.name,
                COALESCE((SELECT SUM(planned_duration)
                          FROM plans WHERE subject_id = s.id), 0) AS planned,
                COALESCE((SELECT SUM(actual_duration)
                          FROM logs  WHERE subject_id = s.id), 0) AS actual
            FROM subjects s
            ORDER BY s.name
        """).fetchall()
        return [dict(r) for r in rows]
