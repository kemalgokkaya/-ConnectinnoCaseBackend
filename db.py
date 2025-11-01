import sqlite3
from contextlib import contextmanager
from typing import Generator

DATABASE_PATH = "sqlite.db"

@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # removed UNIQUE constraint on user_id so a user can have multiple notes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                note TEXT NOT NULL,
                user_id TEXT NOT NULL
            )
        """)
        conn.commit()

def create_note(title: str, note: str, user_id: str) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (title, note, user_id) VALUES (?, ?, ?)",
            (title, note, user_id)
        )
        return cursor.lastrowid

def get_all_notes(user_id: str) -> list[dict]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, note, user_id FROM notes WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        # ensure types match Pydantic expectations (id:int, title:str, note:str, user_id:str)
        result = []
        for row in rows:
            result.append({
                "id": int(row["id"]),
                "title": str(row["title"]),
                "note": str(row["note"]),
                "user_id": str(row["user_id"]),
            })
        return result

def get_note_by_id(note_id: int, user_id: str) -> dict | None:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, note, user_id FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": int(row["id"]),
            "title": str(row["title"]),
            "note": str(row["note"]),
            "user_id": str(row["user_id"]),
        }

def delete_note(note_id: int, user_id: str) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id))
        return cursor.rowcount > 0

def update_note(note_id: int, title: str, note: str, user_id: str) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE notes SET title = ?, note = ? WHERE id = ? AND user_id = ?",
            (title, note, note_id, user_id)
        )
        return cursor.rowcount > 0