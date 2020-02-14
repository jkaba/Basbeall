import pandas as pd
import glob

# Pitching Queries
# These queries pull Lahman pitching data from local MySQL database
pitching_query = '''
    select 
        sum(pitching.ER) as "earned_runs",
        sum(pitching.IPouts) / 3 as "innings_pitched",
        master.throws as "pitcher_arm",
        master.retroID as "pit_id",
        pitching.yearID as "year"
        
    from pitching
        inner join master on pitching.playerID = master.playerID
        
    where pitching.yearID >= '2010'
        
    group by
        master.throws,
        master.retroID,
        pitching.yearID;'''


def get_pitching_experience_query(year):
    pitching_experience_query = '''
        select
          count(pitching.playerID) as "pit_years_of_experience",
          master.retroID as "pit_id"
        
        from pitching
            inner join master on pitching.playerID = master.playerID
        
        where pitching.yearID <= '{0}'
            and pitching.yearID >= '1990'
        
        group by
            master.retroID;'''.format(year)

    return pitching_experience_query

# Batting Queries
# These queries are used to pull batting data from local Lahman database
batting_query = '''
    select
        sum(batting.H) as "H",
        sum(batting.2B) as "2B",
        sum(batting.3B) as "3B",
        sum(batting.HR) as "HR",
        sum(batting.AB) as "AB",
        sum(batting.BB) as "BB",
        sum(batting.HBP) as "HBP",
        sum(batting.SF) as "SF",
        master.bats as "batter_arm",
        master.retroID as "bat_id",
        batting.yearID as "year"
        
    from batting
        inner join master on batting.playerID = master.playerID
        
    where batting.yearID >= '2010'
        
    group by
        master.bats,
        master.retroID,
        batting.yearID;'''


def get_batting_experience_query(year):
    batting_experience_query = '''
        select
          count(batting.playerID) as "bat_years_of_experience",
          master.retroID as "bat_id"

        from batting
            inner join master on batting.playerID = master.playerID

        where batting.yearID <= '{0}'
            and batting.yearID >= '1990'

        group by
            master.retroID;'''.format(year)

    return batting_experience_query

# ingest_retrosheet_csv function
# This function is used to combine all Retrosheet csv files into 1 dataframe
def ingest_retrosheet_csv():

    field_names = pd.read_csv('fields.csv')
    fields = field_names['Header'].tolist()

    df = pd.DataFrame()

    for counter, file in enumerate(glob.glob("data/all*")):
        print file
        temp_df = pd.read_csv(file, skiprows=0, names=fields)
        df = df.append(temp_df)

    df.columns = map(str.lower, df.columns)
    df['home_team_id'] = df['game_id'].str[0:3]
    return df

