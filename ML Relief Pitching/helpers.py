import pandas as pd
import calendar
from sklearn.base import BaseEstimator, TransformerMixin

# subset_data function
# This Function is used to clean up the Retrosheet data
# This function breaks data to plays in the 6th inning or later when score is within 3 runs
# Functions to clean Retrosheet data
def subset_data(df):
    df['score_absolute_value'] = abs(df['away_score_ct'] - df['home_score_ct'])
    df = df[(df['score_absolute_value'] >= 3) & (df['inn_ct'] >= 6)]
    return df

# find_when_pitcher_switch function
# This function is used to create columns to help identify plays when a new pitcher comes in
def find_when_pitchers_switch(df):

    df['previous_pitcher'] = df['pit_id'].shift(1)
    df['previous_fielding_team'] = df['fld_team_id'].shift(1)

    for index, row in df.iterrows():
        if row['previous_pitcher'] == row['pit_id']:
            row['same_pitcher'] = 'yes'
        else:
            row['same_pitcher'] = 'no'

        if row['previous_fielding_team'] == row['fld_team_id']:
            row['same_team'] = 'yes'
        else:
            row['same_team'] = 'no'

    return df

# create_data_variables function
# This function creates variables for date, year, and day of the week
def create_date_variables(df):

    df['date'] = df['game_id'].str[3:11]

    df['year'] = df['game_id'].str[3:7]
    df['year'] = df['year'].astype('str')

    df['month'] = df['date'].str[4:6]
    month_dict = {'03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug', '09': 'Sep',
                  '10': 'Oct'}
    df['month'] = df['month'].map(month_dict)

    weekdays = []
    df['date'] = pd.to_datetime(df['date'])

    for i in df['date']:
        weekdays.append(calendar.day_name[i.weekday()])
    weekdays = pd.DataFrame(weekdays)
    weekdays.columns = ['day_of_week']
    df = pd.merge(df, weekdays, how='inner', left_index=True, right_index=True)
    return df

#  add_the_count function
# This function adds to the count, whether its a ball or strike
def add_the_count(df):
    df['balls_ct'] = df['balls_ct'].astype('str')
    df['strikes_ct'] = df['strikes_ct'].astype('str')
    df['count'] = df['balls_ct'] + '-' + df['strikes_ct']
    return df

# add_pitcher_hitter_matchup function
# This function adds up the match-up based on batter and pitcher arms
def add_pitcher_hitter_matchup(df):
    df['matchup'] = df['pit_hand_cd'] + df['bat_hand_cd']
    return df

# clean_baserunner_columns function
# This functions cleans baserunner data so that it's easy to identify when and where runners
#   are located for any given play
def clean_baserunner_columns(df):

    def clean_label(df, column):
        df[column].fillna(value='no', inplace=True)

        def map_label(row):
            if row[column] == 'no':
                return 'no'
            else:
                return 'yes'

        df[column] = df.apply(lambda row: map_label(row), axis=1)
        return df

    df = clean_label(df, 'base1_run_id')
    df = clean_label(df, 'base2_run_id')
    df = clean_label(df, 'base3_run_id')
    return df

# calculate_the_score function
# This function creates columns to keep score for both teams in a game
def calculate_the_score(df):

    df['bat_home_id'] = df['bat_home_id'].astype('str')

    if df['bat_home_id'].any() == '0':
        df['score_fielding'] = df['home_score_ct']
        df['score_hitting'] = df['away_score_ct']

    elif df['bat_home_id'].any() == '1':
        df['score_fielding'] = df['away_score_ct']
        df['score_hitting'] = df['home_score_ct']

    return df

# add_home_vs_away function
# This function adds a home v. road classification for the team fielding
#       When bat_home_id = 0, home team is on the field
def add_home_vs_away(df):
    
    df['home_vs_away'] = 'away'

    for index, row in df.iterrows():
        if row['bat_home_id'] == 0:
            row['home_vs_away'] = 'home'

    return df

# add_pitcher_number function
# This function adds the order in which a pitcher appeared in a game
def add_pitcher_number(df):

    pitcher_order = df[['game_id', 'pit_id', 'bat_home_id']]
    pitcher_order['uid'] = df['game_id'] + df['pit_id'] + df['bat_home_id']
    pitcher_order.drop_duplicates(subset='uid', keep='first', inplace=True)
    pitcher_order.drop('uid', 1, inplace=True)

    pitcher_order['uid'] = pitcher_order['game_id'] + pitcher_order['bat_home_id']
    pitcher_order.reset_index(inplace=True)
    pitcher_order.drop('index', 1, inplace=True)
    pitcher_order['pitcher_number'] = pitcher_order.groupby('uid').cumcount() + 1
    df = pd.merge(df, pitcher_order, how='left', on=['game_id', 'pit_id'])
    return df

# add_number_of_matchups function
# This function adds to the number of matchups between pitcher and hitter during the year
def add_number_of_matchups(df):
   
    df['match_up'] = df['bat_id'] + '_' + df['pit_id'] + '_' + df['year']
    df['match_ups_counts'] = df.groupby('match_up').cumcount() + 1
    df['match_ups_counts'].fillna(value=0, inplace=True)
    df.drop('match_up', 1, inplace=True)
    return df

# clean_rbi_ct function
# This function is used to clean the rbi count to help identify plays where a run scored
def clean_rbi_ct(df):

    df['rbi_ct'].fillna(value=0, inplace=True)

    def map_label(row):
        if row['rbi_ct'] == 0:
            return 0
        else:
            return 1

    df['rbi_ct'] = df.apply(lambda row: map_label(row), axis=1)
    return df

# add_ops function
# This function calculates OPS by player and by season
def add_ops(df):

    df['obp'] = (df['H'] + df['BB'] + df['HBP']) / (df['AB'] + df['BB'] + df['HBP'] + df['SF'])
    df['slg'] = ((df['H'] - (df['2B'] + df['3B'] + df['HR']) + df['2B'] * 2 + df['3B'] * 3 + df['HR'] * 4)) / df['AB']
    df['ops'] = df['obp'] + df['slg']
    return df

# add_era function
# This function calculates ERA by pitcher and by season
def add_era(df):
    df['era'] = (df['earned_runs'] / df['innings_pitched']) * 9
    return df

# TimeAttributesAdder function
# This custom transformer is used to see if adding dates help the model
class TimeAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_time_variables = 'Both'):
        self.add_time_variables = add_time_variables

    def fit(self, X, Y=None):
        return self

    def transform(self, X, Y=None):
        if self.add_time_variables == 'Only_Month':
            X.drop(list(X.filter(regex='day_of_week_')), axis=1, inplace=True)
            return X
        elif self.add_time_variables == 'Only_Day_of_Week':
            X.drop(list(X.filter(regex='month_')), axis=1, inplace=True)
        else:
            return X
