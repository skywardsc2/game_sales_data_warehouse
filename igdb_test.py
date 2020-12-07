import json
import time
import csv
from datetime import datetime
from utility.igdb_functions import *

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

endpoint = 'platforms'
offset = 0
query_limit = 500   # numero de entradas por request (maximo: 500)
query = f"""fields name, generation, platform_family.name, versions.platform_version_release_dates.date;
            offset {offset};
            limit {query_limit};"""
wrapper = GetIGDBWrapper()
byte_array = RequestIGDB(wrapper, endpoint, query)
dicts = json.loads(byte_array)

max_entries_cnt = 1   # numero de entradas desejado
entries_cnt = 0
while len(dicts) and entries_cnt < max_entries_cnt:
    count = len(dicts)

    offset = offset + count + 1
    entries_cnt = entries_cnt + count

    pretty_dicts = json.dumps(dicts, indent=4)
    print(pretty_dicts)
    print(entries_cnt)

    # calcula quantidade de tuplas faltantes
    if max_entries_cnt - entries_cnt > 0 and max_entries_cnt - entries_cnt < query_limit:
        query_limit = max_entries_cnt - entries_cnt
    
    # faz novo request
    # delay para não ultrapassar o limite de requests por segundo
    time.sleep(0.25)
    query = f""" fields name, abbreviation, versions.name;
            offset {offset};
            limit {query_limit};"""
    byte_array = RequestIGDB(wrapper, endpoint, query)
    dicts = json.loads(byte_array)

# with open(endpoint + '.csv', 'w') as f:
#     writer = csv.DictWriter(f, dicts[0].keys())
#     writer.writeheader()
#     writer.writerows(dicts)