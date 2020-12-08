import csv
import math

vgsales_filename = './input_data/vgsales.csv'

# le arquivo do dataset de vendas de jogos
games = []
with open(vgsales_filename, 'r') as vgsales_file:
  for line in csv.DictReader(vgsales_file):
    games.append(line)

# percorre as linhas para encontrar o menor ano de lançamento
menor_ano = 2020
t = len(games)
for i in range(0, t):
  if (games[i]['Year'] != ''):
    ano = int(float(games[i]['Year']))
    if (ano < menor_ano):
      menor_ano = ano

# cria dicionario para o nome dos meses
mesEscrito = {}
mesEscrito[1] = 'January'
mesEscrito[2] = 'February'
mesEscrito[3] = 'March'
mesEscrito[4] = 'April'
mesEscrito[5] = 'May'
mesEscrito[6] = 'June'
mesEscrito[7] = 'July'
mesEscrito[8] = 'August'
mesEscrito[9] = 'September'
mesEscrito[10] = 'October'
mesEscrito[11] = 'November'
mesEscrito[12] = 'December'

# cria tabela de periodos com todas as combinações possiveis
# desde o menor ano encontrado ate 2021
tabela_periodo = []
for i in range(menor_ano, 2022):
  for j in range(1, 13):
    tupla = {}

    tupla['month'] = str(j)
    tupla['month_name'] = mesEscrito[j]
    tupla['year'] = str(i)
    tupla['bimester'] = str(math.ceil(j/2))
    tupla['trimester'] = str(math.ceil(j/3))
    tupla['semester'] = str(math.ceil(j/6))

    ano = str(i)
    mes = str(j)
    if (len(mes) < 2):
      mes = '0'+mes

    tupla['key'] = ano+mes
    tabela_periodo.append(tupla)

# salva tabela em arquivo csv
with open('./tables_data/periods.csv', 'w', newline='') as file:
  w = csv.DictWriter(file, tabela_periodo[0].keys())
  w.writeheader()
  w.writerows(tabela_periodo)