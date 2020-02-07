# Home Run scraper program
# This program scrapes home run data from Fox Sports MLB
# This program prints out the following data information: Year, # of home runs, Mean # home runs, Std of home runs, Var from average
# Author = Jameel Kaba

# Batting csv is from the baseball data bank
# Link to Baseball Data Bank: https://github.com/chadwickbureau/baseballdatabank

# Import statements
import pandas as pd
import numpy as np
from scipy.stats import norm
import requests
from bs4 import BeautifulSoup
from time import sleep
from sklearn.preprocessing import MinMaxScaler

# totalfile function
# Input: a data frame
# Output: a merged data frame
def totalFile(df):
    mergedDF = pd.DataFrame(df.groupby('yearID')['HR'].sum())
    mergedDF.reset_index(inplace=True)
    mergedDF.columns = ['Year', 'HR']
    mergedDF[['Year', 'HR']] = mergedDF[['Year', 'HR']].astype('int')
    return mergedDF

# scrapeHR function
# This function scrapes home run data from fox sports and saves it as a .csv
# Output: Home Run Data frame
def scrapeHR():
    hr_df = pd.DataFrame()
    for page in range(1, 27):
        url = 'https://www.foxsports.com/mlb/stats?season=2019&category=BATTING&group=1&sort=7&time=0&pos=0&qual=1&' \
              'sortOrder=0&splitType=0&page={0}&statID=0'.format(page)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features="lxml")
        table = soup.findAll('tr')
        data = ([[td.getText() for td in table[i].findAll('td')] for i in range(len(table))])
        df = pd.DataFrame(data)
        hr_df = hr_df.append(df)
    hr_df.to_csv('2019_hr.csv')
    return hr_df

# calculate function
# This function calculates, mean, std, and variance of home runs through the years and prints to screen
def calculate():

    # Read data / Setup data frames
    df2019 = pd.read_csv('2019_hr.csv')
    total_2019 = df2019['8'].sum()
    
    # Batting csv is from the Baseball Data Bank
    batting_df = pd.read_csv('Batting.csv')
    batting_df = totalFile(batting_df)
    
    df2019 = pd.DataFrame({'HR': [total_2019], 'Year': [2019]})
    batting_df = pd.concat([batting_df, df2019], axis=0, sort=True)

    df = pd.DataFrame()
    
    # 20 year time period, let's get info for the past 20 seasons
    for year in range(2000, 2020):
        
        # Initial setup
        cutoff = year - 20
        new_df = batting_df.loc[(batting_df['Year'] >= cutoff) & (batting_df['Year'] < year)]
        
        # Calculate mean and std
        m = new_df['HR'].mean()
        standard = new_df['HR'].std()
        
        # temp data used to clean up for insertion
        tempBat = (batting_df.loc[batting_df['Year'] == year]).reset_index(drop=True)
        numHR = tempBat['HR'][0]
        
        # Load up the appropriate values to create a data frame entry
        dfEntry = pd.DataFrame({
        
            # Year of entry
            'Year': [year],
            
            # Number of home runs hit that season
            'HR': [numHR],
            
            # Rolling mean value updates for every season
            'Mean HR': m,
            
            # Rolling standard deviation value updates for every season
            'Standard Deviation': standard,
        })
        df = df.append(dfEntry)

    # Calculate variance from the average
    df['Variance'] = abs(df['HR'] - df['Mean HR'])
    
    # Print results and exit
    print(df)
    return

# Main function calculates the 2 methods
if __name__ == "__main__":
    scrapeHR()
    calculate()
