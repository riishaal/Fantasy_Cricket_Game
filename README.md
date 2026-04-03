# Fantasy Cricket Game

A Python desktop application built with **PyQt5** and **SQLite**, designed to let users create and manage their own fantasy cricket teams. Users can select real-world players while staying within a budget, save their custom-built teams to a database, and evaluate their scores based on actual match statistics.

## Features

- **Team Creation & Management**: Select exactly 11 players (Batsmen, Bowlers, All-rounders, and a maximum of one Wicket-keeper) to build your ultimate team.
- **Budget Restriction**: Keep your team's total points under 100 using virtual points assigned to each player.
- **Save & Open**: Save your squad to a local SQLite database (`fantasy_cricket.db`) and load previously created teams at any time.
- **Score Evaluation**: Evaluate your saved team's performance based on simulated match data (stored in the database) using realistic scoring rules for batting, bowling, and fielding.

## Requirements

- Python 3.x
- PyQt5

You can install the required packages using pip:

```bash
pip install PyQt5
```

## Setup & Running the Application

1. Clone this repository or download the project files.
2. If `fantasy_cricket.db` does not have tables, run `create_fantasy_cricket_db.py` to initialize the database tables and insert some dummy player data if needed.
3. Start the application by running the main entry script:

```bash
python main.py
```

## Usage Workflow

1. Select a category (BAT, BWL, AR, WK) from the top radio buttons.
2. Double-click a player name in the **Available Players** list to add them to your squad. (Watch your *Points Available*!)
3. To remove a player, double-click their name in the **Selected Players** list.
4. Once you have exactly 11 players, select **Manage Teams > Save Team** from the top menu, or use the `Save` button. Provide a team name to save it.
5. To evaluate a team's score in a match, click **Evaluate Score** or select it from the menu.

## Technologies Used
* **Python**: Core programming language.
* **PyQt5**: For building the Graphical User Interface (GUI).
* **SQLite3**: For the database to store players, match statistics, and custom user teams.
