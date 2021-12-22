import pandas as pd
import configure as conf
from random import randint
import statetransition as st


# Retrieves all restaurant information from csv file
restaurants = pd.read_csv('restaurantinfo.csv')
types = restaurants["food"]
prices = restaurants["pricerange"]
areas = restaurants["area"]
names = restaurants["restaurantname"]
address = restaurants["addr"]
phones = restaurants["phone"]
postcode = restaurants["postcode"]

"""Function: findplace; for finding a restaurant based on available information.
Puts together a list of all the restaurants matching the preferences, 
and then returns that list"""
def findplace(foodtype="nongiven", price="nongiven", location="nongiven"):
    if conf.lower_for_csv:
        foodtype = foodtype.lower()
        price = price.lower()
        location = location.lower()
    list_of_restaurants = []
    # if everything is given and there are some preferences given as 'any':
    if 'any' in {foodtype, price, location} and not('nongiven' in {foodtype, price, location}):
        if foodtype == price == location == 'any':
            for i in range(109):
                list_of_restaurants.append(names[i])
        elif foodtype == price == 'any':
            for i in range(109):
                if areas[i] == location:
                    list_of_restaurants.append(names[i])
        elif foodtype == location =='any':
            for i in range(109):
                if prices[i] == price:
                    list_of_restaurants.append(names[i])
        elif price == location == 'any':
            for i in range(109):
                if types[i] == foodtype:
                    list_of_restaurants.append(names[i])
        elif foodtype == 'any':
            for i in range(109):
                if prices[i] == price and areas[i] == location:
                    list_of_restaurants.append(names[i])
        elif price == 'any':
            for i in range(109):
                if types[i] == foodtype and areas[i] == location:
                    list_of_restaurants.append(names[i])
        elif location == 'any':
            for i in range(109):
                if types[i] == foodtype and prices[i] == price:
                    list_of_restaurants.append(names[i])
    elif foodtype != "nongiven": #if one of them is not given, or all of them are given and not 'any'
        if price != "nongiven":
            if location != "nongiven":
                for i in range(109):  # length of the restaurants csv
                    if types[i] == foodtype and prices[i] == price and areas[i] == location:
                        list_of_restaurants.append(names[i])
            else: # if foodtype and pricerange are given
                if 'any' in {foodtype, price}:
                    if foodtype == price:
                        for i in range(109):
                            list_of_restaurants.append(names[i])
                    elif foodtype == 'any':
                        for i in range(109):
                            if prices[i] == price:
                                list_of_restaurants.append(names[i])
                    elif price == 'any':
                        for i in range(109):
                            if types[i] == foodtype:
                                list_of_restaurants.append(names[i])
                else: #if foodtype and pricerange are given and both not 'any'
                    for i in range(109):  # length of the restaurants csv
                        if types[i] == foodtype and prices[i] == price:
                            list_of_restaurants.append(names[i])
        else: #if foodtype is given and price is not
            if location != "nongiven": #foodtype and location are given
                if 'any' in {foodtype, location}:
                    if foodtype == location:
                        for i in range(109):
                            list_of_restaurants.append(names[i])
                    elif foodtype == 'any':
                        for i in range(109):
                            if areas[i] == location:
                                list_of_restaurants.append(names[i])
                    elif location == 'any':
                        for i in range(109):
                            if types[i] == foodtype:
                                list_of_restaurants.append(names[i])
                else:
                    for i in range(109):  # length of the restaurants csv
                        if types[i] == foodtype and areas[i] == location:
                            list_of_restaurants.append(names[i])
            else: # if only foodtype is given, rest is not
                if foodtype == 'any':
                    for i in range(109):
                        list_of_restaurants.append(names[i])
                else:
                    for i in range(109):  # length of the restaurants csv
                        if types[i] == foodtype:
                            list_of_restaurants.append(names[i])
    elif price != "nongiven": 
        if location != "nongiven": # if price and location are given
            if 'any' in {price, location}:
                if price == location:
                    for i in range(109):
                        list_of_restaurants.append(names[i])
                elif price == 'any':
                    for i in range(109):
                        if areas[i] == location:
                            list_of_restaurants.append(names[i])
                elif location == 'any':
                    for i in range(109):
                        if prices[i] == price:
                            list_of_restaurants.append(names[i])
            else:
                for i in range(109):  # length of the restaurants csv
                    if prices[i] == price and areas[i] == location:
                        list_of_restaurants.append(names[i])
        else: # if only price is given
            if price == 'any':
                for i in range(109):
                    list_of_restaurants.append(names[i])
            else:
                for i in range(109):  # length of the restaurants csv
                    if prices[i] == price:
                        list_of_restaurants.append(names[i])
    elif location != "nongiven": #if only location is given
        if location == 'any':
            for i in range(109):
                list_of_restaurants.append(names[i])
        else: 
            for i in range(109):  # length of the restaurants csv
                if areas[i] == location:
                    list_of_restaurants.append(names[i])
    return (list_of_restaurants)

