import json
import time
import csv
from datetime import datetime
from igdb_functions import *

# Script de teste para requisicoes ao IGDB

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

endpoint = 'games'
offset = 0
query_limit = 500   # numero de entradas por request (maximo: 500)
entries_cnt = 0
number_of_entries = 1   # numero de entradas desejado
query = f""" fields name,slug,involved_companies.company.name,involved_companies.developer;
            where id = 1942;
            offset {offset};
            limit {query_limit};"""

wrapper = GetIGDBWrapper()
games_byte_array = RequestIGDB(wrapper, endpoint, query)
game_dicts = json.loads(games_byte_array)
while len(game_dicts) and entries_cnt < number_of_entries:
    entries = len(game_dicts)

    offset = offset + entries + 1
    entries_cnt = entries_cnt + entries

    print(entries_cnt)
    pretty_game_dicts = json.dumps(game_dicts, indent=4)
    print(pretty_game_dicts)

    # calcula quantidade de tuplas faltantes
    if number_of_entries - entries_cnt > 0 and number_of_entries - entries_cnt < query_limit:
        query_limit = number_of_entries - entries_cnt
    
    # faz novo request
    # delay para não ultrapassar o limite de requests por segundo
    time.sleep(0.25)
    query = f""" fields name,first_release_date,age_ratings.category,age_ratings.rating,franchise.name,game_modes.name;
            offset {offset};
            limit {query_limit};"""
    games_byte_array = RequestIGDB(wrapper, endpoint, query)
    game_dicts = json.loads(games_byte_array)