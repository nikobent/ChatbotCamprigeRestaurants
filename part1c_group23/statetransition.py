import pickle
import dialogparser as dpars
from dialogparser import substring as fs
import retriever as rtvr
import configure
from sklearn.neighbors import KNeighborsClassifier as KN
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from random import randint
from dialogparser import data

global msg, locPreference, foodPreference, pricePreference, name, options, unsureloc, unsureprice, unsurefood

# MACHINE LEARNING CLASSIFIER --- We have pickled our vectorizer, transformer and classifier from part1b
filename1, filename2, filename3 = 'vectorizer.sav', 'transformer.sav', 'model.sav'
vec = pickle.load(open(filename1, 'rb'))
tf_transformer = pickle.load(open(filename2, 'rb'))
tf_transformer.n_jobs = 1
clf = pickle.load(open(filename3, 'rb'))
clf.n_jobs = 1

# BASELINE SYSTEM FOR CLASSIFYING DIALOG --- Can be turned on or off in the configure.py file
"""Implementation of baseline1 for classification"""
def baseline(my_var):
    liss =[]
    if "okay" in my_var or "good" in my_var or "fine" in my_var or "kay" in my_var or "great" in my_var or "thatll do" in my_var:
        liss.append("ack ")
    elif "is it" in my_var or "does it"  in my_var or "is there" in my_var or "is that" in my_var or "is this" in my_var:
        liss.append("confirm ")
    elif "repeat" in my_var or "again" in my_var or "back" in my_var:
        liss.append("repeat ")
    elif "more" in my_var:
        liss.append("reqmore ")
    elif "start" in my_var or "reset" in my_var:
        liss.append("restart ")
    elif "thank you" in my_var or "thanks" in my_var:
        liss.append("thankyou ")
    elif "yes" in my_var or "right" in my_var or "yea" in my_var or "uh huh" in my_var or "y " in my_var:
        liss.append("affirm ")
    elif "goodbye" in my_var or "bye" in my_var:
        liss.append("bye ")
    elif "not" in my_var or "dont want" in my_var or "wrong" in my_var or "change" in my_var:
        liss.append("deny ")
    elif "hello" in my_var or "hi" in my_var or "halo" in my_var:
        liss.append("hello ")
    elif "how about" in my_var or "else" in my_var or "anything" in my_var:
        liss.append("reqalts ")
    elif "looking" in my_var or "food" in my_var or "i dont care" in my_var or "south" in my_var or "west" in my_var or "north" in my_var or "east" in my_var or "spanish" in my_var or "french" in my_var or "chinese" in my_var or "asian" in my_var:
        liss.append("inform ")
    elif "expansive " in my_var or "moderate" in my_var or "cheap" in my_var or "any area" in my_var or "center" in my_var or "doesnt matter" in my_var or "any kind" in my_var or "traditional" in my_var or "barbecue" in my_var:
        liss.append("inform ")
    elif "no " in my_var:
        liss.append("negate")
    elif "what" in my_var or "whats" in my_var or "may" in my_var or "can you" in my_var or "adress" in my_var or "post code" in my_var or "phone number" in my_var or "price range" in my_var:
        liss.append("request4 ")
    else:
        liss.append("null ")
    return(liss[0])

