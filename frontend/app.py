import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Dungeon RPG", page_icon="🗡️", layout="wide")
st.title("🗡️ AI Dungeon RPG")

# Initialize session state
if "game_id" not in st.session_state:
    st.session_state.game_id = None
if "game" not in st.session_state:
    st.session_state.game = None
if "story" not in st.session_state:
    st.session_state.story = []
if "current_image" not in st.session_state:
    st.session_state.current_image = None

# --- Sidebar ---
with st.sidebar:
    st.header("⚔️ Character Setup")

    character_name = st.text_input("Character Name:", placeholder="Aragorn")
    character_class = st.selectbox(
        "Class:",
        ["Warrior", "Mage", "Rogue", "Ranger", "Paladin"]
    )

    if st.button("🎮 New Game", type="primary"):
        if character_name:
            with st.spinner("Creating your world..."):
                response = requests.post(
                    f"{BACKEND_URL}/new-game",
                    json={
                        "character_name": character_name,
                        "character_class": character_class
                    }
                )
                data = response.json()

            st.session_state.game_id = data["game_id"]
            st.session_state.game = data
            st.session_state.story = []
            st.session_state.current_image = data.get("current_image")
            st.rerun()
        else:
            st.warning("Enter a character name!")

    st.divider()

    # Load existing game
    st.header("📂 Continue Game")
    games = requests.get(f"{BACKEND_URL}/games").json()
    if games:
        game_options = {
            f"{g['character_name']} ({g['character_class']}) — {g['game_id']}": g['game_id']
            for g in games
        }
        selected = st.selectbox("Select game:", list(game_options.keys()))
        if st.button("Load Game"):
            game_id = game_options[selected]
            response = requests.get(f"{BACKEND_URL}/game/{game_id}")
            data = response.json()
            st.session_state.game_id = game_id
            st.session_state.game = data["game"]
            st.session_state.story = data["story"]
            st.session_state.current_image = data["game"]["current_image"]
            st.rerun()

# --- Main Game UI ---
if st.session_state.game_id:
    game = st.session_state.game

    # Character info
    st.caption(f"🧙 {game['character_name']} | {game['character_class']} | Game: {st.session_state.game_id}")

    col1, col2 = st.columns([1, 2])

    with col1:
        if st.session_state.current_image:
            st.image(f"http://localhost:8000/images/{st.session_state.current_image}.png", use_container_width=True)

    with col2:
        st.subheader("📖 Current Scene")
        st.write(game["current_scene"])

    st.divider()

    # Story history
    if st.session_state.story:
        st.subheader("📜 Story So Far")
        for msg in st.session_state.story:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(f"*{msg['content']}*")
            else:
                with st.chat_message("assistant"):
                    st.write(msg["content"])

    st.divider()

    # Action input
    st.subheader("⚡ What do you do?")
    action = st.chat_input("Describe your action...")

    if action:
        with st.spinner("The story continues..."):
            response = requests.post(
                f"{BACKEND_URL}/action",
                json={
                    "game_id": st.session_state.game_id,
                    "action": action
                },
                timeout=60
            )
            result = response.json()

        # Update session state
        st.session_state.story.extend([
            {"role": "user", "content": action},
            {"role": "assistant", "content": result.get("story_beat")}
        ])
        st.session_state.game["current_scene"] = result.get("story_beat")
        st.session_state.current_image = result.get("image_url")

        st.rerun()