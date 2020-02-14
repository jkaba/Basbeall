lahman_query = '''
select
    batting.playerID as 'player_id',
    batting.yearID as 'year_id',
    batting.lgID as 'league_id',
    batting.G as 'games_played',
    batting.AB as 'at_bats',
    batting.H as 'hits',
    batting.2B as 'doubles',
    batting.3B as 'triples',
    batting.HR as 'home_runs',
    batting.BB as 'walks',
    batting.IBB as 'intentional_walks',
    batting.SF as 'sacrifice_flies',
    batting.HBP as 'hit_by_pitch',
    salaries.salary,
    fielding.POS as 'position',
    master.birthYear as 'birth_year',
    master.weight,
    master.height,
    master.bats,
    master.throws, 
    batting.yearID - master.birthYear as 'age'
    
from master
    inner join batting on master.playerID = batting.playerID
    inner join fielding on (fielding.playerID = batting.playerID and fielding.yearID = batting.yearID)
    left join salaries on (salaries.playerID = batting.playerID and salaries.yearID = batting.yearID)
    
where master.finalGame < '2018-10-31'
    and fielding.POS <> 'P'
    and master.debut >= '2000-01-01';'''
