# Name: Jameel Kaba
# Method Validate
# Input: The initial number of outs, initial runners on base, the final number of outs, final runners on base, and runs scored
# Output: True, if the play transition is valid; False, otherwise
def validate(initial_outs, initial_base_runners, final_outs, final_base_runners, runs_scored):
    
    # Bases should be empty when 3 outs are recorded
    if(final_outs == 3 and len(final_base_runners) != 0):
        return False

    # Cannot go backwards in outs
    elif(initial_outs > final_outs):
        return False

    # Cannot have more outs than currently possible
    elif(final_outs > initial_outs + len(initial_base_runners) + 1):
        return False

    # Cannot score more than the amount of runners + hitter
    elif(runs_scored > ((len(initial_base_runners)+1))):
        return False

    # If there is a run scored while not at 3 outs
    elif(runs_scored > 0 and final_outs < 3):
    
        # Cannot have more runs, outs, and runners than what is initially possible
        if(final_outs + runs_scored + len(final_base_runners) != initial_outs + len(initial_base_runners) + 1):
            
            # If a run scored via wild pitch, passed ball, error, etc. we have a valid play
            if((runs_scored == len(initial_base_runners) - len(final_base_runners))):
                return True
            
            # Combo of runs, outs, and runners is not possible, play is not valid
            return False

    # Cannot have more base runners than the initial plus 1
    elif(len(initial_base_runners) + 1 != len(final_base_runners) and runs_scored == 0 and final_outs < 3):

        # Check to see if bases are not empty, and that there are the same amount of outs
        if(((0 < len(initial_base_runners) != 3) and (0 < len(final_base_runners) != 3)) and (initial_outs == final_outs)):
            
            # Base runners cannot go backwards -> Not Valid
            if((initial_base_runners > final_base_runners) or (initial_base_runners == final_base_runners)):
                return False
        
            # Runner advanced via walk, wild pitch, passed ball, etc.
            return True


        # Check to see if no runners advances, or if a runner got tagged out
        elif((len(initial_base_runners) == len(final_base_runners) or len(initial_base_runners) == len(final_base_runners) + 1) and (final_outs - initial_outs > 0)):
            return True
        
        elif((len(initial_base_runners) - len(final_base_runners)) > 0 and (final_outs - initial_outs) > 0):
            return True
        
        # Cannot have more runs, outs, and runners than what is initially possible
        elif(final_outs + runs_scored + len(final_base_runners) != initial_outs + len(initial_base_runners) + 1):
            return False

        # Play is not valid, as there are too many runners
        return False

    # Cannot have more base runners than possible, and check to see if outs remain the same
    elif((len(initial_base_runners) == len(final_base_runners)) or (len(initial_base_runners) + 1 == len(final_base_runners)) and (initial_outs == final_outs)):

        # If there are runners on base both before and after the play
        if(len(initial_base_runners) != 0 and len(final_base_runners) != 0):
            
            # If the base runner is still on base, then the play is valid
            if(initial_base_runners[0] in final_base_runners):
                return True
            
            # If the base runner has moved backwards, the play is not valid
            return False

    # Checks all pass, valid play
    return True



# TESTS
# To view test results, just uncomment the test and run the program.
# Example: 1 out, runner at 3rd -> 1 out, runners at 1st and 2nd with 0 runs scored (NOT VALID)
#print(validate(1,[3],1,[1,2],0))

# Example: 1 out, runners at 1st, and 3rd -> 1 out, 1st and 3rd with 0 runs scored (VALID)
#print(validate(1,[1,2],1,[1,3],0))

# 1 out, runner at 3rd -> 1 out, runners at 1st and 2nd with 1 run scored (NOT VALID)
#print(validate(1,[3],1,[1,2],1))

# 0 out, runner at 1st -> 0 outs, runner at 2nd, 0 score (VALID)
#print(validate(0,[1],0,[2],0))

# 0 out, runner at 2nd -> 0 outs, runner at 3rd, 0 score (VALID)
#print(validate(0,[2],0,[3],0))

# 0 out, runner at 3rd -> 0 outs, bases empty, 1 run scores (VALID)
#print(validate(0,[3],0,[],1))

# 0 out, runner at 1st -> 0 outs, bases empty, 0 runs score (NOT VALID)
#print(validate(0,[1],0,[],0))

# 0 out, runner at 2nd -> 0 outs, runner at 1st, 0 runs score (NOT VALID)
#print(validate(0,[2],0,[1],0))

# 0 out, runner at 3rd -> 0 outs, runner at 2nd, 0 runs score (NOT VALID)
#print(validate(0,[3],0,[2],0))

# 0 out, runners at 1st and 2nd -> 0 outs, runners at 2nd and 3rd, 0 scored (VALID)
#print(validate(0,[1,2],0,[2,3],0))

# 0 out, runners at 2nd and 3rd -> 0 outs, runner from 3, 1 scored (VALID)
#print(validate(0,[2,3],0,[3],1))

# 0 outs, runner at 1st -> 1 out, bases empty 0 score (VALID)
#print(validate(0,[1],1,[],0))

# 0 outs, runner at 2nd -> 1 out, bases empty, 0 score (VALID)
#print(validate(0,[2],1,[],0))

# 0 out, runner at 3rd -> 1 out, bases empty, 0 score (VALID)
#print(validate(0,[3],1,[],0))

# 0 out, runner at 1st and 2nd -> 1 out, runner at 2nd, 0 score (VALID)
#print(validate(0,[1,2],1,[2],0))

# 0 outs, runners at 1st and 3rd -> 1 out, runner at 3rd, 0 score (VALID)
#print(validate(0,[1,3],1,[3],0))

# 0 outs, runners at 1st and 2nd -> 2 outs, bases empty, 0 score (VALID)
#print(validate(0,[1,2],2,[],0))

# 0 outs, runners at 1st and 3rd -> 2 outs, bases empty, 0 score (VALID)
#print(validate(0,[1,3],2,[],0))

# 0 outs, bases loaded -> 1 out, runners at 2nd and 3rd, 0 score (VALID)
#print(validate(0,[1,2,3],1,[2,3],0))

# 0 outs, bases loaded -> 2 outs, runner at 2nd, 0 score (VALID)
#print(validate(0,[1,2,3],2,[2],0))

# 0 outs, bases loaded -> 3 outs, 0 score (VALID)
#print(validate(0,[1,2,3],3,[],0))

# 1 out, runner at 2nd -> 1 out, runners at 1st and 2nd, 1 score (NOT VALID)
#print(validate(1,[2],1,[1,2],1))

# 1 out, runner at 1st -> 1 out, runners at 1st and 2nd, 1 score (NOT VALID)
#print(validate(1,[1],1,[1,2],1))

# 1 out, runners at 2nd and 3rd -> 1 out, runners at 1st and 2nd, 0 score (NOT VALID)
#print(validate(1,[2,3],1,[1,2],0))

# 1 out, runners at 1st and 3rd -> 1 out, runners at 1st and 2nd, 0 score (NOT VALID)
#print(validate(1,[1,3],1,[1,2],0))

# 1 out, runners at 1st and 3rd -> 1 out, runners at 1st and 3rd, 0 score (NOT VALID**)
#print(validate(1,[1,3],1,[1,3],0))
