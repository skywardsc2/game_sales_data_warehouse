import csv

def getUniquesFromCSV(filename, column_name):
  list_of_rows = []
  with open(filename, 'r') as csv_file:
    for line in csv.DictReader(csv_file):
      list_of_rows.append(line)

  list_of_rows_unique = []
  hash_map = {}

  t = len(list_of_rows)
  j=0
  for i in range(0, t):
    row = list_of_rows[i].copy()
    if ((row['basename'] in hash_map) == False):
      hash_map[row['basename']] = j
      list_of_rows_unique.append(row)
      j += 1
  
  return list_of_rows_unique

size = 10000
rows = []
with open('../input_data/vgsales.csv', 'r') as f:
  for line in csv.DictReader(f):
    rows.append(line)


rows = rows[:size]

with open('../input_data/vgsales_cut.csv', 'w', newline='') as f:
  writer = csv.DictWriter(f, rows[0].keys())
  writer.writeheader()
  writer.writerows(rows)

rows_unique = []
hash_map = {}
t = len(rows)
j = 0
for i in range(0, t):
  row = rows[i].copy()
  if ((row['basename'] in hash_map) == False):
    hash_map[row['basename']] = j
    rows_unique.append(row)
    j += 1

game_data_rows = []
with open('../tables_data/games.csv', 'r') as f:
  for line in csv.DictReader(f):
    game_data_rows.append(line)

basename_set = set(g['basename'] for g in rows_unique)
game_data_cut = [g for g in game_data_rows if g['Basename'] in basename_set]

with open('../tables_data/games_cut.csv', 'w', newline='') as f:
  writer = csv.DictWriter(f, game_data_cut[0].keys())
  writer.writeheader()
  writer.writerows(game_data_cut)