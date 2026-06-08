import sqlite3
from config import DATABASE_PATH
import os

os.makedirs("./data", exist_ok=True)

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            game_id TEXT PRIMARY KEY,
            character_name TEXT,
            character_class TEXT,
            character_backstory TEXT,
            world_setting TEXT,
            current_scene TEXT,
            current_image TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS story (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id TEXT,
            role TEXT,
            content TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_game(game: dict):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("""
        INSERT INTO games (game_id, character_name, character_class, character_backstory, world_setting, current_scene, current_image)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        game["game_id"],
        game["character_name"],
        game["character_class"],
        game["character_backstory"],
        game["world_setting"],
        game["current_scene"],
        game["current_image"]
    ))
    conn.commit()
    conn.close()


def update_scene(game_id: str, current_scene: str, current_image: str):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("""
        UPDATE games SET current_scene = ?, current_image = ?
        WHERE game_id = ?
    """, (current_scene, current_image, game_id))
    conn.commit()
    conn.close()


def get_game(game_id: str) -> dict:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games WHERE game_id = ?", (game_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "game_id": row[0],
        "character_name": row[1],
        "character_class": row[2],
        "character_backstory": row[3],
        "world_setting": row[4],
        "current_scene": row[5],
        "current_image": row[6]
    }


def save_story_beat(game_id: str, role: str, content: str):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("""
        INSERT INTO story (game_id, role, content)
        VALUES (?, ?, ?)
    """, (game_id, role, content))
    conn.commit()
    conn.close()


def get_story(game_id: str) -> list:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content FROM story
        WHERE game_id = ?
        ORDER BY id ASC
    """, (game_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]


def get_all_games() -> list:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT game_id, character_name, character_class FROM games")
    rows = cursor.fetchall()
    conn.close()
    return [{"game_id": row[0], "character_name": row[1], "character_class": row[2]} for row in rows]