#STATE TRANSITION FUNCTION
"""State transition function, with initial/default state = welcome_msg
output:next_state, utterance from the system"""
def state_transition(users_utterance, current_state="welcome_msg"):
    global msg, locPreference, foodPreference, pricePreference, name, options, unsureloc, unsureprice, unsurefood
    users_utterance = users_utterance.lower()
    if (users_utterance == "editconfig"):
        configure.editconf()
        msg = "Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?"
        locPreference, foodPreference, pricePreference, name = "nongiven", "nongiven", "nongiven", "nongiven"
        return ("restart", msg)
    if (users_utterance == "thank you goodbye"):
        return ("exit_program", "GOODBYE")
    if (users_utterance == "restart" or users_utterance == "reset"):
        msg = "Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?"
        locPreference, foodPreference, pricePreference, name = "nongiven", "nongiven", "nongiven", "nongiven"
        return ("restart", msg)
    if configure.use_baseline:
        act_pred = baseline(users_utterance)
    else:
        phrase_count = vec.transform([users_utterance])
        phrase_tf = tf_transformer.transform(phrase_count)
        act_pred = clf.predict(phrase_tf)
    """Here we handle the repeat and restart act's from the user
    these acts require straight forward actions"""
    if act_pred == "repeat ":
        return (current_state, msg)
    if configure.allow_restart:
        if act_pred == "restart ":
            msg = "Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?"
            locPreference, foodPreference, pricePreference, name = "nongiven", "nongiven", "nongiven", "nongiven"
            unsurefood, unsureloc, unsureprice = False, False, False
            return ("restart", msg)
    if act_pred == "bye " or act_pred == "thankyou ":
        return ("exit_program", "Thank you goodbye")
    # Welcome message state (also, see state transition diagram). 2 options: user provides information; user does not provide information.
    if current_state == 'welcome_msg':
        """Option 1: user provides information which is checked, and when valid provides user with a count of restaurants if there are any.
        When unsure about the information, the system goes to the 'confirmation needed' stage."""
        if act_pred == "inform ":
            dpars.matchInfo(users_utterance)#global variables, no need to catch the return
            if (unsurefood or unsureloc or unsureprice) and configure.ask_correct_lev:
                if unsurefood:
                    msg = "Do you mean {} restaurant ?".format(foodPreference)
                elif unsureprice:
                    msg = "Do you mean a restaurant with {} price range?".format(pricePreference)
                elif unsureloc:
                    msg = "Do you mean a restaurant in the {} part of town".format(locPreference)
                return ("confirmation_need", msg)
            elif foodPreference != "nongiven" and pricePreference != "nongiven" and locPreference != "nongiven":
                options = rtvr.findplace(foodtype=foodPreference, price=pricePreference, location=locPreference)
                state, msg = rtvr.all_info_decide(options)
                return (state, msg)
            elif foodPreference != "nongiven" and pricePreference != "nongiven":
                options = rtvr.findplace(foodtype=foodPreference, price=pricePreference)
                if configure.offering_from_begin:
                    state, msg = rtvr.two_infos_decide_unknown(options)
                else:
                    state, msg = rtvr.two_infos_decide(options)
                return (state, msg)
            elif foodPreference != "nongiven" and locPreference != "nongiven":
                options = rtvr.findplace(foodtype=foodPreference, location=locPreference)
                if configure.offering_from_begin:
                    state, msg = rtvr.two_infos_decide_unknown(options)
                else:
                    state, msg = rtvr.two_infos_decide(options)
                return (state, msg)
            elif pricePreference != "nongiven" and locPreference != "nongiven":
                options = rtvr.findplace(price=pricePreference, location=locPreference)
                if configure.offering_from_begin:
                    state, msg = rtvr.two_infos_decide_unknown(options)
                else:
                    state, msg = rtvr.two_infos_decide(options)
                return (state, msg)
            elif foodPreference != "nongiven":
                options = rtvr.findplace(foodtype=foodPreference)
                if configure.offering_from_begin:
                    state, msg = rtvr.one_info_decide_unknown(options)
                else:
                    state, msg = rtvr.one_info_decide(options)
                return (state,msg)
            elif pricePreference != "nongiven":
                options = rtvr.findplace(price=pricePreference)
                if configure.offering_from_begin:
                    state, msg = rtvr.one_info_decide_unknown(options)
                else:
                    state, msg = rtvr.one_info_decide(options)
                return (state,msg)
            elif locPreference != "nongiven":
                options = rtvr.findplace(location=locPreference)
                if configure.offering_from_begin:
                    state, msg = rtvr.one_info_decide_unknown(options)
                else:
                    state, msg = rtvr.one_info_decide(options)
                return (state,msg)
                #Option 2: If user didnt give any information, system asks for it
            else:
                msg = "What type of food would you like?"
                return ("unknown_info", msg)
        else:
            msg = "What type of food would you like?"
            return ("unknown_info", msg)
    # Confirmation State; user confirms or does not confirm information that the system was unsure about.
    elif current_state == 'confirmation_need':
        """When information is confirmed, system corrects the value of unsure variables, 
            and proceeds to providing restaurant options for the user. """
        if act_pred == "ack " or act_pred == "affirm ":
            if foodPreference != "nongiven":
                unsurefood = False
            if pricePreference != "nongiven":
                unsurefood = False
            if locPreference != "nongiven":
                unsurefood = False
            if foodPreference != "nongiven" and pricePreference != "nongiven" and locPreference != "nongiven":
                options = rtvr.findplace(foodtype=foodPreference, price=pricePreference, location=locPreference)
                state, msg = rtvr.all_info_decide(options)
                return (state, msg)
            elif foodPreference != "nongiven" and pricePreference != "nongiven":
                options = rtvr.findplace(foodtype=foodPreference, price=pricePreference)
                state, msg = rtvr.two_infos_decide(options)
                return (state,msg)
            elif foodPreference != "nongiven" and locPreference != "nongiven":
                options = rtvr.findplace(foodtype=foodPreference, location=locPreference)
                state, msg = rtvr.two_infos_decide(options)
                return (state,msg)
            elif pricePreference != "nongiven" and locPreference != "nongiven":
                options = rtvr.findplace(price=pricePreference, location=locPreference)
                state, msg = rtvr.two_infos_decide(options)
                return (state,msg)
            elif foodPreference != "nongiven":
                options = rtvr.findplace(foodtype=foodPreference)
                state, msg = rtvr.one_info_decide(options)
                return (state,msg)
            elif pricePreference != "nongiven":
                options = rtvr.findplace(price=pricePreference)
                state, msg = rtvr.one_info_decide(options)
                return (state,msg)
            elif locPreference != "nongiven":
                options = rtvr.findplace(location=locPreference)
                state, msg = rtvr.one_info_decide(options)
                return (state,msg)
            """When user denied information, or otherwise did not confirm, the system checks what info it was unsure about, resets that particular preference,
            and asks user for new information concerning that preference."""
        elif act_pred == "deny " or act_pred == "negate ":
            if unsurefood:
                foodPreference = "nongiven"
                msg = "What kind of food would you like?"
                return ("unknown_info", msg)
            elif unsureprice:
                pricePreference = "nongiven"
                msg = "What kind of price range would you like?"
                return ("unknown_info", msg)
            elif unsureloc:
                locPreference = "nongiven"
                msg = "Where in the city would you like to eat?"
                return ("unknown_info", msg)
        else:
            return (current_state, msg)
    #Apologise_not_finding state: if no restaurant is found, system waits for new information or repeats apology.
    elif current_state == 'apologise_not_finding':
        """ In accordance with the diagram: code below makes sure to confirm any new information given in apologise_state,
        so it immediatly transitions to confirmation-need state"""
        if act_pred == "inform ":
            locPreference, foodPreference, pricePreference = "nongiven", "nongiven", "nongiven"
            dpars.matchInfo(users_utterance)
            unsurefood = True if foodPreference != 'nongiven' else False
            unsureprice = True if pricePreference != 'nongiven' else False
            unsureloc = True if locPreference != 'nongiven' else False
            if unsurefood or unsureloc or unsureprice:
                if unsurefood:
                    msg = "Do you mean {} restaurant ?".format(foodPreference)
                elif unsureprice:
                    msg = "Do you mean a restaurant with {} price range?".format(pricePreference)
                elif unsureloc:
                    msg = "Do you mean a restaurant in the {} part of town".format(locPreference)
                return ("confirmation_need", msg)
        else:
            return (current_state, msg)
    #Suggest_restaurant state: system suggests restaurant, then wait for user input: confirm, deny, request info, or
    elif current_state == 'suggest_restaurant':
        """If our suggestion gets denied we offer a new one if the list has any other option to offer.
            we get a new K and we check if it is the same as before using the variable name that we assign
            before making a suggestion, to make sure a different restaurant is suggested, proceeds to suggest_restaurant state"""
        if act_pred == 'deny ' or act_pred == 'negate ' or act_pred == "reqmore " or act_pred == "reqalts ":
            if len(options) > 1:
                k_unique = True
                while (k_unique):
                    k = randint(0, len(options) - 1)
                    if options[k] != name:
                        k_unique = False
                        name = options[k]
                msg = "{} in another option for you".format(name)
                return ("suggest_restaurant", msg)
            else:
                msg = "I am sorry there is no other restaurant following your preferences"
                return ("apologise_not_finding", msg)
            """If our suggestion is accepted we stay at the same state and wait from the user another action"""
        elif act_pred == "ack " or act_pred == "affirm ":
            msg = "I'm glad that you like the restaurant. If you need more info about the restaurant, please ask."
            return (current_state, msg) # Upon request, specific information about the suggested restaurant is provided, proceeds to restaurant_info state
        elif act_pred == "request ":
            if "post" in users_utterance and "code" in users_utterance:
                info = rtvr.give_info("postcode")
                msg = "The post code is {}".format(info)
            elif "address" in users_utterance or "location" in users_utterance:
                info = rtvr.give_info("addr")
                msg = "The address is {}".format(info)
            elif "phone" in users_utterance or "number" in users_utterance or "telephone" in users_utterance:
                info = rtvr.give_info("phone")
                msg = "The phone number is {}".format(info)
            elif "area" in users_utterance:
                info = rtvr.give_info("area")
                msg = "The area is {} of the city".format(info)
            elif "price" in users_utterance:
                info = rtvr.give_info("price")
                msg = "The price range is {}".format(info)
            elif "food" in users_utterance or "type" in users_utterance:
                info = rtvr.give_info("food")
                msg = "The restaurant is serving {} food".format(info)
            return ("restaurant_info", msg)
        # User asks question about information on a suggested restaurant, system answers with confirmation or negation, proceeds to restaurant_info state
        elif act_pred == "confirm ":
            for word in data['informable']["food"]:
                if word in users_utterance:
                    conf = True if rtvr.give_info("food") == word else False
                    if conf:
                        msg = "I can confirm that"
                    else:
                        msg = "This is incorrect, the food type is {}".format(rtvr.give_info('food'))
                    return ("restaurant_info", msg)
            for word in data['informable']["pricerange"]:
                if word in users_utterance:
                    conf = True if rtvr.give_info("price") == word else False
                    if conf:
                        msg = "I can confirm that"
                    else:
                        msg = "This is incorrect, the price range is {}".format(rtvr.give_info("price"))
                    return ("restaurant_info", msg)
            for word in data['informable']["area"]:
                if word in users_utterance:
                    conf = True if rtvr.give_info("area") == word else False
                    if conf:
                        msg = "I can confirm that"
                    else:
                        msg = "This is incorrect, the area is {}".format(rtvr.give_info("area"))
                    return ("restaurant_info", msg)
        else:
            return (current_state, msg)
    #Restaurant_info state: Suggested restaurant is accepted by user and system waits for user input.
    elif current_state == 'restaurant_info':
        """ User asks for logistic or contact information on suggested restaurant """
        if act_pred == "request ":
            if "post" in users_utterance and "code" in users_utterance:
                info = rtvr.give_info("postcode")
                msg = "The post code is {}".format(info)
            elif "address" in users_utterance or "location" in users_utterance:
                info = rtvr.give_info("addr")
                msg = "The address is {}".format(info)
            elif "phone" in users_utterance or "number" in users_utterance or "telephone" in users_utterance:
                info = rtvr.give_info("phone")
                msg = "The phone number is {}".format(info)
            elif "area" in users_utterance:
                info = rtvr.give_info("area")
                msg = "The area is {} of the city".format(info)
            elif "price" in users_utterance:
                info = rtvr.give_info("price")
                msg = "The price range is {}".format(info)
            elif "food" in users_utterance or "type" in users_utterance:
                info = rtvr.give_info("food")
                msg = "The restaurant is serving {} food".format(info)
            return ("restaurant_info", msg)
            # User asks about any of the three restaurant properties (foodtype, price, area)
        elif act_pred == "confirm ":
            for word in data['informable']["food"]:
                if word in users_utterance:
                    conf = True if rtvr.give_info("food") == word else False
                    if conf:
                        msg = "I can confirm that"
                    else:
                        msg = "This is incorrect, the food type is {}".format(rtvr.give_info('food'))
                    return ("restaurant_info", msg)
            for word in data['informable']["pricerange"]:
                if word in users_utterance:
                    conf = True if rtvr.give_info("price") == word else False
                    if conf:
                        msg = "I can confirm that"
                    else:
                        msg = "This is incorrect, the price range is {}".format(rtvr.give_info("price"))
                    return ("restaurant_info", msg)
            for word in data['informable']["area"]:
                if word in users_utterance:
                    conf = True if rtvr.give_info("area") == word else False
                    if conf:
                        msg = "I can confirm that"
                    else:
                        msg = "This is incorrect, the area is {}".format(rtvr.give_info("area"))
                    return ("restaurant_info", msg)
            """ Other input: system repeats suggestion, returns to suggest_restaurant state """
        else:
            msg = "{} is a restaurant that fullfils your preferences".format(name)
            return ("suggest_restaurant", msg)
    #Unknown_info state: system checks all information given, proceeds to confirmation_need if unsure, or to suggest_restaurant or apologise_not_finding if sure.
    elif current_state == 'unknown_info':
        """ Check which of the three preferences the user has given, and assign that to the appropriate global variable , or reset to 'any' when no info is given"""
        if act_pred == 'inform ' or act_pred == 'deny ' or act_pred == 'negate ':  
            if foodPreference == 'nongiven':
                if fs('any',users_utterance) or fs('no', users_utterance):
                    foodPreference = 'any'
                    options = rtvr.findplace(foodtype=foodPreference, price=pricePreference, location=locPreference)
                    if 'nongiven' in {pricePreference, locPreference}:
                        if pricePreference == locPreference:
                            state , msg = rtvr.one_info_decide(options)
                        else:
                            state, msg = rtvr.two_infos_decide(options)
                    else:
                        state,msg = rtvr.all_info_decide(options)
                    return(state,msg)
                else:
                    foodPreference, unsurefood = dpars.fillfood(users_utterance)
            if pricePreference == 'nongiven': #food is given, price is not
                if fs('any',users_utterance) or fs('no', users_utterance):
                    pricePreference = 'any'
                    options = rtvr.findplace(foodtype=foodPreference, price=pricePreference, location=locPreference)
                    if 'nongiven' in {foodPreference, locPreference}:
                        if foodPreference == locPreference:
                            state , msg = rtvr.one_info_decide(options)
                        else:
                            state, msg = rtvr.two_infos_decide(options)
                    else:
                        state,msg = rtvr.all_info_decide(options)
                    return(state,msg)
                else:
                    pricePreference, unsureprice = dpars.fillprice(users_utterance)
            if locPreference == 'nongiven': #food and price given, location is not
                if fs('any',users_utterance) or fs('no', users_utterance):
                    locPreference = 'any'
                    options = rtvr.findplace(foodtype=foodPreference, price=pricePreference, location=locPreference)
                    if 'nongiven' in {pricePreference, foodPreference}:
                        if pricePreference == foodPreference:
                            state , msg = rtvr.one_info_decide(options)
                        else:
                            state, msg = rtvr.two_infos_decide(options)
                    else:
                        state,msg = rtvr.all_info_decide(options)
                    return(state,msg)
                else:
                    locPreference, unsureloc = dpars.fillarea(users_utterance)
            """ If unsure, ask for confirmation and proceed to confirmation_need state """
            if (unsurefood or unsureloc or unsureprice) and configure.ask_correct_lev:
                if unsurefood:
                    msg = "Do you mean {} restaurant ?".format(foodPreference)
                elif unsureprice:
                    msg = "Do you mean a restaurant with {} price range?".format(pricePreference)
                elif unsureloc:
                    msg = "Do you mean a restaurant in the {} part of town".format(locPreference)
                return ("confirmation_need", msg)
                # When sure, system tries to suggest restaurant based on the information available (given by user)
            elif not('nongiven' in {foodPreference, pricePreference, locPreference}):
                options = rtvr.findplace(foodtype=foodPreference, price=pricePreference, location=locPreference)
                state , msg = rtvr.all_info_decide(options)
                return (state, msg)
            elif not('nongiven' in {foodPreference, pricePreference}):
                options = rtvr.findplace(foodtype=foodPreference, price=pricePreference)
                state,msg = rtvr.two_infos_decide(options)
                return (state,msg)
            elif not('nongiven' in {foodPreference, locPreference}):
                options = rtvr.findplace(foodtype=foodPreference, location=locPreference)
                state, msg = rtvr.two_infos_decide(options)
                return (state, msg)
            elif not('nongiven' in {pricePreference, locPreference}):
                options = rtvr.findplace(price=pricePreference, location=locPreference)
                state, msg = rtvr.two_infos_decide(options)
                return (state, msg)
            elif foodPreference != "nongiven":
                options = rtvr.findplace(foodtype=foodPreference)
                state, msg = rtvr.one_info_decide(options)
                return (state, msg)
            elif pricePreference != "nongiven":
                options = rtvr.findplace(price=pricePreference)
                state, msg = rtvr.one_info_decide(options)
                return (state, msg)
            elif locPreference != "nongiven":
                options = rtvr.findplace(location=locPreference)
                state, msg = rtvr.one_info_decide(options)
                return (state, msg)
            """ If no information is available, previous msg is repeated, system stays in this state until (unsure) information is given """
        else:
            return (current_state, msg)