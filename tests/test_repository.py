from datetime import datetime
import tempfile

from habits.models import Periodicity
from habits.repository import SQLiteRepository


def test_create_habit_and_persist():
    with tempfile.TemporaryDirectory() as d:
        db_path = f"{d}/t.db"
        repo = SQLiteRepository(db_path)
        repo.init_db()

        h = repo.create_habit("Test", "Do something", Periodicity.DAILY)
        found = repo.get_habit(h.id)

        assert found is not None
        assert found.name == "Test"
        assert found.periodicity == Periodicity.DAILY


def test_add_completion():
    with tempfile.TemporaryDirectory() as d:
        db_path = f"{d}/t.db"
        repo = SQLiteRepository(db_path)
        repo.init_db()

        h = repo.create_habit("X", "Y", Periodicity.WEEKLY)
        repo.add_completion(h.id, when=datetime(2026, 1, 1, 10, 0, 0))

        comps = repo.list_completions(h.id)
        assert len(comps) == 1
        assert comps[0].habit_id == h.id