"""Function: all_info_decide; is called when all information has been given by the user, selects next state
input: list of restaurants; output: next state and system message"""
def all_info_decide(options):
    if len(options) > 1:
        k = randint(0, len(options) - 1)
        msg = "{} is a nice restaurant in the {} part of town serving {} food at {} prices".format(
            options[k], st.locPreference, st.foodPreference, st.pricePreference)
        st.name = options[k]
        return ("suggest_restaurant", msg)
    elif len(options) == 1:
        msg = "{} is a nice restaurant in the {} part of town serving {} food at {} prices".format(
            options[0], st.locPreference, st.foodPreference, st.pricePreference)
        st.name = options[0]
        return ("suggest_restaurant", msg)
    else:
        msg = "I am sorry, there is no restaurant in the {} part of town serving {} food at {} prices".format(
            st.locPreference, st.foodPreference, st.pricePreference)
        return ("apologise_not_finding", msg)

"""Function: two_infos_decide; is called when user has given 2 of 3 preferences, selects next state
input: list of restaurants; output: next state and system message"""
def two_infos_decide(options):
    if len(options) > 1:
        if st.locPreference=="nongiven":
            msg = "There are {} restaurants of {} type at {} price range, do you have a preference of the area? ".format(
                len(options), st.foodPreference, st.pricePreference)
            return ("unknown_info", msg)
        elif st.pricePreference=="nongiven":
            msg = "There are {} restaurants of {} type in the {} part of town, do you have a preference of the price range? ".format(
                len(options), st.foodPreference, st.locPreference)
            return ("unknown_info", msg)
        else:
            msg = "There are {} restaurants in the {} part of town at {} price range, do you have a preference of the food type? ".format(
                len(options), st.locPreference, st.pricePreference)
            return ("unknown_info", msg)
    elif len(options) == 1:
        if st.locPreference=="nongiven":
            msg = "{} is a nice restaurant serving {} food at {} prices".format(options[0],st.foodPreference,
                                                                                st.pricePreference)
        elif st.pricePreference=="nongiven":
            msg = "{} is a nice restaurant in the {} part of town serving {} food ".format(options[0],
                                                                                           st.locPreference,st.foodPreference)
        else:
            msg = "{} is a nice restaurant in the {} part of town with {} prices".format(options[0],
                                                                                         st.locPreference,st.pricePreference)
        st.name = options[0]
        return ("suggest_restaurant", msg)
    else:
        if st.locPreference=="nongiven":
            msg = "I am sorry, there is no restaurant  serving {} food at {} prices".format(st.foodPreference,
                                                                                        st.pricePreference)
        elif st.pricePreference == "nongiven":
            msg = "I am sorry, there is no restaurant  serving {} food in the {} part of town".format(st.foodPreference,
                                                                                        st.locPreference)
        else:
            msg = "I am sorry, there is no restaurant  in the {} part of town at {} prices".format(st.foodPreference,
                                                                                        st.pricePreference)
        return ("apologise_not_finding", msg)

"""Function: two_infos_decide_unknown; same as the previous one, 
but specific for the case when system is in unknown_info state, and 2 of 3 preferences are already given
input: list of restaurants; output: next state and system message"""
def two_infos_decide_unknown(options):
    if len(options) > 1:
        k = randint(0, len(options) - 1)
        if st.locPreference=="nongiven":
            msg = "{} is a nice restaurant serving {} food at {} prices".format(options[k],st.foodPreference,
                                                                                st.pricePreference)
        elif st.pricePreference=="nongiven":
            msg = "{} is a nice restaurant in the {} part of town serving {} food ".format(options[k],
                                                                                           st.locPreference,
                                                                                          st.foodPreference)
        else:
            msg = "{} is a nice restaurant in the {} part of town with {} prices".format(options[k],
                                                                                         st.locPreference, st.pricePreference)
        st.name = options[k]
        return ("suggest_restaurant", msg)
    elif len(options) == 1:
        if st.locPreference=="nongiven":
            msg = "{} is a nice restaurant serving {} food at {} prices".format(options[0],st.foodPreference,
                                                                                st.pricePreference)
        elif st.pricePreference=="nongiven":
            msg = "{} is a nice restaurant in the {} part of town serving {} food ".format(options[0],
                                                                                           st.locPreference,st.foodPreference)
        else:
            msg = "{} is a nice restaurant in the {} part of town with {} prices".format(options[0],
                                                                                         st.locPreference,st.pricePreference)
        st.name = options[0]
        return ("suggest_restaurant", msg)
    else:
        if st.locPreference=="nongiven":
            msg = "I am sorry, there is no restaurant  serving {} food at {} prices".format(st.foodPreference,
                                                                                        st.pricePreference)
        elif st.pricePreference == "nongiven":
            msg = "I am sorry, there is no restaurant  serving {} food in the {} part of town".format(st.foodPreference,
                                                                                        st.locPreference)
        else:
            msg = "I am sorry, there is no restaurant  in the {} part of town at {} prices".format(st.foodPreference,
                                                                                        st.pricePreference)
        return ("apologise_not_finding", msg)

