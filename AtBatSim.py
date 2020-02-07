# At Bat Simulator which Simulates 100 At Bats and saves results in a .csv
# Values and pitches can be tuned towards a specific pitcher if pitches and pitch probabilities are known
# Author = Jameel Kaba

# Import Statements
import numpy as np
import pandas as pd

# Simulation function
# Input: Series of probabilities
# Output: Simulation results
def simulation(FB_Surrender, CB_Surrender, CH_Surrender, FB_Hit, CB_Hit, CH_Hit, Zero_Zero_Pitch, Zero_Zero_Surrender, Zero_Zero_Hit, One_Zero_Pitch, One_Zero_Surrender, One_Zero_Hit, Zero_One_Pitch, Zero_One_Surrender, Zero_One_Hit, One_One_Pitch, One_One_Surrender, One_One_Hit, Two_Zero_Pitch, Two_Zero_Surrender, Two_Zero_Hit, Zero_Two_Pitch, Zero_Two_Surrender, Zero_Two_Hit, One_Two_Pitch, One_Two_Surrender, One_Two_Hit, Two_One_Pitch, Two_One_Surrender, Two_One_Hit, Three_Zero_Pitch, Three_Zero_Surrender, Three_Zero_Hit, Two_Two_Pitch, Two_Two_Surrender, Two_Two_Hit, Three_One_Pitch, Three_One_Surrender, Three_One_Hit, Three_Two_Pitch, Three_Two_Surrender, Three_Two_Hit, Zero_Zero_Swing, One_Zero_Swing, Zero_One_Swing, One_One_Swing, Two_Zero_Swing, Zero_Two_Swing, One_Two_Swing, Two_One_Swing, Three_Zero_Swing, Two_Two_Swing, Three_One_Swing, Three_Two_Swing, Swing_Out):

    # Child Function pitchSimulation
    # Input: Pitch Probabilities inherited from parent function
    # Output: Data frame containing the outcome of the pitch
    def pitchSimulation(count, count_swing_prob, pitch_probs, count_surrender_prob, FB_Surrender, count_hit_prob, FB_Hit, CB_Surrender, CB_Hit, CH_Surrender, CH_Hit, df):

        # Randomly select a pitch, and whether or not the hitter swings
        pitch = np.random.choice(a=['fastball', 'change', 'curve'], p=pitch_probs)
        swing = np.random.choice(a=['yes', 'no'], p=[count_swing_prob, 1 - count_swing_prob])
    
        # If the pitch is a fastball
        if pitch == 'fastball':
        
            # Hit probability is based on an average of how often the pitcher gives up a hit at that count and with that pitch, as well as how often the hitter records a hit in that count and how often they get a hit on that pitch
            hit_prob = (count_surrender_prob + FB_Surrender + count_hit_prob + FB_Hit) / 4
            
            # If the hitter swings, randomly determine the outcome
            if swing == 'yes':
                outcome = np.random.choice(a=['hit', 'no_hit'], p=[hit_prob, 1 - hit_prob])
                
            # If the hitter doesn't swing, record outcome as no_hit
            elif swing == 'no':
                outcome = 'no_hit'
                
            # Append outcome to data frame
            df = df.append(pd.DataFrame({'count': count, 'pitch': 'fastball', 'swing': swing, 'result': [outcome]}))
        
        # Repeat above process for Secondary pitch
        elif pitch == 'change':
            hit_prob = (count_surrender_prob + CH_Surrender + count_hit_prob + CH_Hit) / 4
        
            if swing == 'yes':
                outcome = np.random.choice(a=['hit', 'no_hit'], p=[hit_prob, 1 - hit_prob])
            
            elif swing == 'no':
                outcome = 'no_hit'
            
            df = df.append(pd.DataFrame({'count': count, 'pitch': 'change', 'swing': swing, 'result': [outcome]}))
        

        # Repeat above process for Tertiary pitch
        elif pitch == 'curve':
            hit_prob = (count_surrender_prob + CB_Surrender + count_hit_prob + CB_Hit) / 4
        
            if swing == 'yes':
                outcome = np.random.choice(a=['hit', 'no_hit'], p=[hit_prob, 1 - hit_prob])
            
            elif swing == 'no':
                outcome = 'no_hit'
            
            df = df.append(pd.DataFrame({'count': count, 'pitch': 'curve', 'swing': swing, 'result': [outcome]}))

        # Return the data frame
        return df

    # Set result variable to reference data frame
    results = pd.DataFrame()

    # Simulate the 0-0 count
    results = pitchSimulation(count='0-0', count_swing_prob=Zero_Zero_Swing, pitch_probs=Zero_Zero_Pitch, count_surrender_prob=Zero_Zero_Surrender, FB_Surrender=FB_Surrender, count_hit_prob=Zero_Zero_Hit, FB_Hit=FB_Hit, CB_Surrender=CB_Surrender, CB_Hit=CB_Hit, CH_Surrender=CH_Surrender, CH_Hit=CH_Hit, df=results)

    # Based on the previous pitch, the simulation continues as follows
    lastResult = results.tail(1)

    # If the last pitch resulted in a swing, then randomly determine if it was the end of the at bat
    if lastResult['swing'].any() == 'yes':
        end_of_at_bat = np.random.choice(a=['yes', 'no'], p=[Swing_Out, 1 - Swing_Out])
        
    # Else, at bat continues
    else:
        end_of_at_bat = 'no'

    # If the result was not a hit, and the at bat hasn't ended, 50/50 chance to determine new count
    if results['result'].any() == 'no_hit' and end_of_at_bat == 'no':
        new_count = np.random.choice(a=['0-1', '1-0'], p=[0.50, 0.50])

        # Continue based on new count
        # Run simulation on 0-1 count
        if new_count == '0-1':
            results = pitchSimulation(count='0-1', count_swing_prob=Zero_One_Swing, pitch_probs=Zero_One_Pitch, count_surrender_prob=Zero_One_Surrender, FB_Surrender=FB_Surrender, count_hit_prob=Zero_One_Hit, FB_Hit=FB_Hit, CB_Surrender=CB_Surrender, CB_Hit=CB_Hit, CH_Surrender=CH_Surrender, CH_Hit=CH_Hit, df=results)

        # Run simulation on 1-0 count
        elif new_count == '1-0':
            results = pitchSimulation(count='1-0', count_swing_prob=One_Zero_Swing, pitch_probs=One_Zero_Pitch, count_surrender_prob=One_Zero_Surrender, FB_Surrender=FB_Surrender, count_hit_prob=One_Zero_Hit, FB_Hit=FB_Hit, CB_Surrender=CB_Surrender, CB_Hit=CB_Hit, CH_Surrender=CH_Surrender, CH_Hit=CH_Hit, df=results)

        # Repeat process from above, get last result, determine if at bat has ended, if not determine new count
        lastResult = results.tail(1)

        if lastResult['swing'].any() == 'yes':
            end_of_at_bat = np.random.choice(a=['yes', 'no'], p=[Swing_Out, 1 - Swing_Out])
            
        else:
            end_of_at_bat = 'no'

        if lastResult['result'].any() == 'no_hit' and lastResult['count'].any() == '1-0' and end_of_at_bat == 'no':
            new_count = np.random.choice(a=['1-1', '2-0'], p=[0.50, 0.50])

        elif lastResult['result'].any() == 'no_hit' and lastResult['count'].any() == '0-1':
            new_count = np.random.choice(a=['1-1', '0-2'], p=[0.50, 0.50])

        if new_count == '1-1':
            results = pitchSimulation(count='1-1', count_swing_prob=One_One_Swing, pitch_probs=One_One_Pitch, count_surrender_prob=One_One_Surrender, FB_Surrender=FB_Surrender, count_hit_prob=One_One_Hit, FB_Hit=FB_Hit, CB_Surrender=CB_Surrender, CB_Hit=CB_Hit, CH_Surrender=CH_Surrender, CH_Hit=CH_Hit, df=results)

        elif new_count == '2-0':
            results = pitchSimulation(count='2-0', count_swing_prob=Two_Zero_Swing, pitch_probs=Two_Zero_Pitch, count_surrender_prob=Two_Zero_Surrender, FB_Surrender=FB_Surrender, count_hit_prob=Two_Zero_Hit, FB_Hit=FB_Hit, CB_Surrender=CB_Surrender, CB_Hit=CB_Hit, CH_Surrender=CH_Surrender, CH_Hit=CH_Hit, df=results)

        elif new_count == '0-2':
            results = pitchSimulation(count='0-2', count_swing_prob=Zero_Two_Swing, pitch_probs=Zero_Two_Pitch, count_surrender_prob=Zero_Two_Surrender, FB_Surrender=FB_Surrender, count_hit_prob=Zero_Two_Hit, FB_Hit=FB_Hit, CB_Surrender=CB_Surrender, CB_Hit=CB_Hit, CH_Surrender=CH_Surrender, CH_Hit=CH_Hit, df=results)

        # Repeat for count after 3 pitches
        lastResult = results.tail(1)

        if lastResult['swing'].any() == 'yes':
            end_of_at_bat = np.random.choice(a=['yes', 'no'], p=[Swing_Out, 1 - Swing_Out])
            
        else:
            end_of_at_bat = 'no'

        if lastResult['result'].any() == 'no_hit' and lastResult['count'].any() == '1-1' and end_of_at_bat == 'no':
            new_count = np.random.choice(a=['1-2', '2-1'], p=[0.50, 0.50])

        elif lastResult['result'].any() == 'no_hit' and lastResult['count'].any() == '2-0':
            new_count = np.random.choice(a=['2-1', '3-0'], p=[0.50, 0.50])

        elif lastResult['result'].any() == 'no_hit' and lastResult['count'].any() == '0-2':
            new_count = '1-2'

        if new_count == '1-2':
            results = pitchSimulation(count='1-2', count_swing_prob=One_Two_Swing, pitch_probs=One_Two_Pitch, count_surrender_prob=One_Two_Surrender, FB_Surrender=FB_Surrender, count_hit_prob=One_Two_Hit, FB_Hit=FB_Hit, CB_Surrender=CB_Surrender, CB_Hit=CB_Hit, CH_Surrender=CH_Surrender, CH_Hit=CH_Hit, df=results)

        if new_count == '2-1':
            results = pitchSimulation(count='2-1', count_swing_prob=Two_One_Swing, pitch_probs=Two_One_Pitch, count_surrender_prob=Two_One_Surrender, FB_Surrender=FB_Surrender, count_hit_prob=Two_One_Hit, FB_Hit=FB_Hit, CB_Surrender=CB_Surrender, CB_Hit=CB_Hit, CH_Surrender=CH_Surrender, CH_Hit=CH_Hit, df=results)

        if new_count == '3-0':
            results = pitchSimulation(count='3-0', count_swing_prob=Three_Zero_Swing, pitch_probs=Three_Zero_Pitch, count_surrender_prob=Three_Zero_Surrender, FB_Surrender=FB_Surrender, count_hit_prob=Three_Zero_Hit, FB_Hit=FB_Hit, CB_Surrender=CB_Surrender, CB_Hit=CB_Hit, CH_Surrender=CH_Surrender, CH_Hit=CH_Hit, df=results)

        # Repeat for pitch count after 4 pitches
        lastResult = results.tail(1)

        if lastResult['swing'].any() == 'yes':
            end_of_at_bat = np.random.choice(a=['yes', 'no'], p=[Swing_Out, 1 - Swing_Out])
            
        else:
            end_of_at_bat = 'no'

        if lastResult['result'].any() == 'no_hit' and lastResult['count'].any() == '1-2' and end_of_at_bat == 'no':
            new_count = '2-2'

        elif lastResult['result'].any() == 'no_hit' and lastResult['count'].any() == '2-1':
            new_count = np.random.choice(a=['2-2', '3-1'], p=[0.50, 0.50])

        elif lastResult['result'].any() == 'no_hit' and lastResult['count'].any() == '3-0':
            new_count = '3-1'

        if new_count == '2-2':
            results = pitchSimulation(count='2-2', count_swing_prob=Two_Two_Swing, pitch_probs=Two_Two_Pitch, count_surrender_prob=Two_Two_Surrender, FB_Surrender=FB_Surrender, count_hit_prob=Two_Two_Hit, FB_Hit=FB_Hit, CB_Surrender=CB_Surrender, CB_Hit=CB_Hit, CH_Surrender=CH_Surrender, CH_Hit=CH_Hit, df=results)

        if new_count == '3-1':
            results = pitchSimulation(count='3-1', count_swing_prob=Three_One_Swing, pitch_probs=Three_One_Pitch, count_surrender_prob=Three_One_Surrender, FB_Surrender=FB_Surrender, count_hit_prob=Three_One_Hit, FB_Hit=FB_Hit, CB_Surrender=CB_Surrender, CB_Hit=CB_Hit, CH_Surrender=CH_Surrender, CH_Hit=CH_Hit, df=results)

        # Repeat for pitch count after 5 pitches
        lastResult = results.tail(1)

        if lastResult['swing'].any() == 'yes':
            end_of_at_bat = np.random.choice(a=['yes', 'no'], p=[Swing_Out, 1 - Swing_Out])
            
        else:
            end_of_at_bat = 'no'

        if lastResult['result'].any() == 'no_hit' and end_of_at_bat == 'no':
            results = pitchSimulation(count='3-2', count_swing_prob=Three_Two_Swing, pitch_probs=Three_Two_Pitch, count_surrender_prob=Three_Two_Surrender, FB_Surrender=FB_Surrender, count_hit_prob=Three_Two_Hit, FB_Hit=FB_Hit, CB_Surrender=CB_Surrender, CB_Hit=CB_Hit, CH_Surrender=CH_Surrender, CH_Hit=CH_Hit, df=results)

    # Return data frame containing pitch and at bat result
    return results

