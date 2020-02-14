# ML Player Decline

This project uses Machine Learning to predict if an offensive player is before or after their peak.

A players peak is defined as the year in which they aquired their highest OPS rating. 

The following variables were used in regards to training the model:
- Past Seasons OPS
- Games Played in Career
- Past Season Salary
- Position
- Age
- Decade
- Weight
- Height
- Batting Hand
- Throwing Hand

The training data consists of all players who debuted after 2000 and those who have retired.
Players had to have played 80 games in order to be considered for the model.

Files:
sql_queries.py - Query files for local instance of the Lahman Database

constants.py - Constant Variables referenced in other scripts 

helpers.py - Functions for cleaning and preprocessing 

descriptive_exploration.py - Function for creating descriptive summaries of data segments

classification.py - File containing functions for Machine Learning 

classification_voting.py - Grouping of multiple models

main.py - Main Method/Function
