from pathlib import Path
import sqlite3

DB_PATH = Path("atlas.db")

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database file not found: {DB_PATH}")

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(\"transaction\")")
    columns = [row[1] for row in cursor.fetchall()]

    if "merchant" in columns:
        print("Column already exists: merchant")
    else:
        cursor.execute(
            "ALTER TABLE \"transaction\" ADD COLUMN merchant VARCHAR"
        )
        print("Added merchant column to transaction table.")
    conn.commit()
