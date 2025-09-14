import json
import os
import time

# Make sure the data folder exists (otherwise saving will break)
def ensure_data_folder(folder_name="data/user_boards"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Save a bingo board as a JSON file
def save_board(board, folder_name="data/user_boards"):
    ensure_data_folder(folder_name)

    # Create a unique filename using the current time
    timestamp = str(int(time.time()))
    filename = "board_" + timestamp + ".json"
    file_path = os.path.join(folder_name, filename)

    # Write the board data into the file
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(board, file, indent=2, ensure_ascii=False)

    return file_path

# Load a bingo board from an uploaded JSON file
def load_board(uploaded_file):
    # uploaded_file behaves like a file-like object, so we can read it directly
    board_data = json.load(uploaded_file)

    return board_data