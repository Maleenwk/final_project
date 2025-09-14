import streamlit as st
from utils.board import generate_board, load_default_prompts, load_custom_prompts,detect_completed_lines, keys_for_lines, random_meme, add_custom_prompt, group_prompts_by_category, swap_tile
from utils.storage import save_board, load_board

def main():
    st.title("Adventure Bingo")
    st.write("Welcome to Adventure Bingo! Generate your own bingo board of fun challenges.")

    # slider to choose board size
    size = st.slider("Choose board size", min_value=3, max_value=7, value=3)
    # value is the initial starting value, changeable from minimal to maximum

    # load prompts
    prompts_all = load_default_prompts() + load_custom_prompts()

    # add user prompts
    with st.expander("Add your own prompts"):
        with st.form("add_prompt_form", clear_on_submit=True):
            activity = st.text_input("Activity *")
            category = st.text_input("Category *")
            submit = st.form_submit_button("Add prompt")
        if submit:
            if not activity.strip() or not category.strip():
                st.error("Please fill in both Activity and Category.")
            else:
                saved = add_custom_prompt(activity.strip(), category.strip())
                st.success(f"Added: {saved['text']}  (ID: {saved['id']}, Category: {saved['category']})")
                # refresh prompts list for immediate availability
                prompts_all = load_default_prompts() + load_custom_prompts()

    # popup sidebar
    with st.sidebar:
        st.header("Browse all prompts")

        # edit mode toggle
        if "edit_mode" not in st.session_state:
            st.session_state.edit_mode = False
        st.session_state.edit_mode = st.toggle(
            "Edit Mode (click a tile to swap)",
            value=st.session_state.edit_mode
        )

        # show currently selected prompt
        if st.session_state.get("selected_prompt"):
            st.caption(f"Selected: **{st.session_state.selected_prompt['text']}**")

        filter_text = st.text_input("Filter by text", "")
        grouped = group_prompts_by_category(prompts_all)

        # show categories in alphabetical order
        for cat in sorted(grouped.keys(), key=lambda x: x.lower()):
            items = grouped[cat]

            # text filter on the prompt text
            if filter_text.strip():
                ft = filter_text.strip().lower()
                items = [p for p in items if ft in p["text"].lower()]
                if not items:
                    continue

            with st.expander(f"{cat} ({len(items)})", expanded=False):
                for p in items:
                    # click prompt to select for swapping
                    if st.button(p["text"], key=f"pick_{p['id']}", use_container_width=True):
                        st.session_state.selected_prompt = p

    # generate new board
    if st.button("Generate Random Board"):
        st.session_state.board = generate_board(size=size, prompts=prompts_all)
        # reset celebration memory and edit mode
        st.session_state.celebrated_lines = []
        st.session_state.selected_prompt = None
        st.session_state.edit_mode = False

    # blank space until clicking generate board
    if "board" not in st.session_state:
        st.info("Click **Generate Random Board** to create a board.")
        return

    board = st.session_state.board

    st.subheader("Your Bingo Board")

    # show board in grid with checkboxes
    n = board["size"]
    tiles = board["tiles"]
    rows = [tiles[i * n:(i + 1) * n] for i in range(n)]
    completed = 0

    for r_i, r in enumerate(rows):
        cols = st.columns(size)
        for c_i, tile in enumerate(r):
            idx = r_i * size + c_i  # flat index for this tile
            with cols[c_i]:
                st.caption(tile["category"])
                if st.session_state.get("edit_mode", False) and st.session_state.get("selected_prompt"):
                    # edit mode
                    if st.button(tile["text"], key=f"swap_{tile['id']}", use_container_width=True):
                        swap_tile(board, idx, st.session_state.selected_prompt)
                        st.session_state.selected_prompt = None

                else:
                    # play mode
                    tile["completed"] = st.checkbox(tile["text"], value=tile["completed"], key=tile["id"])
                    if tile["completed"]:
                        completed += 1

    # run bingo detection after potential checkbox change
    completed_lines = detect_completed_lines(board)
    completed_keys = keys_for_lines(completed_lines)

    if "celebrated_lines" not in st.session_state:
        st.session_state.celebrated_lines = []

    new_keys = [k for k in completed_keys if k not in st.session_state.celebrated_lines]
    if len(new_keys) > 0:
        meme_path = random_meme("media")
        st.image(meme_path, caption="BINGO!!", use_container_width=True)
        st.session_state.celebrated_lines += new_keys

    # progress bar
    st.progress(completed / (n * n))
    st.caption(f"Completed: {completed}/{n * n}")

    # save and load
    st.subheader("Save or Load Your Board")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save Current Board"):
            path = save_board(board)
            st.success(f"Board saved to: {path}")

    with col2:
        uploaded = st.file_uploader("Load a board from JSON", type="json")
        if uploaded is not None:
            st.session_state.board = load_board(uploaded)
            st.success("Board loaded successfully!")
            st.write(st.session_state.board)
            # reset celebration for loaded state
            st.session_state.celebrated_lines = []

# run the app
if __name__ == "__main__":
    main()