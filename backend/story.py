from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
from database import get_game, get_story, save_story_beat, update_scene
from image import generate_image

client = Groq(api_key=GROQ_API_KEY)


def take_action(game_id: str, action: str) -> dict:
    """
    Player takes an action:
    1. Load game state + full story history
    2. LLM continues story
    3. Generate one scene image
    4. Save to SQLite
    """
    game = get_game(game_id)
    if not game:
        return {"error": "Game not found"}

    history = get_story(game_id)

    system_prompt = f"""You are a master storyteller running a fantasy RPG.

World: {game['world_setting']}
Character: {game['character_name']}, a {game['character_class']}
Backstory: {game['character_backstory']}

Rules:
- Continue the story based on the player's action
- Be descriptive and immersive — 3-5 sentences
- Always end with a new situation or choice that demands a response
- Remember everything that happened in the story so far
- Make consequences feel real and meaningful
- Never break the fourth wall"""

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": action})

    # Get story continuation
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        max_tokens=400
    )
    story_beat = response.choices[0].message.content.strip()

    # Generate image prompt from story beat
    image_prompt_response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{
            "role": "user",
            "content": f"""Extract a short visual scene description for image generation from this story beat:
{story_beat}

Return ONLY a short image prompt, 10-15 words, no explanation."""
        }],
        max_tokens=50
    )
    image_prompt = image_prompt_response.choices[0].message.content.strip()

    # Generate scene image
    image_url = generate_image(image_prompt, f"{game_id}_{len(history)}")

    # Save to DB
    save_story_beat(game_id, "user", action)
    save_story_beat(game_id, "assistant", story_beat)
    update_scene(game_id, story_beat, image_url)

    return {
        "story_beat": story_beat,
        "image_url": image_url
    }