"""Function: one_info_decide; is called when user has given 1 of 3 preferences, selects next state
input: list of restaurants; output: next state and system message"""
def one_info_decide(options):
    if len(options) > 1:
        if st.foodPreference != 'nongiven':
            msg = "There are {} restaurants serving {} food, do you have a preference in price range or area ?".format(len(options),st.foodPreference)
        elif st.pricePreference != 'nongiven':
            msg = "There are {} restaurants at {} price range, do you have a preference in food type or area ?".format(len(options), st.pricePreference)
        else:
            msg = "There are {} restaurants in the {} part of the city , do you have a preference in price range or food type ?".format(len(options), st.locPreference)
        return ("unknown_info", msg)
    elif len(options) == 1:
        if st.foodPreference != 'nongiven':
            msg = "{} is a nice restaurant serving {} food ".format(options[0],st.foodPreference)
        elif st.pricePreference != 'nongiven':
            msg = "{} is a nice restaurant with {} prices".format(options[0], st.pricePreference)
        else:
            msg = "{} is a nice restaurant in the {} part of town ".format(options[0], st.locPreference)
        st.name = options[0]
        return ("suggest_restaurant", msg)
    else:
        if st.locPreference != "nongiven":
            msg = "I am sorry, there is no restaurant in the {} part of town ".format(st.locPreference)
        elif st.pricePreference != "nongiven":
            msg = "I am sorry, there is no restaurant serving food at {} prices".format(st.pricePreference)
        else:
            msg = "I am sorry, there is no restaurant serving {} food ".format(st.foodPreference)
        return ("apologise_not_finding", msg)

"""Function: one_info_decide; same as the previous one, 
but specific for the case when system is in unknown_info state, and 1 of 3 preferences is already given
input: list of restaurants; output: next state and system message"""
def one_info_decide_unknown(options):
    if len(options) > 1:
        k = randint(0, len(options) - 1)
        if st.foodPreference != 'nongiven':
            msg = "{} is a nice restaurant serving {} food ".format(options[k],st.foodPreference)
        elif st.pricePreference != 'nongiven':
            msg = "{} is a nice restaurant with {} prices".format(options[k], st.pricePreference)
        else:
            msg = "{} is a nice restaurant in the {} part of town ".format(options[k], st.locPreference)
        st.name = options[k]
        return ("suggest_restaurant", msg)
    elif len(options) == 1:
        if st.foodPreference != 'nongiven':
            msg = "{} is a nice restaurant serving {} food ".format(options[0],st.foodPreference)
        elif st.pricePreference != 'nongiven':
            msg = "{} is a nice restaurant with {} prices".format(options[0], st.pricePreference)
        else:
            msg = "{} is a nice restaurant in the {} part of town ".format(options[0], st.locPreference)
        st.name = options[0]
        return ("suggest_restaurant", msg)
    else:
        if st.locPreference != "nongiven":
            msg = "I am sorry, there is no restaurant in the {} part of town ".format(st.locPreference)
        elif st.pricePreference != "nongiven":
            msg = "I am sorry, there is no restaurant serving food at {} prices".format(st.pricePreference)
        else:
            msg = "I am sorry, there is no restaurant serving {} food ".format(st.foodPreference)
        return ("apologise_not_finding", msg)

"""Function: give_info; when requested, for giving specific information on a restaurant accepted by the user"""
def give_info(req1):
    for i in range(len(address)):
        if st.name == names[i]:
            if req1 == "addr":
                return (address[i])
            if req1 == "postcode":
                return (postcode[i])
            if req1 == "phone":
                return (phones[i])
            if req1 == "area":
                return (areas[i])
            if req1 == "price":
                return (prices[i])
            if req1 == "food":
                return (types[i])
