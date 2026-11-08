
import sqlite3
from pathlib import Path

# Database file location
DB_PATH = Path(__file__).resolve().parent / "tasks.db"


def init_db():

    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.cursor()

        # Create tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
        """)

        # Check whether tasks already exist
        cursor.execute("SELECT COUNT(*) FROM tasks")
        count = cursor.fetchone()[0]

        # Insert sample tasks only if table is empty
        if count == 0:

            sample_tasks = [
                ("Learn FastAPI", 0),
                ("Build CRUD API", 0),
                ("Push project to GitHub", 1)
            ]

            cursor.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                sample_tasks
            )

        conn.commit()

    finally:
        conn.close()


def get_all_tasks():

    conn = sqlite3.connect(DB_PATH)

    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks")

        rows = cursor.fetchall()

        return [
            {
                "id": row["id"],
                "title": row["title"],
                "done": bool(row["done"])
            }
            for row in rows
        ]

    finally:
        conn.close()


def get_task_by_id(task_id):

    conn = sqlite3.connect(DB_PATH)

    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }

    finally:
        conn.close()


def create_task(title):

    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
            """,
            (title, 0)
        )

        # Get automatically generated ID
        new_id = cursor.lastrowid

        conn.commit()

        return {
            "id": new_id,
            "title": title,
            "done": False
        }

    finally:
        conn.close()


def update_task(task_id, title=None, done=None):

    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.cursor()

        # Check whether task exists
        cursor.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        # Keep existing values if not provided
        current_title = row[1]
        current_done = row[2]

        if title is not None:
            current_title = title

        if done is not None:
            current_done = int(done)

        # Update database
        cursor.execute(
            """
            UPDATE tasks
            SET title = ?, done = ?
            WHERE id = ?
            """,
            (current_title, current_done, task_id)
        )

        conn.commit()

        return {
            "id": task_id,
            "title": current_title,
            "done": bool(current_done)
        }

    finally:
        conn.close()


def delete_task(task_id):

    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        deleted = cursor.rowcount > 0

        conn.commit()

        return deleted

    finally:
        conn.close()

