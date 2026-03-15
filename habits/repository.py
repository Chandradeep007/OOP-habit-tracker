from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Iterable, List, Optional
from uuid import uuid4

from .models import Completion, Habit, Periodicity


class SQLiteRepository:
    """Persistence layer (I/O only). Keeps analytics pure."""
    def __init__(self, db_path: str = "habits.db") -> None:
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS habits (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    task_spec TEXT NOT NULL,
                    periodicity TEXT NOT NULL CHECK (periodicity IN ('DAILY','WEEKLY')),
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id TEXT NOT NULL,
                    completed_at TEXT NOT NULL,
                    FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_completions_habit ON completions(habit_id);
                CREATE INDEX IF NOT EXISTS idx_completions_time ON completions(completed_at);
                """
            )

    def reset_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                DROP TABLE IF EXISTS completions;
                DROP TABLE IF EXISTS habits;
                """
            )
        self.init_db()

    # ---------- Habits ----------
    def create_habit(self, name: str, task_spec: str, periodicity: Periodicity) -> Habit:
        habit = Habit(
            id=str(uuid4()),
            name=name.strip(),
            task_spec=task_spec.strip(),
            periodicity=periodicity,
            created_at=datetime.utcnow(),
        )
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO habits (id, name, task_spec, periodicity, created_at) VALUES (?, ?, ?, ?, ?)",
                (habit.id, habit.name, habit.task_spec, habit.periodicity.value, habit.created_at.isoformat()),
            )
        return habit

    def delete_habit(self, habit_id: str) -> bool:
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
            return cur.rowcount > 0

    def get_habit(self, habit_id: str) -> Optional[Habit]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM habits WHERE id = ?", (habit_id,)).fetchone()
        if not row:
            return None
        return Habit(
            id=row["id"],
            name=row["name"],
            task_spec=row["task_spec"],
            periodicity=Periodicity(row["periodicity"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def list_habits(self, periodicity: Optional[Periodicity] = None) -> List[Habit]:
        query = "SELECT * FROM habits"
        params = ()
        if periodicity:
            query += " WHERE periodicity = ?"
            params = (periodicity.value,)
        query += " ORDER BY created_at ASC"

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

        return [
            Habit(
                id=r["id"],
                name=r["name"],
                task_spec=r["task_spec"],
                periodicity=Periodicity(r["periodicity"]),
                created_at=datetime.fromisoformat(r["created_at"]),
            )
            for r in rows
        ]

    # ---------- Completions ----------
    def add_completion(self, habit_id: str, when: Optional[datetime] = None) -> Completion:
        when = when or datetime.utcnow()
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
                (habit_id, when.isoformat()),
            )
            completion_id = cur.lastrowid
        return Completion(id=completion_id, habit_id=habit_id, completed_at=when)

    def list_completions(self, habit_id: Optional[str] = None) -> List[Completion]:
        query = "SELECT * FROM completions"
        params = ()
        if habit_id:
            query += " WHERE habit_id = ?"
            params = (habit_id,)
        query += " ORDER BY completed_at ASC"

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

        return [
            Completion(
                id=r["id"],
                habit_id=r["habit_id"],
                completed_at=datetime.fromisoformat(r["completed_at"]),
            )
            for r in rows
        ]

    # ---------- Fixtures ----------
    def bulk_insert(self, habits: Iterable[Habit], completions: Iterable[Completion]) -> None:
        with self._connect() as conn:
            conn.executemany(
                "INSERT OR REPLACE INTO habits (id, name, task_spec, periodicity, created_at) VALUES (?, ?, ?, ?, ?)",
                [
                    (h.id, h.name, h.task_spec, h.periodicity.value, h.created_at.isoformat())
                    for h in habits
                ],
            )
            conn.executemany(
                "INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
                [
                    (c.habit_id, c.completed_at.isoformat())
                    for c in completions
                ],
            )
