from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

from .models import Completion, Habit, Periodicity


def build_fixtures():
    """
    5 predefined habits (>=1 daily and >=1 weekly) + 4 weeks of completion timestamps.
    (Used for demo + deterministic testing.)
    """
    base = datetime(2026, 1, 6, 9, 0, 0)  # fixed start for reproducibility

    habits = [
        Habit(str(uuid4()), "Drink water", "Drink 2 liters of water", Periodicity.DAILY, base),
        Habit(str(uuid4()), "Walk", "Walk 30 minutes", Periodicity.DAILY, base),
        Habit(str(uuid4()), "Read", "Read 20 minutes", Periodicity.DAILY, base),
        Habit(str(uuid4()), "Call family", "Call family once a week", Periodicity.WEEKLY, base),
        Habit(str(uuid4()), "Plan week", "Create weekly plan every Sunday", Periodicity.WEEKLY, base),
    ]

    # 4 weeks = 28 days window
    completions = []

    # Habit 1: strong daily streak (10-day streak, then gaps)
    for i in range(10):
        completions.append(Completion(None, habits[0].id, base + timedelta(days=i)))

    # Habit 2: daily with breaks (3, break, 4)
    for i in [0, 1, 2, 5, 6, 7, 8]:
        completions.append(Completion(None, habits[1].id, base + timedelta(days=i)))

    # Habit 3: daily scattered (no long streak)
    for i in [1, 4, 9, 14, 20, 27]:
        completions.append(Completion(None, habits[2].id, base + timedelta(days=i)))

    # Weekly habits: use one completion per week (ISO week periods)
    # Week 1..4 (some gaps)
    # Call family: 3-week streak
    for i in [0, 7, 14]:
        completions.append(Completion(None, habits[3].id, base + timedelta(days=i)))

    # Plan week: week 1, skip week 2, week 3, week 4 -> best streak 2
    for i in [0, 14, 21]:
        completions.append(Completion(None, habits[4].id, base + timedelta(days=i)))

    return habits, completions
