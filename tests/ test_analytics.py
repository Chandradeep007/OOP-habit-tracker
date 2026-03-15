from habits.analytics import longest_streak_all, longest_streak_for_habit
from habits.fixtures import build_fixtures


def test_longest_streak_for_habit():
    habits, completions = build_fixtures()
    h_drink = habits[0]  # 10-day streak in fixtures
    s = longest_streak_for_habit(h_drink, completions)
    assert s == 10


def test_longest_streak_all():
    habits, completions = build_fixtures()
    best_id, best_len = longest_streak_all(habits, completions)
    assert best_id is not None
    assert best_len == 10
