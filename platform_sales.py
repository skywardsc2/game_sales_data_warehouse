import csv
import numpy as np

filename_vgsales = "./input_data/vgsales_cut.csv"

# le arquivo contendo a tabela de regioes
regioes = []
with open('./tables_data/regions.csv', 'r') as file_regioes:
  for line in csv.DictReader(file_regioes):
    regioes.append(line)

# le arquivo contendo o dataset de vendas
vgsales = []
with open(filename_vgsales, 'r') as file_vgsales:
  for line in csv.DictReader(file_vgsales):
    vgsales.append(line)

# processa todas as linhas do dataset
t = len(vgsales)

# variaveis para dados sinteticos
piece = 1/4
var = piece/4

for i in range(0, t):
  game = vgsales[i]

  # exclui colunas não utilizadas
  game.pop('Genre', None)
  game.pop('ESRB_Rating', None)
  game.pop('Publisher', None)
  game.pop('Developer', None)
  game.pop('VGChartz_Score', None)
  game.pop('Critic_Score', None)
  game.pop('User_Score', None)
  game.pop('Year', None)
  game.pop('Last_Update', None)
  game.pop('url', None)
  game.pop('status', None)
  game.pop('Vgchartzscore', None)
  game.pop('Global_Sales', None)
  game.pop('img_url', None)

  # transforma colunas vazias em 0
  # e as colunas preenchidas para o numero real (o dataset consta em milhoes de vendas)
  if (game['Total_Shipped'] == ''):
    game['Total_Shipped'] = '0'
  else:
    game['Total_Shipped'] = str(int(float(game['Total_Shipped'])*1000000))

  if (game['NA_Sales'] == ''):
    game['NA_Sales'] = '0'
  else:
    game['NA_Sales'] = str(int(float(game['NA_Sales'])*1000000))

  if (game['PAL_Sales'] == ''):
    game['PAL_Sales'] = '0'
  else:
    game['PAL_Sales'] = str(int(float(game['PAL_Sales'])*1000000))

  if (game['JP_Sales'] == ''):
    game['JP_Sales'] = '0'
  else:
    game['JP_Sales'] = str(int(float(game['JP_Sales'])*1000000))

  if (game['Other_Sales'] == ''):
    game['Other_Sales'] = '0'
  else:
    game['Other_Sales'] = str(int(float(game['Other_Sales'])*1000000))

  # distribui o valor da coluna "total shipped" para as colunas das regioes
  r = piece + (np.random.uniform(-1, 1, 4) * var)
  distr = int(game['Total_Shipped'])

  game['NA_Sales'] = str(int(distr*r[0]) + int(game['NA_Sales']))
  game['JP_Sales'] = str(int(distr*r[1]) + int(game['JP_Sales']))
  game['PAL_Sales'] = str(int(distr*r[2]) + int(game['PAL_Sales']))
  game['Other_Sales'] = str(int(distr*r[3]) + int(game['Other_Sales']))

# cria vetores com paises que receberao valores para cada coluna de regioes do dataset
t = len(regioes)

other_div = []
for i in range(0, t):
  if (
      regioes[i]['region'] != 'Northern America' and
      regioes[i]['country'] != 'Japan' and
      regioes[i]['continent'] != 'Europe'
  ):
    other_div.append(regioes[i]['key'])


pal_div = []
for i in range(0, t):
  if (regioes[i]['continent'] == 'Europe'):
    pal_div.append(regioes[i]['key'])

na_div = []
for i in range(0, t):
  if (regioes[i]['region'] == 'Northern America'):
    na_div.append(regioes[i]['key'])

jp_div = []
for i in range(0, t):
  if (regioes[i]['country'] == 'Japan'):
    jp_div.append(regioes[i]['key'])

# define funcao para sortear paises que receberao valores de vendas
def sorteia_paises(conj, n):
  t = len(conj)
  
  index = np.random.uniform(0, 1, n)

  index = (index*(t-1))

  res = []
  for i in range(0, n):
    res.append(conj[int(index[i])])

  return res

# cria dicionarios para indexação em loop

# dicionario para a coluna do dataset
col = {}
col[0] = 'NA_Sales'
col[1] = 'PAL_Sales'
col[2] = 'JP_Sales'
col[3] = 'Other_Sales'

# dicionario para os vetores de paises que receberao valores
divs = {}
divs[0] = na_div
divs[1] = pal_div
divs[2] = jp_div
divs[3] = other_div

#dicionario para quantidade de paises que receberao valores em cada caso
nc = {}
nc[0] = 1
nc[1] = 3
nc[2] = 1
nc[3] = 5

# leitura do arquivo que contem a tabela de jogos (para pegar as datas de lançamento dos jogos)
games_filename = './tables_data/games.csv'
games = []
with open(games_filename, 'r') as file_games:
  for line in csv.DictReader(file_games):
    games.append(line)

# percorre a tabela de jogos
# cria um dicionario contendo a data de lançamento de cada jogo
datas = {}
t = len(games)

for i in range(0, t):  
  data = {}
  aux = games[i]['release_date'].split('/')
  data['dd'] = aux[0]
  data['mm'] = aux[1]
  data['yyyy'] = aux[2]
  datas[games[i]['basename']] = data

# define funcao para somar meses a uma data
def soma_meses(data, nmeses):
  res = {}
  res['dd'] = data['dd']
  mes = int(data['mm'])
  ano = int(data['yyyy'])

  if (mes < 1):
    mes = 1

  mes += nmeses

  if (mes > 12):
    mes -= 12
    ano+=1

  mes = str(mes)
  ano = str(ano)

  if (len(mes) < 2):
    mes = '0'+mes

  res['mm'] = mes
  res['yyyy'] = ano

  return res

# funcao para retornar a chave de uma data
def chave_data(data):
  res = data['yyyy']+data['mm']
  return res

# percorre o dataset criando as tuplas da tabela de fatos
t = len(vgsales)
tabela_fatos = []
ncol = 4
nmeses = 12

for i in range(0, t):
  line = vgsales[i]

  data_lanc = datas[line['basename']]

  # para cada coluna de regioes de vendas no dataset
  for j in range(0, ncol):
    total = int(line[col[j]])

    # distribui o numero de vendas
    if (total > 0):
      n = nc[j] * nmeses

      piece = 1/n
      var = piece/4

      # define paises sorteados para receber uma parte das vendas
      paises = sorteia_paises(divs[j], nc[j])

      # define proporções para cada pais e para cada mês
      rand = piece + (np.random.uniform(-1, 1, (nc[j], nmeses)) * var)

      # cria as tuplas e insere na tabela de fatos
      for k in range(0, nc[j]):
        for l in range(0, nmeses):
          tupla = {}
          tupla['game'] = line['basename']
          tupla['region'] = paises[k]
          tupla['period'] = chave_data(soma_meses(data_lanc, l))
          tupla['platform'] = line['Platform']
          tupla['sales'] = int(total*rand[k][l])
          tabela_fatos.append(tupla)

# salva a tabela de fatos em um arquivo csv
with open('./tables_data/platform_sales.csv', 'w', newline='') as file:
  w = csv.DictWriter(file, tabela_fatos[0].keys())
  w.writeheader()
  w.writerows(tabela_fatos)