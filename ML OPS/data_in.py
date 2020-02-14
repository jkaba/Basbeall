# Queries which are used to pull data from local Lahman database
lahman_master_query = '''
    select
        batting.playerID as 'player_id',
        batting.yearID as 'year_id',
        batting.teamID as 'team_id',
        batting.lgID as 'league_id',
        batting.G as 'games_played',
        batting.AB as 'at_bats',
        batting.R as 'run_scored',
        batting.H as 'hits',
        batting.2B as 'doubles',
        batting.3B as 'triples',
        batting.HR as 'home_runs',
        batting.RBI as 'rbi',
        batting.SB as 'stolen_bases',
        batting.CS as 'caught_stealing',
        batting.BB as 'walks',
        batting.SO as 'strikeouts',
        batting.IBB as 'intentional_walks',
        batting.SF as 'sacrifice_flies',
        batting.HBP as 'hit_by_pitch',
        
        ifnull(battingpost.G, 0) as 'postseason_games_played',
        ifnull(battingpost.AB, 0) as 'postseason_at_bats',
        ifnull (battingpost.R, 0) as 'postseason_run_scored',
        ifnull(battingpost.H, 0) as 'postseason_hits',
        ifnull(battingpost.2B, 0) as 'postseason_doubles',
        ifnull(battingpost.3B, 0) as 'postseason_triples',
        ifnull(battingpost.HR, 0) as 'postseason_home_runs',
        ifnull(battingpost.RBI, 0) as 'postseason_rbi',
        ifnull(battingpost.SB, 0) as 'postseason_stolen_bases',
        ifnull(battingpost.BB, 0) as 'postseason_walks',
        ifnull(battingpost.SO, 0) as 'postseason_strikeouts',
        ifnull(battingpost.IBB, 0) as 'postseason_intentional_walks',
        
        salaries.salary,
        fielding.POS as 'position',
        master.nameFirst,
        master.nameLast
        
    from master
        inner join batting on master.playerID = batting.playerID
        inner join fielding on (fielding.playerID = batting.playerID and fielding.yearID = batting.yearID)
        left join battingpost on (battingpost.playerID = batting.playerID and battingpost.yearID = batting.yearID)
        left join salaries on (salaries.playerID = batting.playerID and salaries.yearID = batting.yearID)
            
    where
        /*My local database is too slow to run the below subquery, so I will just write a function to de-dupe records*/
        /*fielding.POS in (select max(G) from fielding where POS <> 'P' group by playerID, yearID)*/
        fielding.POS <> 'P'
        and batting.yearID >= 1995;'''


awards_query = '''
    select 
        playerID as 'player_id',
        yearID as 'year_id',
        awardID as 'award'
        
    from awardsplayers
    
    where awardID = "Silver Slugger"
    and yearID >= 1995;'''


all_star_query = '''
    select
        playerID as 'player_id',
        yearID as 'year_id'
        
    from allstarfull
    
    where yearID >= 1995;'''
