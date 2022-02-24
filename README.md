# Baseball
This repo will be the home to Baseball projects which I have done.

AtBatSim.py
- An At Bat Simulator written in Python. Current settings are set to 100 at bat simulations, could change to ask for user requirments. Probabilities are completely random, and are not set to any particular hitter or pitcher. Probabilities can be tuned with the appropriate data to focus on a particular pitcher or hitter. 

HistoricTeams.R
- R Script, to take a look and compare teams throughout history. Plots include: correlation matrix, relationship between variables, parallel coordinate plots, K means Clustering, and hierarchical structure through a dendrogram

HomeRunScraper.py
- Python program which scrapes home run data from Fox Sports, calculates the mean standard deviation, and variance from year to year over a 20 year period. 

KBO_SwingMiss_Probability.ipynb
- This is a model built to determine the odds of a KBO pitcher getting a hitter to swing and miss at a fastball. This was originally a technical prompt for a data analyst position with a KBO team. 

MLB_Attendance.r
- This R program was used for an analysis in regards to MLB Attendance, and looks into potential factors which could affect attendance. 

MLOA_App.py
- Simple Web app made in Python Dash as part of an assessment for a position of Major League Operations Analyst. Each page contains a look at different topics. Topics include: Release Speed vs. Spin Rate; Spin Rate per Pitch; Event Occurrences by Pitch thrown by Pitcher; Event Occurances by balls-strikes count.

NoHitterVerlander.r
- R script that takes a look at Justin Verlander's 3rd career no hitter which was Sept. 1, 2019 against the Toronto Blue Jays

PitcherData.py
- This program is meant to be used as a tool to compare a pitcher's pitch data before and after a specified date. This program takes as user input a pitcher's first and last name, as well as two date ranges to compare data, and returns a plot of the pitcher's pitch data as well as a data table with info such as Speed, Release Extension, Break, Exit Velocity, and Launch Angle. 

PlayValidation.py
- A method which validates whether or not a transition from one game state to another can validly occur as a play. For this method, a "play" is the period from one instance when a pitcher has the ball and may legally pitch to either the next such instance or the end of a half-inning. 

Player swing probability.ipynb
- This model attempts to determine whether or not an MLB hitter will swing at a given pitch. model is trained using pitch-by-pitch data from StatCast and used the following features: pitch speed, pitch location, the velocity in the x,y,z, directions, the count the pitch was thrown in, the movement of the pitch in the x,z directions, and the pitch type of the previous pitch. 

PredictedBatAvg.py: 
- This is a Neural Network project in which given Exit Velocity and Launch Angles as User Inputs a Neural Network trained on StatCast data will produce the estimated batting average and slugging percentage.

PredictedPlayerStats.py
- This is an extension of the PredictedBatAvg.py program. A user inputs a player's first and last name to the program which the Neural Network trained on StatCast data will return an estimated batting average and slugging percentage based on this players StatCast data.

QualifyingOffer.R
- This was a task from an assessment for an R&D role. The program calculates the Qualifying Offer based on  user provided data, and returns the monetary value for the Qualifying Offer as well as a .csv containing the top 125 salaries.
