# Expected batting average program
# This program takes as user input exit velocity and launch angle
# The Neural Network trained on statcast data will return an expected batting average and slugging percentage
# Have to send as a txt, please change to .py
# Author = Jameel Kaba

# Import statements
# Must have PyBaseball and SciKit Learn libraries installed
from pybaseball import statcast
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import math as m
import matplotlib.pylab as plt
import matplotlib as mpl
import os
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from matplotlib import cm
plt.style.use('bmh')

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

# Function to get the training data
def getTrainingData():
    # Range to get the data from, larger range = longer time
    train = statcast('2019-3-20', '2019-10-31')
    train = train[['events', 'launch_speed', 'launch_angle']]
    train = train.dropna()
    train = pd.DataFrame(train, columns=['events', 'launch_speed', 'launch_angle'])
    outsList = ['field_out']
    desiredOutcome = ['out', 'single', 'double', 'triple', 'home_run']
    train['events'] = train['events'].replace(outsList, 'out')
    train = train.loc[train['events'].isin(desiredOutcome)]
    train.index = range(len(train['events']))
    y_train = train['events']
    X_train = train.drop('events', axis=1)
    print('Beginning to train model, this may take a while.')
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    mlp = MLPClassifier(solver="sgd", hidden_layer_sizes=(40, 40, 40))
    mlp.fit(X_train, y_train)
    return mlp, scaler


# Function to calculate the predicted stats
def xpredictStats(model, launch_speed, launch_angle, model_scaler):
    test = [[launch_speed, launch_angle]]
    test = pd.DataFrame(test, columns=['launch_speed', 'launch_angle'])
    test = model_scaler.transform(test)
    probabilities = model.predict_proba(test)
    xpBA = (probabilities[0][0] + probabilities[0][1] +
            probabilities[0][3] + probabilities[0][4])
    xpSLG = (probabilities[0][3] + 2 * probabilities[0][0] +
             3 * probabilities[0][4] + 4 * probabilities[0][1])
    xpBA = round(xpBA, 3)
    xpSLG = round(xpSLG, 3)
    xpredictedStats = [[launch_speed, launch_angle, xpBA, xpSLG]]
    xpredictedStats = pd.DataFrame(xpredictedStats, columns=['exit_velocity',
                                                             'launch_angle',
                                                             'xpBA', 'xpSLG'])
    return xpredictedStats

# Main function
def main():
    nnModel, scale = getTrainingData()
    while(1 == 1):
        launchspeed = float(input('Enter Launch Speed (mph): '))
        launchangle = float(input('Enter Launch Angle (deg.): '))
        xpStats = xpredictStats(nnModel, launchspeed, launchangle, scale)
        print(xpStats)
    
if __name__ == "__main__":
    main()
