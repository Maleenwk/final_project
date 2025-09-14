import json
import random
import time
import os

### prompts

# load default prompts from JSON file
def load_default_prompts(path="data/prompts_default.json"):
    # Read the whole file as text (using UTF-8 so special characters can be used)
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

# create custom prompts file if it doesn't exist
def ensure_custom_file(path="data/prompts_custom.json"):

    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    else:
        # if the file exists but is empty, initialize it to []
        if os.path.getsize(path) == 0:
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

def load_custom_prompts(path="data/prompts_custom.json"):
    # load custom prompts, return list of dicts
    ensure_custom_file(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def add_custom_prompt(text, category, path="data/prompts_custom.json"):
    # append new user prompt to prompts_custom.json
    if not text or not category:
        raise ValueError("Please provide text and category")

    ensure_custom_file(path)
    items = load_custom_prompts(path)

    # ID using timestamp
    new_id = "U" + str(int(time.time() * 1000))

    new_prompt = {
        "id": new_id,
        "text": text,
        "category": category
    }
    items.append(new_prompt)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    return new_prompt

def group_prompts_by_category(prompts):
# return grouped prompt dictionary
    grouped = {}
    for p in prompts:
        cat = p["category"]
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(p)
    return grouped

### board

# generate a bingo board
def generate_board(size=5, prompts=None):
    # make sure we actually got prompts and enough of them
    if prompts is None:
        raise ValueError("No prompts were provided")
    if len(prompts) < size * size:
        raise ValueError("Not enough prompts to fill the bingo board")

    # randomly choose enough prompts to fill board
    chosen_prompts = random.sample(prompts, size * size)

    # create tiles for each chosen prompt
    tiles = []
    for index, prompt in enumerate(chosen_prompts):
        tile = {
            "id": "T" + str(index).zfill(3),  # e.g. T000, T001, ...
            "text": prompt["text"],
            "category": prompt["category"],
            "completed": False,
        }
        tiles.append(tile)

    # build final board object
    board = {
        "board_id": str(int(time.time())) + "_" + str(size) + "x" + str(size),
        "size": size,
        "tiles": tiles
    }

    return board

### bingo detection

def detect_completed_lines(board):
    # detect all completed rows, columns, diagonals for an n×n board, returns a list of lines with each line being a list of (row, col) tuples
    n = board["size"]
    tiles = board["tiles"]
    completed = []

    def is_marked(r, c):
        i = r * n + c
        return bool(tiles[i].get("completed", False))

    # rows
    for r in range(n):
        row_done = True
        for c in range(n):
            if not is_marked(r, c):
                row_done = False
                break
        if row_done:
            line = []
            for c in range(n):
                line.append((r, c))
            completed.append(line)

    # columns
    for c in range(n):
        col_done = True
        for r in range(n):
            if not is_marked(r, c):
                col_done = False
                break
        if col_done:
            line = []
            for r in range(n):
                line.append((r, c))
            completed.append(line)

    # main diagonal
    diag_done = True
    for i in range(n):
        if not is_marked(i, i):
            diag_done = False
            break
    if diag_done:
        line = []
        for i in range(n):
            line.append((i, i))
        completed.append(line)

    # anti diagonal
    anti_done = True
    for i in range(n):
        if not is_marked(i, n - 1 - i):
            anti_done = False
            break
    if anti_done:
        line = []
        for i in range(n):
            line.append((i, n - 1 - i))
        completed.append(line)

    return completed


def line_key(line):
    # turn a line into a stable string key
    parts = []
    for (r, c) in line:
        parts.append(str(r) + "-" + str(c))
    return "|".join(parts)


def keys_for_lines(lines):
    # convert list of lines into list of string keys
    return [line_key(line) for line in lines]

### meme for bingo

def random_meme(media_folder="media"):
    # get all files that end with .gif
    if not os.path.isdir(media_folder):
        return None

    meme_files = []
    for f in os.listdir(media_folder):
        if f.lower().endswith(".gif"):
            meme_files.append(os.path.join(media_folder, f))

    if len(meme_files) == 0:
        return None

    # pick one at random
    return random.choice(meme_files)

### swapping

# replace tile at specific index, reset completed status
def swap_tile(board, index, new_prompt):
    tiles = board["tiles"]
    if index < 0 or index >= len(tiles):
        raise IndexError("Tile index out of range")
    tiles[index]["text"] = new_prompt["text"]
    tiles[index]["category"] = new_prompt["category"]
    tiles[index]["completed"] = False  # reset when swapping