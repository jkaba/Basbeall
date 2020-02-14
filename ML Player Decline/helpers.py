import pandas as pd


def clean_database_input(df):

    # If a player played in both leagues, then combine rows for those years
    df_al = df.loc[df['league_id'] == 'AL']
    df_nl = df.loc[df['league_id'] == 'NL']
    df_merged = pd.merge(df_al, df_nl, how='inner', on=['player_id', 'year_id'])
    df_merged.columns = df_merged.columns.str.replace("_x", "")

    for column in ['games_played', 'at_bats', 'hits', 'doubles', 'triples', 'home_runs', 'walks', 'intentional_walks', 'sacrifice_flies', 'hit_by_pitch']:
        df_merged[column] = df_merged[column + '_y'] + df_merged[column]

    df_merged['salary'] = (df_merged['salary'] + df_merged['salary_y']) / 2
    df_merged.reset_index(inplace=True)
    index_list = df_merged['index'].tolist()
    df = df.drop(df.index[index_list])
    df = pd.concat([df, df_merged])
    df.drop_duplicates(subset=['player_id', 'year_id'], inplace=True)

    # Find decade
    df['year_id'] = df['year_id'].astype('str')
    df['decade'] = df['year_id'].str[0:3]
    df['year_id'] = df['year_id'].astype('int')

    # Find total games played
    df.sort_values(['player_id', 'year_id'], ascending=[True, True], inplace=True)
    df['cumulative_games'] = df.groupby('player_id')['games_played'].transform(pd.Series.cumsum)
    return df


def create_target(df):
    vars_list = ['hits', 'walks', 'hit_by_pitch', 'at_bats', 'sacrifice_flies', 'doubles', 'triples', 'home_runs', 'intentional_walks']

    for variable in vars_list:
        df[variable] = pd.to_numeric(df[variable], errors='coerce')

    df['obp'] = (df['hits'] + df['walks'] + df['hit_by_pitch']) / (df['at_bats'] + df['walks'] + df['hit_by_pitch'] + df['sacrifice_flies'])

    df['slg'] = (df['hits'] - (df['doubles'] + df['triples'] + df['home_runs']) + df['doubles'] * 2 + df['triples'] * 3 + df['home_runs'] * 4) / df['at_bats']

    df['slg'].fillna(value=0, inplace=True)
    df['obp'].fillna(value=0, inplace=True)

    df['ops'] = df['obp'] + df['slg']
    df['ops'].fillna(value=0, inplace=True)

    df.sort_values(['player_id', 'year_id'], ascending=[True, True], inplace=True)
    df = df.loc[df['games_played'] > 80]
    ops_max = pd.DataFrame(df.groupby('player_id')['ops'].max())
    ops_max.columns = ['max_ops']
    ops_max.reset_index(inplace=True)

    df = pd.merge(df, ops_max, how='inner', on='player_id')

    final_df = pd.DataFrame()
    player_list = set(df['player_id'].tolist())

    for player in player_list:
        print(player)
        temp_df = df.loc[df['player_id'] == player]
        temp_df.loc[temp_df['ops'] == temp_df['max_ops'], 'max_year'] = temp_df['year_id']
        temp_df['max_year'].fillna(temp_df['max_year'].mean(), inplace=True)
        temp_df['max_year'] = temp_df['max_year'].astype('int')
        temp_df['year_diff'] = temp_df['max_year'] - temp_df['year_id']
        temp_df.loc[temp_df['year_diff'] > 0, 'target'] = 0
        temp_df.loc[temp_df['year_diff'] < 0, 'target'] = 1
        temp_df = temp_df.loc[temp_df['year_diff'] != 0]
        final_df = final_df.append(temp_df)

    # Subset the data
    final_df['decade'] = final_df['decade'].astype('str')
    final_df = final_df[['ops', 'cumulative_games', 'salary', 'position', 'age', 'decade', 'weight', 'height', 'bats', 'throws', 'target']]

    return final_df
