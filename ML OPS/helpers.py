# Import Statements
import pandas as pd
import pickle

# drop_duplicates function
# This function Drops Duplicates based on UID
def drop_duplicates(df):
    print('dropping duplicates')

    # Create UID
    df.drop_duplicates(inplace=True)
    df.reset_index(inplace=True, drop=True)

    df['year_id'] = df['year_id'].astype('str')
    df['games_played'] = df['games_played'].astype('str')

    df['uid'] = df['player_id'] + df['year_id']
    df['full_uid'] = df['player_id'] + df['year_id'] + df['games_played']
    df.drop_duplicates(subset='full_uid', keep='first', inplace=True)
    df['games_played'] = df['games_played'].astype('int')

    # Dataframe gets sorted with duplicates dropped
    df.sort_values(by=['player_id', 'year_id', 'games_played'], ascending=[False, False, False], inplace=True)
    df.drop_duplicates(subset='uid', keep='first', inplace=True)
    df.drop(['uid', 'full_uid'], axis=1, inplace=True)
    return df

# perform_cleaning function
# This function performs general cleaning
def perform_cleaning(df):
    print('performing general light cleaning')

    # Temas that changed names, can have data combined
    df['team_id'] = df['team_id'].str.replace('ANA', 'LAA').str.replace('FLO', 'MIA').str.replace('MON', 'WAS')

    # In the event a player has no salary, assume minimum
    # Because players can be paid less if they only play part season, we need to factor that
    # Does not count for inflation
    df['salary'].fillna(value=500000 * (df['games_played'] / 162), inplace=True)
    return df

# clean_award_variables function
# This function is used to create and clean datasets for awards (all_star, and silver slugger)
def clean_award_variables(main_df, awards_df, all_stars_df):
    print('cleaning awards variables')

    # Create a Dataset for each award
    silver_slugger_df = awards_df.loc[awards_df['award'] == 'Silver Slugger']
    silver_slugger_df.rename(columns={'award': 'silver_slugger'}, inplace=True)
    silver_slugger_df['silver_slugger'] = silver_slugger_df['silver_slugger'].str.replace('Silver Slugger', 'yes')
    all_stars_df['all_star'] = 'yes'

    # Merge the award dataset into the main dataset
    main_df['year_id'] = main_df['year_id'].astype('str')
    silver_slugger_df['year_id'] = silver_slugger_df['year_id'].astype('str')
    all_stars_df['year_id'] = all_stars_df['year_id'].astype('str')

    main_df = pd.merge(main_df, silver_slugger_df, how='left', on=['player_id', 'year_id'])
    main_df = pd.merge(main_df, all_stars_df, how='left', on=['player_id', 'year_id'])
    main_df['silver_slugger'].fillna(value='no', inplace=True)
    main_df['all_star'].fillna(value='no', inplace=True)
    return main_df

# create_target function
# This function is used to calculate the OPS
def create_target(df):
    print('calculating ops')

    # All variables should be numeric
    vars_list = ['hits', 'walks', 'hit_by_pitch', 'at_bats', 'sacrifice_flies', 'doubles', 'triples', 'home_runs', 'intentional_walks']

    for variable in vars_list:
        df[variable] = pd.to_numeric(df[variable], errors='coerce')

    # Calculate OBP
    df['obp'] = (df['hits'] + df['walks'] + df['hit_by_pitch']) / (df['at_bats'] + df['walks'] + df['hit_by_pitch'] + df['sacrifice_flies'])

    df['obp'].fillna(value=0, inplace=True)

    # Calculate SLG
    df['slg'] = (df['hits'] - (df['doubles'] + df['triples'] + df['home_runs']) + df['doubles'] * 2 + df['triples'] * 3 + df['home_runs'] * 4) / df['at_bats']

    df['slg'].fillna(value=0, inplace=True)

    # Calculate OPS
    df['ops'] = df['obp'] + df['slg']
    df['ops'].fillna(value=0, inplace=True)

    # Create target
    df.sort_values(['player_id', 'year_id'], ascending=[True, True], inplace=True)
    df['target'] = df.groupby('player_id')['ops'].shift(-1)
    df.dropna(subset=['target'], inplace=True)
    return df

# drop_columns function
# This function is used to drop columns which aren't needed
def drop_columns(df):
    print('dropping columns')

    # Save a copy of the data
    df['name'] = df['nameFirst'] + ' ' + df['nameLast']
    df.to_pickle('full_data_frame.pkl')

    # Drop columns which are not needed for modeling
    df.drop(['nameFirst', 'nameLast', 'name'], axis=1, inplace=True)
    return df

# machine_learning_prep function
# This function is used to prep data for machine learning
def machine_learning_prep(df, dependent_variable):
    print('preparing data for machine learning')

    df = pd.get_dummies(df)

    # 2017 and 2018 are used for training set
    testing_list = [2017, 2018]
    training_df = df.loc[~df['year_id'].isin(testing_list)]
    testing_df = df.loc[df['year_id'].isin(testing_list)]

    df.drop('year_id', axis=1, inplace=True)
    training_df.drop('year_id', axis=1, inplace=True)
    testing_df.drop('year_id', axis=1, inplace=True)

    y_train = training_df[dependent_variable]
    X_train = training_df.drop(dependent_variable, axis=1)

    y_test = testing_df[dependent_variable]
    X_test = testing_df.drop(dependent_variable, axis=1)

    return X_train, X_test, y_train, y_test

# create_lagged_variables function
# This function creates lagged variables
def create_lagged_variables(df):

    # Create the lags
    vars_list = ['games_played', 'at_bats', 'run_scored', 'hits', 'doubles', 'triples', 'home_runs', 'rbi', 'stolen_bases', 'walks', 'strikeouts', 'obp', 'slg', 'ops', 'intentional_walks'] * 5

    for variable in vars_list:
        df[variable] = pd.to_numeric(df[variable], errors='coerce')

    lags_list = [1] * 15 + [2] * 15 + [3] * 15 + [4] * 15 + [5] * 15
    names_list = ['lag_1'] * 15 + ['lag_2'] * 15 + ['lag_3'] * 15 + ['lag_4'] * 15 + ['lag_5'] * 15

    def create_lag(variable, lag, new_name):
        df['temp_name'] = df.groupby('player_id')[variable].shift(lag)
        df.rename(columns={'temp_name': variable + '_' + new_name}, inplace=True)
        df[variable + '_' + new_name].fillna(value=0, inplace=True)
        return df

    for var, lag, name in zip(vars_list, lags_list, names_list):
        create_lag(var, lag, name)

    # 1995-1999 are deleted, those years are only used for lag variables
    df['year_id'] = df['year_id'].astype('int')
    delete_list = [1995, 1996, 1997, 1998, 1999]
    df = df.loc[~df['year_id'].isin(delete_list)]

    df.drop('player_id', axis=1, inplace=True)
    return df

# back_test_the_model function
# This function is used to predict on all data for back-testing purposes
def back_test_the_model(model):
    print('back testing the model')

    # Read in the data
    df = pd.read_pickle('players_df_pre_processed.pkl')
    actual = df['target']
    actual.columns = ['actual']
    df.drop('target', axis=1, inplace=True)

    # Run the data through the prediction pipeline
    pipe = pickle.load(open(model, 'rb'))
    predictions = pd.DataFrame(pipe.predict(df))
    predictions.columns = ['predicted']

    combined_df = pd.DataFrame(pd.concat([df, actual, predictions], axis=1))
    return combined_df
