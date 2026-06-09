from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
from database import save_game, save_story_beat
from image import generate_image
import json
import uuid
import random

client = Groq(api_key=GROQ_API_KEY)


def generate_new_game(character_name: str, character_class: str) -> dict:
    """
    LLM generates:
    - Character backstory based on name + class
    - Unique world setting
    - Opening scene
    Then generates first scene image.
    """
    game_id = str(uuid.uuid4())[:8]

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{
            "role": "user",
            "content": f"""Create a fantasy RPG game setup. Random seed: {random.randint(1, 99999)}

Character name: {character_name}
Character class: {character_class}

Return ONLY valid JSON, no backticks, no explanation:
{{
    "character_backstory": "2-3 sentences about this character's origin and motivation",
    "world_setting": "2-3 sentences describing the world and its current state of danger",
    "opening_scene": "3-4 sentences describing where the character is and what they see. End with a choice or situation that demands action.",
    "image_prompt": "short visual description of the opening scene for image generation"
}}"""
        }],
        max_tokens=1000
    )

    content = response.choices[0].message.content.strip()
    content = content.replace("```json", "").replace("```", "").strip()
    data = json.loads(content)

    # Generate opening scene image
    image_url = generate_image(data["image_prompt"], f"{game_id}_opening")

    game = {
        "game_id": game_id,
        "character_name": character_name,
        "character_class": character_class,
        "character_backstory": data["character_backstory"],
        "world_setting": data["world_setting"],
        "current_scene": data["opening_scene"],
        "current_image": image_url
    }

    save_game(game)
    save_story_beat(game_id, "assistant", data["opening_scene"])

    return game