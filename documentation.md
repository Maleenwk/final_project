# Development of Adventure Bingo

## Final Project Idea
This Project is very personal to me because the Adventure Bingo idea is something my friends and I came up with while on vacation just after New Year's. 
We all wanted to set Goals for ourselves for the upcoming year and keep track of what we achieved. So we wrote them down on a square piece of paper in the form of a Bingo card. 
Over the course of the year, these cards have become damaged or lost, making it difficult to keep track of our achievements. 
This is the reason why I wanted to use my Final Project to create a digital version of our Adventure Bingo so that we can use it to write down our adventures for the upcoming year and have them saved on our devices.

## Intermediate Project Presentation

[Project Presentation Bingo.pdf](https://github.com/user-attachments/files/22170390/Project.Presentation.Bingo.pdf)

## MVP Scope

Having a minimum viable project scope will help me set my priorities for this project and filter my ideas into either essential for the functionality of my project or cool add-ons to work on if I have the time.

>
	Must-have (core features)
    - A bingo board (5x5 grid) is generated with random challenges.
    - Challenges come from a JSON file (seed prompts).
    - User can check off tiles.
    - Progress is tracked during the session (st.session_state) or saved to JSON.
    - User can reset the board to get new challenges.

>
 	Nice-to-have (stretch features)
    - Add your own custom challenges.
    - Save your own custom challenges.
    - Filter/select categories (e.g., “active” only).
    - drag and drop challenges into tiles.
    - Save/load multiple boards.
    - Aesthetic UI emojis, color changes when completing tiles, big cross over finished tiles.
    - A web-deployed app with authentication.
    - Multiplayer/social features.
    - Leaderboards or achievement badges.
    - Friend challenges (send a board to someone).

## Project Structure

My project structure is mostly copied from the sample projects, although I did make some adjustments to fit my specific project better. 
First of all, I decided to work with a two-file system for my dependencies, because the requirements.txt file that was created after installing streamlit, streamlit-extras, and pandas was very big and unclear. 
I asked ChatGPT whether all of these downloads from the requirements.txt file were necessary and how to structure it better so that the user knows what libraries are used in this project. 
ChatGPT introduced me to the two-file documentation of my dependencies. 
It also helped me set them up correctly, so that I now only need to put my library into requirements.in and let it automatically install all dependencies of that library and update my requirements.txt.
I also decided to split my project code into different helper functions, saved into the utils directory, and save static and user data in a separate directory.

>
	final_project/                     # final project repository
        adventure_Bingo.py             # main entry point (streamlit app)
        data/prompts_default.json      # storage of static data (seed prompts)
        data/user_data/                # storage of user data (bingo Boards)
        board_1234.json
        utils/board.py                 # helper function (bingo board logic)
        utils/storage.py               # helper function (data storage)
        media/                         # non-code assets    
        .gitignore                     # git commit exclusions
        LISCENSE                       # project liscencing
        README.md                      # project installation and usage instructions
        documentation.md               # documentation of development progress
        requirements.in                # direct dependencies, a two file worklfow creates a more clear management of external libraries
        requirements.txt               # full lock requirements file

## Structure & Categorization of Seed Prompts

When writing down my seed prompts, I decided on 6 different categories I wanted to create prompts for: 
Social
Wellbeing
Active
Lifetime
Creativity
Everyday Adventures.

At first I wrote my prompts out in the form of a nested directory organized by category

>
    {
        "Connect": [
        "Call a friend",
        "Invite a neighbor for coffee"
        ],
        "Dreams": [
        "Plan your next travel adventure",
        "Write down your 5-year goals"
        ]
    }


but I realized soon after that a Flat list with IDs for all prompts and category fields is the better sturcture for my seed prompts.

>
    [
        {"id": "A001", "text": "Try a new café in town", "category": "Connect"},
        {"id": "A002", "text": "Call a friend you haven’t spoken to in a while", "category": "Connect"},
        {"id": "B001", "text": "Plan your 5-year goals", "category": "Dreams"}
    ]

because I can still easily filter these prompts by category, it makes it easier to pick random prompts across multiple categories, and it will be easier to extend them with extra fields later (e.g. timespan, points,...).
The unique IDs every prompt has also makes it easier to track what prompts a user has completed later on.

## Basic Board Functions

At the start, I created the core functions needed for the bingo game:

>
	•	load_prompts() → loads the seed prompts from prompts_default.json.
	•	generate_board() → randomly creates a bingo board with tiles from the prompts.
	•	save_board_json() and load_board_json() → allow saving a generated board to a file and reloading it later.
	•	load_board_json() → loads a previously saved board back into the app.

These functions formed the foundation of the app, letting me generate and store boards before building the interactive UI with Streamlit.

While creating my main app, I had to import my helper functions and had to google how to create pathways between folders.
(not from board import generate_board, but  from utils.board import generate_board)
I also learned about including UTF-8 so special characters can be used in my app through trial and error.

## Saving Process

I set up a saving process so each generated board is stored as a JSON file. 

Along the way, I ran into problems re-uploading saved boards (wrong encoding and path handling) and had to adjust my functions. 
<img width="828" height="732" alt="Screenshot 2025-09-01 at 13 16 11" src="https://github.com/user-attachments/assets/732853c5-3777-4d41-be51-6cbaeb85c2f6" />

Another issue was the saved boards ending up in the data/ folder, which I don’t want to commit to Git. 
I fixed this by adding and saving the boards to data/user_data/ directory. Then I added this pathway to my .gitignore, so boards are stored locally but not pushed to the repository.

To avoid overwriting old boards, I created unique filenames by adding the current time as a timestamp to each saved file.
This means every saved board will have a different filename (e.g., board_1693948291.json). 
Even if multiple boards are saved in the same folder, each will be stored separately thanks to the unique timestamp.
