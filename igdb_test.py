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

with open('games.csv', 'w', encoding='utf8', newline='') as csvfile:
    pass

endpoint = 'games'
offset = 0
query_limit = 500   # numero de entradas por request (maximo: 500)
entries_cnt = 0
number_of_entries = 1   # numero de entradas desejado
query = f""" fields name,slug,first_release_date,age_ratings.category,age_ratings.rating,franchise.name,game_modes.name;
            where id = 1942;
            offset {offset};
            limit {query_limit};"""

wrapper = GetIGDBWrapper()
games_byte_array = RequestIGDB(wrapper, endpoint, query)
game_dicts = json.loads(games_byte_array)
csv_keys = []
while len(game_dicts) and entries_cnt < number_of_entries:

    # formata campos ou adiciona os que faltam
    game_dicts_formatted = []
    for game_dict in game_dicts:
        # seleciona apenas os campos desejados
        keys = ['name', 'slug', 'first_release_date', 'age_ratings', 'franchise', 'game_modes']
        game_dict_formatted = { key: game_dict[key] for key in keys if key in game_dict }

        if 'first_release_date' in game_dict_formatted and game_dict_formatted['first_release_date'] > 0:
            release_timestamp = game_dict_formatted['first_release_date']
            release_date = datetime.fromtimestamp(release_timestamp)
            game_dict_formatted['first_release_date'] = release_date.strftime("%d/%m/%Y")
        else:
            game_dict_formatted['first_release_date'] = 'null'
        
        if 'age_ratings' in game_dict_formatted:
            age_ratings = game_dict_formatted['age_ratings'][0]
            rating = age_rating_category[age_ratings['category']] + "-" + age_rating_value[age_ratings['rating']]
            game_dict_formatted['age_ratings'] = rating
        else:
            game_dict_formatted['age_ratings'] = 'null'
        
        
        single_player = 0
        multi_player = 0
        if 'game_modes' in game_dict_formatted:
            for game_mode in game_dict_formatted['game_modes']:
                if(game_mode['name'] == "Single player"):
                    single_player = 1
                else:
                    multi_player = 1
            game_dict_formatted['single_player'] = single_player
            game_dict_formatted['multi_player'] = multi_player
            game_dict_formatted.pop('game_modes', None)
        else:
            game_dict_formatted['single_player'] = 'null'
            game_dict_formatted['multi_player'] = 'null'
        
        if 'franchise' in game_dict_formatted:
            game_dict_formatted['franchise'] = game_dict_formatted['franchise']['name']
        else:
            game_dict_formatted['franchise'] = 'null'
        
        # adiciona jogo formatado à lista
        game_dicts_formatted.append(game_dict_formatted)
    
    if entries_cnt == 0:
        csv_keys = game_dicts_formatted[0].keys()
        
    # escreve no arquivo .csv
    with open('games.csv', 'a', encoding='utf8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, csv_keys)
        if entries_cnt == 0:
            writer.writeheader()
        writer.writerows(game_dicts_formatted)
    
    offset = offset + query_limit + 1
    entries_cnt = entries_cnt + query_limit

    # delay para não ultrapassar o limite de requests por segundo
    time.sleep(0.25)
    print(entries_cnt)
    print(game_dict_formatted)

    # calcula quantidade de tuplas faltantes
    if number_of_entries - entries_cnt > 0 and number_of_entries - entries_cnt < query_limit:
        query_limit = number_of_entries - entries_cnt
    
    # faz novo request
    query = f""" fields name,first_release_date,age_ratings.category,age_ratings.rating,franchise.name,game_modes.name;
            offset {offset};
            limit {query_limit};"""
    games_byte_array = RequestIGDB(wrapper, endpoint, query)
    game_dicts = json.loads(games_byte_array)