# Pitcher Data program used to show the differences in a pitcher's pitches before and after a date range.
# Data is taken from statcast
# User inputs the pitchers first and last name, as well as a range of when to compare data
# Must have pybaseball and scikit learn installed
# Author = Jameel Kaba

# Import statements
from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup
import pandas as pd
import math as m
import matplotlib.pylab as plt

# Settings
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

# getNumber method used to locate a player's location in the data table
# Input: Players first and last name
# Output: Location of players data
def getNumber(last, first):
    playerTable = playerid_lookup(last, first)
    playerTable = playerTable.loc[playerTable['mlb_played_last'].isin([2019])]
    playerTable.index = range(len(playerTable['mlb_played_last']))
    number = playerTable['key_mlbam']
    number = number[0]
    return number

# dataGrab method, grabs data for player between start and end date
# Input: number = location of player data, start date, and end date
# Output: The player data
def dataGrab(number, start, end):
    data = statcast_pitcher(start_dt=start, end_dt=end,
                            player_id=number)
    data = data[['pitch_type', 'effective_speed', 'release_pos_x', 'plate_x',
                 'release_pos_z', 'plate_z', 'release_extension', 'zone',
                 'launch_speed', 'launch_angle']]
    data = pd.DataFrame(data, columns=['pitch_type', 'effective_speed',
                                       'release_pos_x', 'plate_x',
                                       'release_pos_z', 'plate_z',
                                       'release_extension', 'zone',
                                       'launch_speed', 'launch_angle'])
    data.index = range(len(data['pitch_type']))
    return data

# Release data per method 
def releaseData(before, after, end, begin):
    pitch_types = ['CH', 'CU', 'FC', 'FF', 'FO', 'FS', 'FT', 'GY', 'KC', 'KN',
                   'SC', 'SI', 'SL', 'EP']
    before = before.loc[before['pitch_type'].isin(pitch_types)]
    after = after.loc[after['pitch_type'].isin(pitch_types)]
    countsB = before['pitch_type'].value_counts(dropna=True)
    countsA = after['pitch_type'].value_counts(dropna=True)
    pitches = []
    for i in range(len(countsB)):
        is_pitch = before['pitch_type'] == countsB.index[i]
        pitchData = before[is_pitch]
        date = 'Before ' + end
        name = countsB.index[i]
        avgEffSpeed = round(pitchData['effective_speed'].mean(), 2)
        averageRelExt = round(pitchData['release_extension'].mean(), 2)
        averageRelX = round(pitchData['plate_x'].mean(), 2)
        averageRelZ = round(pitchData['plate_z'].mean(), 2)
        pitch = [date, name, avgEffSpeed, averageRelExt,
                 averageRelX, averageRelZ]
        pitches.append(pitch)
    for i in range(len(countsA)):
        is_pitch = after['pitch_type'] == countsA.index[i]
        pitchData = after[is_pitch]
        date = 'After ' + begin
        name = countsA.index[i]
        avgEffSpeed = round(pitchData['effective_speed'].mean(), 2)
        averageRelExt = round(pitchData['release_extension'].mean(), 2)
        averageRelX = round(pitchData['plate_x'].mean(), 2)
        averageRelZ = round(pitchData['plate_z'].mean(), 2)
        pitch = [date, name, avgEffSpeed, averageRelExt,
                 averageRelX, averageRelZ]
        pitches.append(pitch)
    pitches = pd.DataFrame(pitches, columns=['Before/After', 'Name',
                                             'Effective_Speed',
                                             'Release_Extension',
                                             'Horizontal_Break',
                                             'Vertical_Break'])
    pitches = pitches.sort_values(by=['Name', 'Before/After'], ascending=False)
    return pitches

