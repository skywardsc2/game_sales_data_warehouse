import csv

filename = "./utility/regioes.csv"
filename_out = "./tables_data/regions.csv"

# le arquivo csv cque contem os continentes, regioes e paises
file = open(filename, 'r')
regioes = []
for line in csv.DictReader(file):
  regioes.append(line)

file.close()

# cria a chave para cada instancia
for dic in regioes:
  dic['key'] = (dic['continent']+dic['region']+dic['country']).replace(' ', '')

# salva em arquivo csv
with open(filename_out, 'w', newline='') as file:
  w = csv.DictWriter(file, regioes[0].keys())
  w.writeheader()
  w.writerows(regioes)