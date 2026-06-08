from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(__file__))

from database import init_db, get_game, get_story, get_all_games
from generator import generate_new_game
from story import take_action

app = FastAPI(title="Dungeon RPG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

from fastapi.staticfiles import StaticFiles
os.makedirs("./data/images", exist_ok=True)
app.mount("/images", StaticFiles(directory="./data/images"), name="images")

@app.get("/")
def health_check():
    return {"status": "Dungeon RPG running"}


@app.post("/new-game")
async def new_game(payload: dict):
    return generate_new_game(
        character_name=payload.get("character_name"),
        character_class=payload.get("character_class")
    )


@app.post("/action")
async def action(payload: dict):
    return take_action(
        game_id=payload.get("game_id"),
        action=payload.get("action")
    )


@app.get("/game/{game_id}")
async def get_game_state(game_id: str):
    game = get_game(game_id)
    story = get_story(game_id)
    return {"game": game, "story": story}


@app.get("/games")
async def list_games():
    return get_all_games()