# Main function
def main():

    # Setting up probabilities
    # All probabilities are not set to any pitcher or hitter, values can be tuned for better precision
    
    # Pitch probabilities
    FB_Surrender = 0.250
    CH_Surrender = 0.250
    CB_Surrender = 0.250


    FB_Hit = 0.300
    CH_Hit = 0.250
    CB_Hit = 0.200

    # Probabilities for 0-0 count
    Zero_Zero_Pitch = [0.70, 0.20, 0.10]
    Zero_Zero_Surrender = 0.250
    Zero_Zero_Hit = 0.250
    Zero_Zero_Swing = 0.250

    # Probabilities for a 1-0 count
    One_Zero_Pitch = [0.60, 0.25, 0.15]
    One_Zero_Surrender = 0.250
    One_Zero_Hit = 0.260
    One_Zero_Swing = 0.45

    # Probabilities for a 0-1 count
    Zero_One_Pitch = [0.50, 0.25, 0.25]
    Zero_One_Surrender = 0.235
    Zero_One_Hit = 0.260
    Zero_One_Swing = 0.400

    # Probabilities for a 1-1 count
    One_One_Pitch = [0.60, 0.20, 0.20]
    One_One_Surrender = 0.250
    One_One_Hit = 0.250
    One_One_Swing = 0.50

    # Probabilities for a 2-0 count
    Two_Zero_Pitch = [0.70, 0.25, 0.05]
    Two_Zero_Surrender = 0.275
    Two_Zero_Hit = 0.230
    Two_Zero_Swing = 0.40

    # Probabilities for a 0-2 count
    Zero_Two_Pitch = [0.45, 0.35, 0.20]
    Zero_Two_Surrender = 0.205
    Zero_Two_Hit = 0.220
    Zero_Two_Swing = 0.50

    # Probabilities for a 1-2 count
    One_Two_Pitch = [0.50, 0.20, 0.30]
    One_Two_Surrender = 0.200
    One_Two_Hit = 0.230
    One_Two_Swing = 0.65

    # Probabilities for a 2-1 count
    Two_One_Pitch = [0.55, 0.25, 0.20]
    Two_One_Surrender = 0.250
    Two_One_Hit = 0.250
    Two_One_Swing = 0.55

    # Probabilities for a 3-0 count
    Three_Zero_Pitch = [0.90, 0.05, 0.05]
    Three_Zero_Surrender = 0.290
    Three_Zero_Hit = 0.310
    Three_Zero_Swing = 0.05

    # Probabilities for 2-2 count
    Two_Two_Pitch = [0.60, 0.25, 0.15]
    Two_Two_Surrender = 0.215
    Two_Two_Hit = 0.230
    Two_Two_Swing = 0.50
    
    # Probabilities for a 3-1 count
    Three_One_Pitch = [0.80, 0.15, 0.05]
    Three_One_Surrender = 0.280
    Three_One_Hit = 0.300
    Three_One_Swing = 0.50

    # Probabilities for a full count
    Three_Two_Pitch = [0.80, 0.10, 0.10]
    Three_Two_Surrender = 0.265
    Three_Two_Hit = 0.280
    Three_Two_Swing = 0.75

    # Probability that the swing results in an out
    Swing_Out = 0.70

    # Set up results frame
    results = pd.DataFrame()

    # Adjust number of simulations
    simulation_runs = 100
    counter = 0
    
    # Simulate X number of times
    while counter < simulation_runs:
        temp = simulation(FB_Surrender, CB_Surrender, CH_Surrender, FB_Hit, CB_Hit, CH_Hit, Zero_Zero_Pitch, Zero_Zero_Surrender, Zero_Zero_Hit, One_Zero_Pitch, One_Zero_Surrender, One_Zero_Hit, Zero_One_Pitch, Zero_One_Surrender, Zero_One_Hit, One_One_Pitch, One_One_Surrender, One_One_Hit, Two_Zero_Pitch, Two_Zero_Surrender, Two_Zero_Hit, Zero_Two_Pitch, Zero_Two_Surrender, Zero_Two_Hit, One_Two_Pitch, One_Two_Surrender, One_Two_Hit, Two_One_Pitch, Two_One_Surrender, Two_One_Hit, Three_Zero_Pitch, Three_Zero_Surrender, Three_Zero_Hit, Two_Two_Pitch, Two_Two_Surrender, Two_Two_Hit, Three_One_Pitch, Three_One_Surrender, Three_One_Hit, Three_Two_Pitch, Three_Two_Surrender, Three_Two_Hit, Zero_Zero_Swing, One_Zero_Swing, Zero_One_Swing, One_One_Swing, Two_Zero_Swing, Zero_Two_Swing, One_Two_Swing, Two_One_Swing, Three_Zero_Swing, Two_Two_Swing, Three_One_Swing, Three_Two_Swing, Swing_Out)

        # Append the at bat result to the data frame and increment counter
        results = results.append(temp)
        counter += 1
    
    # Save results in a .csv (Alternatively could print each pitch to screen with a delay)
    results.to_csv('simulation_results.csv', index=False)
