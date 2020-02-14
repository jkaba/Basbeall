import pandas as pd

# calculate_failure_rates function
# This function calculates the percentage of plays in which a pitcher gives up a run
def calculate_failure_rates(dataframe, column):

    try:
        grouped = dataframe.groupby([column, 'pitcher_number']).agg({'rbi_ct': 'sum'}).reset_index()
        df_len = dataframe.groupby([column, 'pitcher_number']).agg({'game_id': 'count'}).reset_index()
        df_len.rename(columns={'rbi_ct': 'denom'}, inplace=True)

        grouped = pd.merge(grouped, df_len, how='inner', on=[column, 'pitcher_number'])
        grouped['failure_rate'] = grouped['rbi_ct'] / grouped['denom']
        grouped.to_csv(column + '_failure_rate.csv')
    except:
        print('cannot analyze this value')

    return None
