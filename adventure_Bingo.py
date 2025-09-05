import streamlit as st
from utils.board import generate_board, load_prompts
from utils.storage import save_board_json, load_board_json

def main():
    st.title("Adventure Bingo")

    st.write("Welcome to Adventure Bingo! Generate your own bingo board of fun challenges.")

    # Let the user choose board size
    size = st.slider("Choose board size", min_value=3, max_value=6, value=3)
    # Value is the initial starting value, changeable from minimal to maximum

    # Load prompts
    prompts = load_prompts()

    # Generate a new board when button is clicked
    if st.button("Generate New Board"):
        st.session_state.board = generate_board(size=size, prompts=prompts)

    # If no board exists yet, create one as a placeholder
    if "board" not in st.session_state:
        st.session_state.board = generate_board(size=size, prompts=prompts)

    board = st.session_state.board

    st.subheader("Your Bingo Board")

    # Show the board in a grid with checkboxes
    tiles = board["tiles"]
    rows = [tiles[i * size:(i + 1) * size] for i in range(size)]
    completed = 0

    for r in rows:
        cols = st.columns(size)
        for i, tile in enumerate(r):
            with cols[i]:
                # Checkbox for each tile
                tile["completed"] = st.checkbox(tile["text"], value=tile["completed"], key=tile["id"])
                if tile["completed"]:
                    completed += 1

    # Show progress bar
    st.progress(completed / (size * size))
    st.caption(f"Completed: {completed}/{size * size}")

    # Save and load buttons
    st.subheader("Save or Load Your Board")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save Current Board"):
            path = save_board_json(board)
            st.success(f"Board saved to: {path}")

    with col2:
        uploaded = st.file_uploader("Load a board from JSON", type="json")
        if uploaded is not None:
            st.session_state.board = load_board_json(uploaded)
            st.success("Board loaded successfully!")
            st.write(st.session_state.board)

# Run the app
if __name__ == "__main__":
    main()