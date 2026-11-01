from db import schema, connection
from datetime import datetime


def add_plan(
    subject_id: int, 
    title: str, 
    planned_date: datetime, 
    duration: int, 
    status: str = "pending"
) -> int:
    """
    Thêm một kế hoạch học tập mới vào cơ sở dữ liệu.

    Args:
        subject_id: ID của môn học (phải tồn tại trong bảng subjects).
        title: Tiêu đề của kế hoạch (VD: "Học chương 1").
        planned_date: Ngày dự định học (sẽ tự động format thành YYYY-MM-DD).
        duration: Thời lượng dự kiến (tính bằng phút).
        status: Trạng thái ban đầu. Mặc định là "pending".

    Returns:
        ID của kế hoạch vừa được tạo trong DB.

    Raises:
        ValueError: Nếu `subject_id` không tồn tại trong bảng subjects.
    """
    date_str = planned_date.strftime("%Y-%m-%d") 
    
    schema.init_db()
    with connection.get_conn() as conn:
        exists = conn.execute(
            "SELECT 1 FROM subjects WHERE id = ?", (subject_id,)
        ).fetchone()
        
        if not exists:
            raise ValueError(f"Môn id={subject_id} không tồn tại")

        cur = conn.execute(
            "INSERT INTO plans (subject_id, title, planned_date, planned_duration, status) "
            "VALUES (?, ?, ?, ?, ?)",
            (subject_id, title, date_str, duration, status),
        )
        return cur.lastrowid


def remove_plan(plan_id: int) -> int:
    """
    Xóa một kế hoạch học tập theo ID.

    Args:
        plan_id: ID của kế hoạch cần xóa.

    Returns:
        Số dòng bị ảnh hưởng (1 nếu xóa thành công).

    Raises:
        ValueError: Nếu `plan_id` không tồn tại trong DB.
    """
    schema.init_db()
    with connection.get_conn() as conn:
        exists = conn.execute(
            "SELECT 1 FROM plans WHERE id = ?", (plan_id,)
        ).fetchone()
        
        if not exists:
            raise ValueError(f"Plan id={plan_id} không tồn tại")
            
        cur = conn.execute(
            "DELETE FROM plans WHERE id = ?", (plan_id,)
        )
        return cur.rowcount


def set_status(plan_id: int, status: str) -> int:
    """
    Cập nhật trạng thái của một kế hoạch học tập.

    Args:
        plan_id: ID của kế hoạch cần cập nhật.
        status: Trạng thái mới (thường là 'pending', 'in_progress', 'done', 'skip').

    Returns:
        Số dòng bị ảnh hưởng (1 nếu cập nhật thành công).

    Raises:
        ValueError: Nếu `plan_id` không tồn tại trong DB.
    """
    schema.init_db()
    with connection.get_conn() as conn:
        exists = conn.execute(
            "SELECT 1 FROM plans WHERE id = ?", (plan_id,)
        ).fetchone()
        
        if not exists:
            raise ValueError(f"Plan id={plan_id} không tồn tại")
            
        cur = conn.execute(
            "UPDATE plans SET status = ? WHERE id = ?", 
            (status, plan_id,)
        )
        return cur.rowcount
    