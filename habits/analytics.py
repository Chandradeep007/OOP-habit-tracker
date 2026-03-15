from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Iterable, List, Optional, Tuple

from .models import Completion, Habit, Periodicity


def list_all_habits(habits: Iterable[Habit]) -> List[Habit]:
    return list(habits)


def list_habits_by_periodicity(habits: Iterable[Habit], periodicity: Periodicity) -> List[Habit]:
    return [h for h in habits if h.periodicity == periodicity]


def _period_key(habit: Habit, ts: datetime) -> date:
    """
    Returns a comparable 'period start' date.
    DAILY  -> that calendar day
    WEEKLY -> Monday of ISO week
    """
    d = ts.date()
    if habit.periodicity == Periodicity.DAILY:
        return d
    iso = d.isocalendar()  # (year, week, weekday)
    monday = date.fromisocalendar(iso.year, iso.week, 1)
    return monday


def longest_streak_for_habit(habit: Habit, completions: Iterable[Completion]) -> int:
    """
    Streak = consecutive successful periods.
    Multiple completions in the same period count once (but raw data is preserved).
    """
    keys = {_period_key(habit, c.completed_at) for c in completions if c.habit_id == habit.id}
    if not keys:
        return 0

    sorted_keys = sorted(keys)
    best = 1
    current = 1

    step = timedelta(days=1) if habit.periodicity == Periodicity.DAILY else timedelta(days=7)

    for prev, nxt in zip(sorted_keys, sorted_keys[1:]):
        if nxt - prev == step:
            current += 1
            best = max(best, current)
        else:
            current = 1

    return best


def longest_streak_all(habits: Iterable[Habit], completions: Iterable[Completion]) -> Tuple[Optional[str], int]:
    """
    Returns (habit_id, streak_len) for the best streak overall.
    """
    best_id: Optional[str] = None
    best_len = 0

    habits_list = list(habits)
    comps_list = list(completions)

    for h in habits_list:
        s = longest_streak_for_habit(h, comps_list)
        if s > best_len:
            best_len = s
            best_id = h.id

    return best_id, best_len
