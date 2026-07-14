from pathlib import Path
import sqlite3

DB_PATH = Path("atlas.db")

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database file not found: {DB_PATH}")

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(\"transaction\")")
    columns = [row[1] for row in cursor.fetchall()]

    if "running_balance" in columns:
        print("Column already exists: running_balance")
    else:
        cursor.execute(
            "ALTER TABLE \"transaction\" ADD COLUMN running_balance NUMERIC"
        )
        print("Added running_balance column to transaction table.")
    conn.commit()
