import json
import random
import time
from pathlib import Path

# Function to load prompts from a JSON file
def load_prompts(path="data/prompts_default.json"):
    # Read the whole file as text (using UTF-8 so special characters can be used)
    with open(path, "r", encoding="utf-8") as file:
        prompts_data = json.load(file)
    return prompts_data

# Function to generate a bingo board
def generate_board(size=5, prompts=None):
    # Make sure we actually got prompts and enough of them
    if prompts is None:
        raise ValueError("No prompts were provided")
    if len(prompts) < size * size:
        raise ValueError("Not enough prompts to fill the bingo board")

    # Randomly choose enough prompts to fill the board
    chosen_prompts = random.sample(prompts, size * size)

    # Create tiles for each chosen prompt
    tiles = []
    for index, prompt in enumerate(chosen_prompts):
        tile = {
            "id": "T" + str(index).zfill(3),  # e.g. T000, T001, ...
            "text": prompt["text"],
            "category": prompt["category"],
            "completed": False,
        }
        tiles.append(tile)

    # Build the final board object
    board = {
        "board_id": str(int(time.time())) + "_" + str(size) + "x" + str(size),
        "size": size,
        "tiles": tiles
    }

    return board