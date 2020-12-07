import json
import requests
import time
import csv
from datetime import datetime
from utility.igdb_functions import *

# Script de carregamento da tabela de Jogos

# define enums para traducao do campo age_ratings
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

# Carrega dados do dataset VGS
vgs_games = []
with open('input_data/vgsales_unified.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        vgs_games.append(row)

# Para cada jogo do dataset, recupera informações na base do IGDB
requested_games = vgs_games
number_of_requested_games = len(requested_games)
endpoint = 'games'
wrapper = GetIGDBWrapper()
games = []  # lista de jogos a ser salva no arquivo de saida
games_count = 1
for vgs_game in requested_games:
    # Recupera chave do jogo do dataset
    game_basename = vgs_game['basename']
    game_basename = game_basename.replace('"', '\\"')

    # Faz requisição ao IGDB do jogo do dataset
    query = f""" fields name,slug,first_release_date,age_ratings.category,age_ratings.rating,franchise.name,game_modes.name;
            where slug = "{game_basename}";"""
    igdb_byte_array = RequestIGDB(wrapper, endpoint, query)
    games_list = json.loads(igdb_byte_array)    # array com 1 único jogo, se encontrado

    # Formatação e integração das informações do jogo
    game = {}
    if len(games_list) > 0: # se encontrou o jogo na base do IGDB
        igdb_game = games_list[0]

        game['Name'] = igdb_game['name']
        game['Basename'] = vgs_game['basename']

        if 'first_release_date' in igdb_game:
            release_timestamp = igdb_game['first_release_date']
            release_date = datetime.fromtimestamp(release_timestamp)
            game['Release Date'] = release_date.strftime("%d/%m/%Y")
        elif 'Year' in vgs_game:
            game['Release Date'] = f'00/00/' + vgs_game['Year'][0:4]
        else:
            game['Release Date'] = ''
        
        if 'age_ratings' in igdb_game:
            age_ratings = igdb_game['age_ratings'][0]
            rating = age_rating_category[age_ratings['category']] + "-" + age_rating_value[age_ratings['rating']]
            game['Age Rating'] = rating
        elif 'ESRB_Rating' in vgs_game:
            game['Age Rating'] = f'ESRB-' + vgs_game['ESRB_Rating']
        else:
            game['Age Rating'] = ''
        
        single_player = 0
        multi_player = 0
        if 'game_modes' in igdb_game:
            for game_mode in igdb_game['game_modes']:
                if(game_mode['name'] == "Single player"):
                    single_player = 1
                else:
                    multi_player = 1
            game['Single Player'] = single_player
            game['Multi Player'] = multi_player
        else:
            game['Single Player'] = ''
            game['Multi Player'] = ''
        
        if 'franchise' in igdb_game:
            game['Franchise'] = igdb_game['franchise']['name']
        else:
            game['Franchise'] = ''
    else:   # Se nao encontrou o jogo na base do IGDB, utiliza os dados do VGSales
        game['Name'] = vgs_game['Name']
        game['Basename'] = vgs_game['basename']
        
        if 'Year' in vgs_game:
            game['Release Date'] = f'00/00/' + vgs_game['Year'][0:4]
        else:
            game['Release Date'] = ''

        if 'ESRB_Rating' in vgs_game:
            game['Age Rating'] = f'ESRB-' + vgs_game['ESRB_Rating']
        else:
            game['Age Rating'] = ''
        
        game['Single Player'] = ''
        game['Multi Player'] = ''
        game['Franchise'] = ''
    
    games.append(game)
    time.sleep(0.25)

    print(f'{games_count}/{number_of_requested_games}')
    games_count = games_count + 1

with open('tables_data/games.csv', 'w', encoding='utf8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, games[0].keys())
    writer.writeheader()
    writer.writerows(games)