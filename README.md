# AI Dungeon RPG 🗡️

A production-inspired AI game with persistent world state, character classes, and AI-generated scene images. Every playthrough is unique.

## How It Works

    Character Setup → Pick name + class
           ↓
    LLM generates world + backstory + opening scene
           ↓
    Player types action
           ↓
    LLM continues story based on full history
           ↓
    Image generated for current scene
           ↓
    Saved to SQLite — continue anytime

## Key Concepts

**Persistent world state** — every action and story beat saved to SQLite. Player can close the browser and continue exactly where they left off.

**Full story memory** — entire conversation history passed to LLM every turn, maintaining perfect narrative consistency.

**Local image generation** — scene images generated locally using Stable Diffusion (runwayml/stable-diffusion-v1-5), no external API needed.

## Tech Stack

| Component | Free (This Project) | Production Equivalent |
|---|---|---|
| LLM | Groq llama-3.3-70b-versatile | Azure OpenAI GPT-4 / AWS Bedrock |
| Image Generation | Stable Diffusion (local) | DALL-E 3 / Stable Diffusion API |
| Persistent Memory | SQLite | Azure Cosmos DB / DynamoDB |
| UI | Streamlit | React enterprise portal |
| Backend | FastAPI | AWS Lambda / Azure Functions |

## Project Structure

    dungeon-rpg/
    ├── backend/
    │   ├── main.py          # FastAPI app + endpoints
    │   ├── generator.py     # World + character generation
    │   ├── story.py         # Story continuation engine
    │   ├── image.py         # Local Stable Diffusion image generation
    │   ├── database.py      # SQLite operations
    │   └── config.py        # Settings
    ├── frontend/
    │   └── app.py           # Streamlit UI
    └── requirements.txt

## Run Locally

### Prerequisites
- Python 3.10+
- Groq API key (free at [console.groq.com](https://console.groq.com))
- Stable Diffusion model cached locally (runwayml/stable-diffusion-v1-5)

### Setup
```bash
git clone https://github.com/lordrajesh/dungeon-rpg.git
cd dungeon-rpg
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

### Configure

GROQ_API_KEY=your_groq_api_key_here

### Download Image Model
```python
from diffusers import StableDiffusionPipeline
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
```

### Start
```bash
# Terminal 1
cd backend && uvicorn main:app --reload

# Terminal 2
cd frontend && streamlit run app.py
```

## Key Concepts Demonstrated
- **Persistent game state** — SQLite stores entire world + story history
- **Local image generation** — Stable Diffusion runs fully offline
- **Stateful LLM conversations** — full history passed every turn for consistency
- **Production mapping** — every component maps to enterprise equivalent