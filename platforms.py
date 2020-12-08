import json
import requests
import time
import csv
from datetime import datetime
from utility.igdb_functions import *

# Dictionary com lista de plataformas únicas do vgsales.csv e seus nomes como consta no IGDB
from utility.platform_name_integration import PlatformNameConverter 

# Script de carregamento da tabela de Plataformas

# Para cada jogo do dataset, recupera informações na base do IGDB
endpoint = 'platforms'
wrapper = GetIGDBWrapper()

entries_cnt = 1
number_of_platforms = len(PlatformNameConverter)
platforms = []  # lista de plataformas a ser salva no arquivo de saida
for platform_name in PlatformNameConverter.keys():
    # Faz requisição das informações da plataforma ao IGDB
    query = f"""fields name, generation, platform_family.name, versions.platform_version_release_dates.date;
            where name = "{PlatformNameConverter[platform_name]}";"""
    igdb_byte_array = RequestIGDB(wrapper, endpoint, query)
    platforms_list = json.loads(igdb_byte_array)    # array com 1 única plataforma, se encontrada

    # Formatação e integração das informações da plataforma
    platform = {}
    if len(platforms_list) > 0: # se encontrou a plataforma na base do IGDB
        igdb_platform = platforms_list[0]

        platform['name'] = platform_name
        platform['abbreviation'] = platform_name
        platform['first_release_date'] = ''
        platform['generation'] = ''
        platform['family'] = ''

        if 'name' in igdb_platform:
            platform['name'] = igdb_platform['name']

        if 'versions' in igdb_platform:
            version = igdb_platform['versions'][0]
            if 'platform_version_release_dates' in version:
                # recupera primeira data de lançamento da plataforma
                version_release_dates = []
                for release_date in version['platform_version_release_dates']:
                    if 'date' in release_date:
                        version_release_dates.append(release_date['date'])
                version_release_dates.sort()
                release_timestamp = version_release_dates[0]
                release_date = datetime.fromtimestamp(release_timestamp)
                platform['first_release_date'] = release_date.strftime("%d/%m/%Y")
        
        if 'generation' in igdb_platform:
            platform['generation'] = igdb_platform['generation']
        
        if 'platform_family' in igdb_platform:
            if 'name' in igdb_platform['platform_family']:
                platform['family'] = igdb_platform['platform_family']['name']
    
    platforms.append(platform)
    time.sleep(0.25)

    print(f'{entries_cnt}/{number_of_platforms}')
    entries_cnt = entries_cnt + 1

with open(f'tables_data/{endpoint}.csv', 'w', encoding='utf8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, platforms[0].keys())
    writer.writeheader()
    writer.writerows(platforms)