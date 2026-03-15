from __future__ import annotations

import argparse
from typing import Optional

from .analytics import longest_streak_all, longest_streak_for_habit, list_habits_by_periodicity
from .fixtures import build_fixtures
from .models import Periodicity
from .repository import SQLiteRepository


def _parse_periodicity(value: str) -> Periodicity:
    v = value.strip().upper()
    if v not in ("DAILY", "WEEKLY"):
        raise argparse.ArgumentTypeError("periodicity must be DAILY or WEEKLY")
    return Periodicity(v)


def cmd_init_db(repo: SQLiteRepository, _args: argparse.Namespace) -> None:
    repo.init_db()
    print("✅ Database initialized.")

def cmd_reset_db(repo: SQLiteRepository, _args: argparse.Namespace) -> None:
    repo.reset_db()
    print("✅ Database reset.")

def cmd_add_habit(repo: SQLiteRepository, args: argparse.Namespace) -> None:
    habit = repo.create_habit(args.name, args.task, args.periodicity)
    print("✅ Habit created:")
    print(f"  id: {habit.id}")
    print(f"  name: {habit.name}")
    print(f"  periodicity: {habit.periodicity.value}")

def cmd_list_habits(repo: SQLiteRepository, args: argparse.Namespace) -> None:
    habits = repo.list_habits(args.periodicity)
    if not habits:
        print("(no habits found)")
        return
    for h in habits:
        print(f"- {h.id} | {h.periodicity.value} | {h.name} — {h.task_spec}")

def cmd_delete_habit(repo: SQLiteRepository, args: argparse.Namespace) -> None:
    ok = repo.delete_habit(args.habit_id)
    print("✅ Deleted." if ok else "❌ Habit id not found.")

def cmd_checkoff(repo: SQLiteRepository, args: argparse.Namespace) -> None:
    habit = repo.get_habit(args.habit_id)
    if not habit:
        print("❌ Habit id not found.")
        return
    c = repo.add_completion(args.habit_id)
    print(f"✅ Check-off recorded for '{habit.name}' at {c.completed_at.isoformat()}")

def cmd_init_fixtures(repo: SQLiteRepository, args: argparse.Namespace) -> None:
    if args.reset:
        repo.reset_db()
    else:
        repo.init_db()
    habits, completions = build_fixtures()
    repo.bulk_insert(habits, completions)
    print("✅ Fixtures loaded (5 habits + 4 weeks of completion data).")

def cmd_longest_all(repo: SQLiteRepository, _args: argparse.Namespace) -> None:
    habits = repo.list_habits()
    comps = repo.list_completions()
    best_id, best_len = longest_streak_all(habits, comps)
    if not best_id:
        print("(no streaks yet)")
        return
    best_habit = repo.get_habit(best_id)
    print(f"🏆 Longest streak overall: {best_len} periods — {best_habit.name} ({best_habit.periodicity.value})")

def cmd_longest_for(repo: SQLiteRepository, args: argparse.Namespace) -> None:
    habit = repo.get_habit(args.habit_id)
    if not habit:
        print("❌ Habit id not found.")
        return
    comps = repo.list_completions(habit.id)
    streak = longest_streak_for_habit(habit, comps)
    print(f"📈 Longest streak for '{habit.name}': {streak} periods")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="habits", description="OOFPP Habit Tracker (CLI)")
    p.add_argument("--db", default="habits.db", help="Path to SQLite database file")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init-db").set_defaults(fn=cmd_init_db)
    sub.add_parser("reset-db").set_defaults(fn=cmd_reset_db)

    add = sub.add_parser("add-habit")
    add.add_argument("--name", required=True)
    add.add_argument("--task", required=True)
    add.add_argument("--periodicity", required=True, type=_parse_periodicity)
    add.set_defaults(fn=cmd_add_habit)

    lst = sub.add_parser("list-habits")
    lst.add_argument("--periodicity", type=_parse_periodicity, required=False)
    lst.set_defaults(fn=cmd_list_habits)

    dele = sub.add_parser("delete-habit")
    dele.add_argument("habit_id")
    dele.set_defaults(fn=cmd_delete_habit)

    chk = sub.add_parser("checkoff")
    chk.add_argument("habit_id")
    chk.set_defaults(fn=cmd_checkoff)

    fx = sub.add_parser("init-fixtures")
    fx.add_argument("--reset", action="store_true", help="Reset DB before inserting fixtures")
    fx.set_defaults(fn=cmd_init_fixtures)

    sub.add_parser("analytics-longest-all").set_defaults(fn=cmd_longest_all)

    lf = sub.add_parser("analytics-longest")
    lf.add_argument("habit_id")
    lf.set_defaults(fn=cmd_longest_for)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    repo = SQLiteRepository(args.db)
    args.fn(repo, args)


if __name__ == "__main__":
    main()
