# OOFPP Habit Tracker (CLI)

## Overview
A Python **CLI-only** habit tracking application that demonstrates:
- **Object-Oriented Programming (OOP):** domain modeling with `Habit` and timestamped `Completion` events
- **Persistence:** data stored in **SQLite** so habits and check-offs remain available across sessions
- **Functional Programming (FP):** analytics implemented as pure functions over habits + completion events
- **Testing:** basic functionality covered with **pytest**

> This project intentionally uses a command-line interface. A graphical user interface (GUI) is **not required**.

---

## Features
- Create habits with **DAILY** or **WEEKLY** periodicity
- Record **timestamped check-offs** (completion event log)
- Persist habits and completions in **SQLite**
- Analytics:
  - list all habits
  - filter habits by periodicity
  - **longest streak overall**
  - **longest streak for a specific habit**
- Fixtures for repeatable demos:
  - **5 predefined habits**
  - **4 weeks of completion data**
- Unit tests for repository + analytics

---

## Requirements
- macOS / Linux / Windows
- **Python 3.7+** (recommended 3.10+)
- `pip` (included with most Python installs)

---

## Setup (venv)
Create and activate a virtual environment from the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies

Install dependencies using python -m pip (recommended):
```bash
python -m pip install -r requirements.txt
```
## How to Run (CLI)

- Show available commands
```bash
python -m habits.cli --help
```
- Initialize the database
```bash
python -m habits.cli init-db
```
- Add a new habit
```bash
python -m habits.cli add-habit --name "Gym" --task "Workout 45 minutes" --periodicity DAILY
```
- List habits
```bash
python -m habits.cli list-habits
```
- Filter by periodicity:
```bash
python -m habits.cli list-habits --periodicity DAILY
python -m habits.cli list-habits --periodicity WEEKLY
```
- Check-off a habit (records timestamp)
```bash
python -m habits.cli checkoff <HABIT_ID>
```
## Analytics

- Longest streak overall:
```bash
python -m habits.cli analytics-longest-all
```
- Longest streak for a specific habit:
```bash
python -m habits.cli analytics-longest <HABIT_ID>
```
## Using a custom database path (optional)

- If your CLI supports --db, you can run against a specific file:
```bash
python -m habits.cli --db habits.db init-db
```
## Fixtures
To load reproducible demo data (recommended for evaluation), run:
```bash
python -m habits.cli init-fixtures --reset
```
This loads:
  - 5 predefined habits (mix of DAILY and WEEKLY)
  - 4 weeks of completion events for testing analytics and demos

## Analytics (streak definition)

Streak = consecutive successful periods based on the habit periodicity:
   DAILY streak: consecutive calendar days with at least one completion
   WEEKLY streak: consecutive ISO weeks (Monday-based week periods) with at least one completion
   If multiple completions exist in the same period, they count as one success for streak calculation (the raw events are still preserved in the log)

## Tests (pytest)

 Run tests from the project root:
 ```bash
      python -m pytest -q
  ```
Recommended coverage areas:
  - repository: create habit, store completion, persistence behavior
  - analytics: longest streak logic for daily and weekly habits
  - fixtures: data creation consistency

## Project Structure

  oofpp-habits/
  habits/
    __init__.py
    models.py          # OOP domain models (Habit, Completion, Periodicity)
    repository.py      # SQLiteRepository (persistence layer)
    analytics.py       # FP analytics (streak calculations, filters)
    fixtures.py        # 5 habits + 4 weeks demo data
    cli.py             # CLI interface (commands)
  tests/
    test_repository.py
    test_analytics.py
  requirements.txt
  README.md

## Troubleshooting

  zsh: command not found: python
  Use python3 instead:
    ```bash
       python3 -m habits.cli --help
       python3 -m pytest -q
    ```
ModuleNotFoundError: No module named 'habits'

Make sure you are:
  1. in the project root (where habits/ folder exists), and
  2. running commands as a module:
     ```bash
     python -m habits.cli --help
     ```


## Database not updating / old data remains

  Reset and reload fixtures:
  ```bash
  python -m habits.cli init-fixtures --reset
  ```

## Tests failing unexpectedly
Ensure:
    -virtual environment is activated
    -dependencies are installed
    -you run from the project root
```bash
    python -m pip install -r requirements.txt
python -m pytest -q
```

## Notes
 - The application is designed as a CLI backend; no GUI is required.
 - SQLite database files (e.g., habits.db) are generated at runtime; you can safely delete them to start fresh.
 - For final submission packaging, ensure the GitHub repository content and the ZIP submission content are identical.


