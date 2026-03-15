from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class Periodicity(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"


@dataclass(frozen=True)
class Habit:
    """Core OOP domain model for a habit."""
    id: str
    name: str
    task_spec: str
    periodicity: Periodicity
    created_at: datetime


@dataclass(frozen=True)
class Completion:
    """A timestamped check-off event (stored separately from Habit)."""
    id: Optional[int]
    habit_id: str
    completed_at: datetime
