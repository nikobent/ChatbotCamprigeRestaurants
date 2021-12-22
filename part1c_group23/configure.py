"""System options file. Can be true or false,
when true they are running, when false they are disabled.
"""
lower_for_csv = True #Turns all preferences to lower-case before searching the csv files
output_in_caps = True #System returned messages are always printed in ALLCAPS
limit_the_dialogue = False #When True, limits the maximum length of the dialog (# of acts) to 5
allow_restart = True #When True, restarts of the system are allowed
ask_correct_lev = True #Enables a user-prompt about the levenshtein match
use_baseline = False #When true the baseline system is used instead of the ML-classifier
offering_from_begin = False #When true, system begins suggesting restaurants immediatly. 

def editconf():
    print("\n -----------------------------CONFIGURATION SCREEN-------------------------------------\n")
    global lower_for_csv, output_in_caps, limit_the_dialogue, allow_restart, ask_correct_lev, use_baseline, offering_from_begin
    while True:
        varedit = input("What would you like to edit? (type exact name of variable) \n lower_for_csv: turns all preferences to lowercase before reading restaurant data \n output_in_caps: turns all system output messages into CAPS \n limit_the_dialogue: limits the full dialog to max. 5 acts \n allow_restart: when true, allows the system to restart \n ask_correct_lev: when true, asks user for confirmation if levenshtein distance is used \n use_baseline: when true, system uses baseline instead of ML classifier \n offering_from_begin: when true, system starts offering restaurants from the start \n OR type 'exit' to restart system \n")
        if varedit == "lower_for_csv":
            varvalue = input("Would you like it 'true' or 'false'? \n")
            if varvalue == "true":
                lower_for_csv = True
                print("lower_for_csv is now set to True; press any key to continue")
                input()
                continue
            if varvalue == "false":
                lower_for_csv = False
                print("lower_for_csv is now set to False; press any key to continue")
                input()
                continue
            else: 
                print("No correct input, system restarting with old value\n-------------------------------------------------------------------\n")
                break 
        elif varedit == "output_in_caps":
            varvalue = input("Would you like it 'true' or 'false'? \n")
            if varvalue == "true":
                output_in_caps = True
                print("output_in_caps is now set to True; press any key to continue")
                input()
                continue
            if varvalue == "false":
                output_in_caps = False
                print("output_in_caps is now set to False; press any key to continue")
                input()
                continue
            else: 
                print("No correct input, system restarting with old value\n-------------------------------------------------------------------\n")
                break
        elif varedit == "limit_the_dialogue":
            varvalue = input("Would you like it 'true' or 'false'? \n")
            if varvalue == "true":
                limit_the_dialogue = True
                print("limit_the_dialogue is now set to True; press any key to continue")
                input()
                continue
            if varvalue == "false":
                limit_the_dialogue = False
                print("limit_the_dialogue is now set to False; press any key to continue")
                input()
                continue
            else: 
                print("No correct input, system restarting with old value\n-------------------------------------------------------------------\n")
                break
        elif varedit == "allow_restart":
            varvalue = input("Would you like it 'true' or 'false'? \n")
            if varvalue == "true":
                allow_restart = True
                print("allow_restart is now set to True; press any key to continue")
                input()
                continue
            if varvalue == "false":
                allow_restart = False
                print("allow_restart is now set to False; press any key to continue")
                input()
                continue
            else: 
                print("No correct input, system restarting with old value\n-------------------------------------------------------------------\n")
                break
        elif varedit == "ask_correct_lev":
            varvalue = input("Would you like it 'true' or 'false'? \n")
            if varvalue == "true":
                ask_correct_lev = True
                print("ask_correct_lev is now set to True; press any key to continue")
                input()
                continue
            if varvalue == "false":
                ask_correct_lev = False
                print("ask_correct_lev is now set to False; press any key to continue")
                input()
                continue
            else: 
                print("No correct input, system restarting with old value\n-------------------------------------------------------------------\n")
                break
        elif varedit == "use_baseline":
            varvalue = input("Would you like it 'true' or 'false'? \n")
            if varvalue == "true":
                use_baseline = True
                print("use_baseline is now set to True; press any key to continue")
                input()
                continue
            if varvalue == "false":
                use_baseline = False
                print("use_baseline is now set to False; press any key to continue")
                input()
                continue
            else: 
                print("No correct input, system restarting with old value\n-------------------------------------------------------------------\n")
                break 
        elif varedit == "offering_from_begin":
            varvalue = input("Would you like it 'true' or 'false'? \n")
            if varvalue == "true":
                offering_from_begin = True
                print("offering_from_begin is now set to True; press any key to continue")
                input()
                continue
            if varvalue == "false":
                offering_from_begin = False
                print("offering_from_begin is now set to False; press any key to continue")
                input()
                continue
            else: 
                print("No correct input, system restarting with old value\n-------------------------------------------------------------------\n")
                break
        elif varedit == "exit":
            print("Exiting configuration, restarting system \n-------------------------------------------------------------------\n")
            break
        else: 
            print("No correct input given, system restarting with old values\n-----------------------------------------------------------oo--------\n")
            break
    return
          
