import pandas as pd


def calculate_decline_by_category(dataframe, column):
    try:
        grouped = dataframe.groupby(column).agg({'target': 'sum'}).reset_index()
        df_len = dataframe.groupby(column).agg({'target': 'count'}).reset_index()
        df_len.rename(columns={'target': 'denom'}, inplace=True)

        grouped = pd.merge(grouped, df_len, how='inner', on=column)
        grouped['percentage'] = grouped['target'] / grouped['denom']
        grouped.to_csv('exploration/' + column + '_percentage.csv')
    except:
        print('cannot analyze this value')

    return