# Plot Release data method
# This method plots the data into a strike zone, with bar charts to compare the pitch velocities
def plotReleaseData(before, after, end, begin):
    pitch_types = ['CH', 'CU', 'FC', 'FF', 'FO', 'FS', 'FT', 'GY', 'KC', 'KN',
                   'SC', 'SI', 'SL', 'EP']
    before = before.loc[before['pitch_type'].isin(pitch_types)]
    after = after.loc[after['pitch_type'].isin(pitch_types)]
    countsB = before['pitch_type'].value_counts(dropna=True)
    countsA = after['pitch_type'].value_counts(dropna=True)
    fig, axes = plt.subplots(nrows=2, ncols=1)
    fig.set_size_inches(8, 6, forward=True)
    fig.subplots_adjust(hspace=0.4)
    ax0, ax1 = axes.flatten()
    for i in range(len(countsB)):
        is_pitch = before['pitch_type'] == countsB.index[i]
        pitchData = before[is_pitch]
        name = countsB.index[i]
        avgEffSpeed = round(pitchData['effective_speed'].mean(), 2)
        averageRelX = round(pitchData['plate_x'].mean(), 2)
        averageRelZ = round(pitchData['plate_z'].mean(), 2)
        label = name + ' Before'
        ax0.scatter(averageRelX, averageRelZ, label=label, s=100)
        ax1.bar(label, avgEffSpeed)
        ax1.text(label, 70, s=round(avgEffSpeed, 1),
                 horizontalalignment='center', verticalalignment='center')
    for i in range(len(countsA)):
        is_pitch = after['pitch_type'] == countsA.index[i]
        pitchData = after[is_pitch]
        name = countsA.index[i]
        avgEffSpeed = round(pitchData['effective_speed'].mean(), 2)
        averageRelX = round(pitchData['plate_x'].mean(), 2)
        averageRelZ = round(pitchData['plate_z'].mean(), 2)
        label = name + ' After'
        ax0.scatter(averageRelX, averageRelZ, label=label, s=100)
        ax1.bar(label, avgEffSpeed)
        ax1.text(label, 70, s=round(avgEffSpeed, 1),
                 horizontalalignment='center', verticalalignment='center')
    ax0.plot([.79, .79, -.79, -.79, .79], [3.5, 1.5, 1.5, 3.5, 3.5],
             color='red', label='K Zone')
    ax0.plot([.94, .94, -.94, -.94, .94], [3.73, 1.27, 1.27, 3.73, 3.73],
             color='red', label='Outer Limits of K Zone', ls=':', alpha=0.5)
    ax0.legend(prop={'size': 7})
    ax0.set_title('Average Location at the Plate (Catcher\'s View)')
    ax0.set_xlim(-3, 3)
    ax0.set_ylim(1, 4)
    ax0.get_xaxis().set_visible(False)
    ax0.get_yaxis().set_visible(False)
    ax1.set_title('Average Effective Velocity per Pitch')
    ax1.set_ylim(67, 102)
    ax1.set_ylabel('Effective Velocity (mph)')


# bat_exit method
# This method is used to primarily clean up and organize data as most data points are null for launch speed/angle
def batExit(before, after, end, begin):
    before = before[['pitch_type', 'launch_speed', 'launch_angle']].dropna()
    after = after[['pitch_type', 'launch_speed', 'launch_angle']].dropna()
    countsB = before['pitch_type'].value_counts(dropna=True)
    countsA = after['pitch_type'].value_counts(dropna=True)
    pitches = []
    for i in range(len(countsB)):
        is_pitch = before['pitch_type'] == countsB.index[i]
        pitchData = before[is_pitch]
        pitchData = pitchData.dropna()
        dateB = 'Before ' + end
        name = countsB.index[i]
        lauchSpeedB = round(pitchData['launch_speed'].mean(), 2)
        launchAngleB = round(pitchData['launch_angle'].mean(), 2)
        pitch = [dateB, name, lauchSpeedB, launchAngleB]
        pitches.append(pitch)

    for i in range(len(countsA)):
        is_pitch = after['pitch_type'] == countsA.index[i]
        pitchData = after[is_pitch]
        dateB = 'After ' + begin
        name = countsA.index[i]
        launchSpeedA = round(pitchData['launch_speed'].mean(), 2)
        launchAngleA = round(pitchData['launch_angle'].mean(), 2)
        pitch = [dateB, name, launchSpeedA, launchAngleA]
        pitches.append(pitch)
    pitches = pd.DataFrame(pitches, columns=['Before/After', 'Name',
                                             'Launch_Speed', 'Launch_Angle'])
    return pitches

# Main method
def main():

    # Take Pitcher's First and Last name as input
    pFirst = input('Enter Pitcher\'s First Name: ')
    pLast = input('Enter Pitcher\'s Last Name: ')
    
    # Get the first Date Range
    Date1Start = input('Enter First Range Start Date (Example: 2019-3-1 for March 1st, 2019): ')
    Date1End = input('Enter First Rage End Date: ')
    
    # Get the Second Date Range
    Date2Start = input('Enter Second Range Start Date: ')
    Date2End = input('Enter Second Rage End Date: ')

    # Gather the data
    number = getNumber(pLast, pFirst)
    before = dataGrab(number, Date1Start, Date1End)
    after = dataGrab(number, Date2Start, Date2End)
    release_data = releaseData(before, after, Date1End, Date2Start)
    bat_data = batExit(before, after, Date1End, Date2Start)

    # Plot the Data
    plotReleaseData(before, after, Date1End, Date2Start)

    # Merge data to be displayed on terminal
    data = pd.merge(release_data, bat_data)
    
    # Print data and display plot
    print(data)
    plt.show()
    
    # Quit command
    input('Enter to Quit.')

if __name__ == "__main__":
    main()
