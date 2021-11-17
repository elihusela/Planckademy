import requests
import pandas as pd
import datetime

relevant_keys = ['dishId', 'dishName', 'dishDescription', 'dishPrice']


def start_log(path):
    test_time = open(path, 'w')
    test_time.truncate(0)
    test_time.close()


def check_update():
    '''
    Returns True if update is needed - meaning the txt file is empty or the date is older than one day.
    Returns False if the latest update date is today.
    '''

    with open("latest_update.txt") as f:
        contents = f.readlines()
    today = datetime.date.today()
    if not contents:
        print("Updating DB...")     # Might go to some server log instead of printing
        return True
    if str(today) != contents[0]:
        print("Updating DB...")     # Might go to some server log instead of printing
        return True
    return False


def get_db():
    '''
    Request the data from the relevant API.

    Parse is relevantly after I've learned the data format.

    Generate pandas dataframes for each type (drinks, pizzas, desserts) and leave in only the relevant info.

    Concatenate the dataframes and return them.

    Update the latest_update.txt file to today's date.

    Might be a place for error checking of the data - formats and other stuff.

    '''

    ########## Web Request  ##############
    API = "https://www.10bis.co.il/NextApi/GetRestaurantMenu?culture=en&uiCulture=en&restaurantId=19156&deliveryMethod=pickup"

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.68 Safari/537.36'
    }
    response = requests.get(API, headers=headers)

    menu_api = response.json()
    Data = menu_api['Data']
    C_list = Data['categoriesList']

    ################# Database generation   ###################
    for i in C_list:
        if i['categoryName'] == 'Drinks':
            Drinks = i['dishList']
        if i['categoryName'] == 'Pizzas':
            Pizzas = i['dishList']
        if i['categoryName'] == 'Desserts':
            Desserts = i['dishList']

    ######## Parsing ##########
    drinks_df = pd.DataFrame.from_dict(Drinks)
    for col in drinks_df.columns:
        if col not in relevant_keys:
            drinks_df.drop(columns=[col], inplace=True)
    drinks_df['dishType'] = 'Drink'

    pizzas_df = pd.DataFrame.from_dict(Pizzas)
    for col in pizzas_df.columns:
        if col not in relevant_keys:
            pizzas_df.drop(columns=[col], inplace=True)
    pizzas_df['dishType'] = 'Pizza'

    dessert_df = pd.DataFrame.from_dict(Desserts)
    for col in dessert_df.columns:
        if col not in relevant_keys:
            dessert_df.drop(columns=[col], inplace=True)
    dessert_df['dishType'] = 'Dessert'

    database = pd.concat([drinks_df, pizzas_df, dessert_df])

    ##########  Save update date  ################
    DATE = datetime.datetime.now().day
    test_time = open('latest_update.txt', 'w')
    test_time.truncate(0)
    test_time.close()

    test_time = open('latest_update.txt', 'a')
    today = datetime.date.today()
    test_time.write(str(today))
    test_time.close()

    return database

