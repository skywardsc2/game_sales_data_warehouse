import os
import dotenv
import json
import requests
import time
import csv
from datetime import datetime
from igdb.wrapper import IGDBWrapper

dotenv.load_dotenv()

# make connection to igdb API via wrapper
twitch_id = os.environ.get("TWITCH_ID")
twitch_secret = os.environ.get("TWITCH_SECRET")
pload = {'client_id':twitch_id,
        'client_secret':twitch_secret,
        'grant_type':'client_credentials'}
twitch = requests.post('https://id.twitch.tv/oauth2/token', data=pload)

oAuth = twitch.json()

wrapper = IGDBWrapper(twitch_id, oAuth['access_token'])

# define enums for age rating
age_rating_category = {
    1: "ESRB",
    2: "PEGI"
}

age_rating_value = {
    1: "3",
    2: "7",
    3: "12",
    4: "16",
    5: "18",
    6: "RP",
    7: "EC",
    8: "E",
    9: "E10",
    10: "T",
    11: "M",
    12: "AO"
}

def RequestIGDB(wrapper, endpoint, query, result):
    result = wrapper.api_request(endpoint, query)
    return len(result)

endpoint = 'games'
offset = 0
query_limit = 500
requests_per_sec = 4
sleep_time = 1/requests_per_sec
entries_cnt = 0
number_of_entries = 20000
query = f""" fields name,first_release_date,age_ratings.category,age_ratings.rating,franchise.name,game_modes.name;
            where id = 1942;
            offset {offset};
            limit {query_limit};"""
games_byte_array = bytearray()
while RequestIGDB(wrapper, endpoint, query, games_byte_array) and entries_cnt < number_of_entries:
    games_dict = json.loads(games_byte_array)

    for item in games_dict:
        rating = age_rating_category[item['age_ratings'][0]['category']] + "-" + age_rating_value[item['age_ratings'][0]['rating']]
        item['age_ratings'] = rating
        
        release_date = datetime.fromtimestamp(item['first_release_date'])
        item['first_release_date'] = release_date.strftime("%d/%m/%Y")

        single_player = 0
        multi_player = 0
        for game_mode in item['game_modes']:
            if(game_mode['name'] == "Single player"):
                single_player = 1
            else:
                multi_player = 1
        item['single_player'] = single_player
        item['multi_player'] = multi_player
        item.pop('game_modes', None)
    
    with open('games.csv', 'a', encoding='utf8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, games_dict[0].keys())
        writer.writeheader()
        writer.writerows(games_dict)
    
    offset = offset + query_limit + 1
    number_of_entries = number_of_entries + query_limit
    time.sleep(sleep_time)
        

# games_byte_array = wrapper.api_request(
#     'games',
#     'fields name,first_release_date,age_ratings.category,age_ratings.rating,franchise.name,game_modes.name;where id = 1942;'
# )
# games_json = json.loads(games_byte_array)

# for item in games_json:
#     rating = age_rating_category[item['age_ratings'][0]['category']] + "-" + age_rating_value[item['age_ratings'][0]['rating']]
#     item['age_ratings'] = rating
    
#     release_date = datetime.fromtimestamp(item['first_release_date'])
#     item['first_release_date'] = release_date.strftime("%d/%m/%Y")

#     single_player = 0
#     multi_player = 0
#     for game_mode in item['game_modes']:
#         if(game_mode['name'] == "Single player"):
#             single_player = 1
#         else:
#             multi_player = 1
#     item['single_player'] = single_player
#     item['multi_player'] = multi_player
#     item.pop('game_modes', None)

# games_formatted = json.dumps(games_json, indent=4)
# print(games_formatted)

# game_age_rating_id = games_json[0]["age_ratings"][0]["id"]

# for item in age_ratings_json:
#     if item['id'] == game_age_rating_id:
#         print('Achou')

# print(len(age_ratings_json))

# age_rating = next(item for item in age_ratings_json if item['checksum'] == game_age_rating_id)
# print(age_rating)

# game_modes_byte_array = wrapper.api_request(
#     'game_modes',
#     'fields name;offset 7;'
# )
# game_modes_json = json.loads(game_modes_byte_array)
# game_modes_formatted = json.dumps(game_modes_json, indent=4)

# print(game_modes_formatted)
