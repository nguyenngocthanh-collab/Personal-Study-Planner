# db/schema.py
from .connection import get_conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
        -- BẢNG 1: MÔN HỌC
        CREATE TABLE IF NOT EXISTS subjects (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL UNIQUE,
            description TEXT,
            status      TEXT DEFAULT 'pending'
                        CHECK(status IN ('pending', 'ended'))
        );

        -- BẢNG 2: KẾ HOẠCH CẦN HỌC
        CREATE TABLE IF NOT EXISTS plans (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id       INTEGER NOT NULL,
            title            TEXT NOT NULL,
            planned_date     DATE NOT NULL,  
            planned_duration INTEGER NOT NULL,
            status           TEXT DEFAULT 'pending'
                             CHECK(status IN ('pending','in_progress','done','skip')),
            created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
        );

        -- BẢNG 3: LỊCH SỬ ĐÃ HỌC THỰC TẾ
        CREATE TABLE IF NOT EXISTS logs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id      INTEGER NOT NULL,
            plan_id         INTEGER,                          
            study_date      DATE NOT NULL,
            actual_duration INTEGER NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
            FOREIGN KEY (plan_id)    REFERENCES plans(id)    ON DELETE SET NULL
            --                                                 
            --                                        xóa plan → log vẫn còn, plan_id = NULL
        );

        CREATE INDEX IF NOT EXISTS idx_logs_date     ON logs(study_date);
        CREATE INDEX IF NOT EXISTS idx_logs_subject  ON logs(subject_id);
        CREATE INDEX IF NOT EXISTS idx_plans_status  ON plans(status);
        """)