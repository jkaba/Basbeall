# Expected batting average program extension
# This is a modified version of PredictedBatAvg.py where the program returns an estimated batting average and slugging percentage for a specified player.
# This program takes as user input a players first and last name
# The Neural Network trained on statcast data will return an expected batting average and slugging percentage for the player.
# Author = Jameel Kaba

# Import statements
# Must have PyBaseball and SciKit Learn libraries installed
from pybaseball import statcast
from pybaseball import statcast_batter
from pybaseball import playerid_lookup
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.utils import resample
import os
import pandas as pd

# Settings
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

# Method which finds the player's info in the playerTable
def getNumber(last, first):
    playerTable = playerid_lookup(last, first)
    playerTable = playerTable.loc[playerTable['mlb_played_last'].isin([2019])]
    playerTable.index = range(len(playerTable['mlb_played_last']))
    number = playerTable['key_mlbam']
    number = number[0]
    return number

# Method to get the batters statcast data
def getBatterData(number):
    data = statcast_batter('2019-03-01', '2019-10-31', number)
    data = data[['events', 'launch_speed', 'launch_angle']]
    return data


# Method to train the neural network on statcast data
def getTrainingData():
    # Range to get the data, larger range = longer time
    train = statcast('2019-3-20', '2019-10-31')
    train = train[['events', 'launch_speed', 'launch_angle']]
    train = train.dropna()
    train = pd.DataFrame(train, columns=['events', 'launch_speed', 'launch_angle'])
    
    outsList = ['field_out']
    desiredOutcome = ['single', 'double', 'triple', 'home_run', 'out']
    
    train['events'] = train['events'].replace(outsList, 'out')
    train = train.loc[train['events'].isin(desiredOutcome)]
    
    y_train = train['events']
    X_train = train.drop('events', axis=1)
    
    print('Beginning to train model, this may take a while.')
    
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    mlp = MLPClassifier(solver="sgd", hidden_layer_sizes=(40, 40, 40))
    mlp.fit(X_train, y_train)
    return mlp, scaler

# Method which predicts the players batting average and slugging percentage
def predictStats(model, player_data, model_scaler):
    test = player_data[['events', 'launch_speed', 'launch_angle']]
    test = pd.DataFrame(test, columns=['events', 'launch_speed', 'launch_angle'])
    
    # Types of outs
    outsList = ['field_out', 'double_play', 'field_error', 'fielders_choice',
                'fielders_choice_out', 'force_out',
                'grounded_into_double_play', 'triple_play']
    
    # Non-batted ball outs
    nonBBOuts = ['strikeout', 'strikeout_double_play']
    
    # Outcomes we are looking for
    desiredOutcome = ['single', 'double', 'triple', 'home_run', 'out']
    
    amountnBBOuts = len(test.loc[test['events'].isin(nonBBOuts)])
    test['events'] = test['events'].replace(outsList, 'out')
    test = test.loc[test['events'].isin(desiredOutcome)]
    test = test.dropna()
    test.index = range(len(test['events']))
    X_test = test.drop('events', axis=1)
    
    # Initialize variables
    hit = 0
    bases = 0
    ABs = len(X_test) + amountnBBOuts
    sumpBA = 0
    sumpSLG = 0
    
    # Loops to figure out stats
    for i in range(0, 4):
        for i in range(len(X_test)):
            test = X_test.take([i])
            test = model_scaler.transform(test)
            probability = model.predict(test)
            if(probability == 'single'):
                bases += 1
                hit += 1
            else:
                if(probability == 'double'):
                    bases += 2
                    hit += 1
                else:
                    if(probability == 'triple'):
                        bases += 3
                        hit += 1
                    else:
                        if(probability == 'home_run'):
                            bases += 4
                            hit += 1
                        else:
                            bases += 0
                            hit += 0
        predictedBA = hit/ABs
        predictedSLG = bases/ABs
        sumpBA += predictedBA
        sumpSLG += predictedSLG

    # Round the values for the stats
    avgpBA = round(sumpBA/10, 3)
    avgpSLG = round(sumpSLG/10, 3)
    
    # Getting the predicted values in shape for results
    predictedStats = [[avgpBA, avgpSLG]]
    predictedStats = pd.DataFrame(predictedStats, columns=['pBA', 'pSLG'])
    return predictedStats

# Main method which given a player will return a predicted batting average and slugging percentage
def main():
    nnModel, scale = getTrainingData()
    while(1 == 1):
        firstName = input('Enter Player\'s First Name: ')
        lastName = input('Enter Player\'s Last Name: ')
        nameString = firstName + ' ' + lastName
        player_data = getBatterData(getNumber(lastName, firstName))
        pStats = predictStats(nnModel, player_data, scale)
        pStats['Name'] = nameString
        cols = pStats.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        pStats = pStats[cols]
        print(pStats)

if __name__ == "__main__":
    main()
