# Import libraries
from db_config import conn
from constants import *
from data_in import *
import helpers
import exploration
import classification

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

import time
import numpy as np


# Run the analysis
def main():
    print('Running Relief Pitching Analysis')

    # Get the data
    print('Ingesting Data')
    retrosheet_df = ingest_retrosheet_csv()
    batting_df = pd.read_sql(batting_query, conn)
    pitching_df = pd.read_sql(pitching_query, conn)

    # Increment to get a cumulative count of experience in the MLB
    years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    batter_experience_df = pd.DataFrame()
    pitcher_experience_df = pd.DataFrame()

    for i in years:
        print(i)
        bat_query = get_batting_experience_query(i)
        bat_temp_df = pd.read_sql(bat_query, conn)
        bat_temp_df['year'] = str(i)
        batter_experience_df = batter_experience_df.append(bat_temp_df)

        pit_query = get_pitching_experience_query(i)
        pit_temp_df = pd.read_sql(pit_query, conn)
        pit_temp_df['year'] = str(i)
        pitcher_experience_df = pitcher_experience_df.append(pit_temp_df)

    # Clean up retro sheet data
    print('Wrangling the data')
    retrosheet_df = helpers.create_date_variables(retrosheet_df)
    retrosheet_df = helpers.add_number_of_matchups(retrosheet_df)
    retrosheet_df = helpers.clean_baserunner_columns(retrosheet_df)
    retrosheet_df = helpers.calculate_the_score(retrosheet_df)
    retrosheet_df = helpers.add_home_vs_away(retrosheet_df)
    retrosheet_df = helpers.add_pitcher_number(retrosheet_df)
    retrosheet_df = helpers.clean_rbi_ct(retrosheet_df)

    batting_df = helpers.add_ops(batting_df)
    pitching_df = helpers.add_era(pitching_df)

    # Merge Retrosheet data
    print('Merging Data')
    df_list = [retrosheet_df, batting_df, pitching_df, batter_experience_df, pitcher_experience_df]

    for i in df_list:
        i['year'] = i['year'].astype('str')

    retrosheet_df = pd.merge(retrosheet_df, batting_df, how='left', on=['bat_id', 'year'])
    retrosheet_df = pd.merge(retrosheet_df, batter_experience_df, how='left', on=['bat_id', 'year'])
    retrosheet_df = pd.merge(retrosheet_df, pitching_df, how='left', on=['pit_id', 'year'])
    retrosheet_df = pd.merge(retrosheet_df, pitcher_experience_df, how='left', on=['pit_id', 'year'])

    # Exploration
    print('Exploring Data')

    retrosheet_exploration_df = retrosheet_df[['pit_years_of_experience','bat_years_of_experience', 'inn_ct',
                                               'outs_ct', 'month', 'day_of_week', 'year', 'balls_ct', 'strikes_ct',
                                               'base1_run_id', 'base2_run_id', 'base3_run_id', 'score_fielding',
                                               'score_hitting', 'rbi_ct', 'pitcher_number', 'home_team_id',
                                               'away_team_id', 'batter_arm', 'pitcher_arm', 'match_ups_counts']]

    retrosheet_exploration_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    retrosheet_exploration_df.replace(r'\s+', np.nan, regex=True, inplace=True)
    retrosheet_exploration_df.dropna(inplace=True)

    retrosheet_exploration_df.to_pickle('retrosheet_data_for_exploration.pkl')
    retrosheet_cols = list(retrosheet_exploration_df)

    for i in retrosheet_cols:
      exploration.calculate_failure_rates(retrosheet_df, i)

    # Final Set
    retrosheet_df = retrosheet_df[['rbi_ct', 'era', 'ops', 'pitcher_number', 'pit_years_of_experience',
                                   'bat_years_of_experience', 'inn_ct', 'outs_ct', 'balls_ct', 'strikes_ct',
                                   'score_fielding', 'score_hitting', 'match_ups_counts', 'month', 'day_of_week',
                                   'year', 'base1_run_id',  'base2_run_id', 'base3_run_id', 'home_team_id',
                                   'away_team_id', 'batter_arm', 'pitcher_arm']]

    # Drop nulls
    retrosheet_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    retrosheet_df.replace(r'\s+', np.nan, regex=True, inplace=True)
    retrosheet_df.dropna(inplace=True)

    # Save final data frame
    retrosheet_df.to_pickle('retrosheet_data_for_modeling.pkl')

    # Run Classifications
    # Prep data for machine learning
    X_train, X_test, Y_train, Y_test = classification.machine_learning_prep_classification(retrosheet_df, 'rbi_ct')

    # Create lists for iteration
    classifiers_list = [RandomForestClassifier(), ExtraTreesClassifier(), GradientBoostingClassifier(), LogisticRegression(), MLPClassifier()]
    classifier_model_names = ['random_forest', 'extra_trees', 'gradient_boosting', 'logistic_regression', 'multi_layer_perceptron']
    param_grid_lists = [tree_param_grid, tree_param_grid, gb_param_grid, logreg_param_grid, mlp_param_grid]

    # Train and evaluate the models
    for i, j, k in zip(classifier_model_names, classifiers_list, param_grid_lists):
        classification.run_classification(X_train, X_test, Y_train, Y_test, i, j, k)

    return None


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
