import Levenshtein as lev
import pandas as pd
import json
import re
import statetransition as st
import string

""" Function: substring; little helper function to make sure code does not interpret: ('no' in 'north part of town') as true, for example. """
def substring(part, full):
    """Checks if part is in full, not within word: 'any' in 'anything' == false; 'any' in 'any thing' == true"""
    index = full.find(part)
    if index == -1:
        return False
    if index != 0 and full[index-1] not in string.whitespace:
        return False
    L = index + len(part)
    if L < len(full) and full[L] not in string.whitespace:
        return False
    return True

# Open the json file and store as variable 'data'
with open('ontology_dstc2.json') as json_file:
    data = json.load(json_file)


"""Function: spellcheck;
If user-given spelling matches the json file, the spelling is correct
else use levenshtein distance to find the correct spelling"""
def spellcheck(word, type):
    if word in data['informable'][type]:
        return (word, False)
    else:
        list = []
        for i in data['informable'][type]:
            list.append(lev.distance(word, i))
        index = list.index(min(list))
        return (data['informable'][type][index], True)


"""Function: fillfood; Checks user utterance for information on food_type, and stores it in global variable
Flags the info as unsure (st.unsurefood=True) if the lev_distance was used to find the information in the user-utterance."""
def fillfood(users_utterance):
    # search whether food is in the sentence
    matchFood = re.search(r'(.*) food(.*)', users_utterance)
    if matchFood:
        stringFood = (re.split(r'\W', matchFood.group(1)))[-2:]
        stringFood = ''.join(stringFood)
        st.foodPreference, st.unsurefood = spellcheck(stringFood, 'food')
        # 'unsure' is a boolean variable that if true means that our system was unsure for the user's input and used levensthein
    else:
        split_utterance = (re.split(r'\W', users_utterance))
        #the types of food have a maximum length of two 
        if len(split_utterance) < 3: 
            st.foodPreference, st.unsurefood = spellcheck(users_utterance, 'food')
    return (st.foodPreference, st.unsurefood)

"""Function: fillprice; Checks user utterance for information on price_range, and stores it in global variable
Flags the info as unsure (st.unsureprice=True) if the lev_distance was used to find the information in the user-utterance."""
def fillprice(users_utterance):
    # Information on price is searched with regular expressions and with simple If's because we want to be sure that we don't lose any information
    matchPrice = re.search(r'(.*) price(.*)', users_utterance)
    if "cheap" in users_utterance:
        st.pricePreference, st.unsureprice = "cheap", False
    elif "moderate" in users_utterance or "moderately" in users_utterance:
        st.pricePreference, st.unsureprice = "moderate", False

    elif "expenisve" in users_utterance:
        st.pricePreference, st.unsureprice = "expensive", False
    # find word before price
    elif matchPrice:
        stringPrice = re.split(r'\W', matchPrice.group(1))[-1]
        st.pricePreference, st.unsureprice = spellcheck(stringPrice, 'pricerange')
        # adjust moderately to moderate
        if st.pricePreference == 'moderately':
            st.pricePreference = 'moderate'
    return (st.pricePreference, st.unsureprice)

"""Function: fillarea; Checks user utterance for information on area, and stores it in global variable
Flags the info as unsure (st.unsureloc=True) if the lev_distance was used to find the information in the user-utterance."""
def fillarea(users_utterance):
    # search whether location is in the sentence, with the same measures as we did for the price
    matchLocation = re.search(r'(.*) part of town(.*)', users_utterance)
    if "centre" in users_utterance:
        st.locPreference, st.unsureloc = "centre", False
    elif "north" in users_utterance:
        st.locPreference, st.unsureloc = "north", False
    elif "south" in users_utterance:
        st.locPreference, st.unsureloc = "south", False
    elif "west" in users_utterance:
        st.locPreference, st.unsureloc = "west", False
    elif "east" in users_utterance:
        st.locPreference, st.unsureloc = "east", False
    elif matchLocation:
        stringLocation = re.split(r'\W', matchLocation.group(1))[-1]
        st.locPreference, st.unsureloc = spellcheck(stringLocation, 'area')
    return (st.locPreference,st.unsureloc)

""" Function: matchInfo; takes all global variables associated with preferences, and tries to modify them based on the user's input 
using one of the three 'fill' functions above"""
def matchInfo(users_utterance):
    #try to fill the variables for food, price and location with their unique function
    st.foodPreference, st.unsurefood = fillfood(users_utterance)
    st.pricePreference, st.unsureprice = fillprice(users_utterance)
    st.locPreference, st.unsureloc = fillarea(users_utterance)
    #print(users_utterance, st.foodPreference, st.pricePreference, st.locPreference, st.unsureprice, st.unsurefood, st.unsureloc)
    return (st.pricePreference, st.foodPreference, st.locPreference, st.unsureprice, st.unsurefood, st.unsureloc)