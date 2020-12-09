# Game Sales Data Warehouse

## Sobre

Segundo trabalho da disciplina de Processamento Analítico de Dados do ICMC-USP

## Autores

- Rodrigo Mendes Andrade (nusp: 10262721)
- Marcelo Kiochi Hatanaka (nusp: 10295645)


---


## Arquivos

- [input_data](./input_data/) - contém datasets utilizados
  - [vgsales.csv](./input_data/vgsales.csv) - dataset original ([link](https://www.kaggle.com/ashaheedq/video-games-sales-2019))
- [query_data](./query_data/) - contém arquivos e gráficos com resultados das consultas efetuadas
- [tables_data](./tables_data) - arquivos .csv para povoamento das tabelas
- [sql](./sql) - arquivos com scripts de criação das tabelas e consultas realizadas
- [utility](./utility/) - módulos utilitários para requisições ao igdb, transformação dos dados, etc.
- [games.py](games.py), [platforms.py](platforms.py), ... - scripts de geração dos arquivos .csv para povoamento das tabelas
- [requirements.txt](requirements.txt) - módulos python necessários para executar os scripts (instalar com ```pip install requirements.txt```)
  - Módulos:
    - igdb-api-v4
    - requests
    - dotenv
    - numpy

## Observações

É necessário uma conta [Twitch](https://www.twitch.tv) e as variáveis de ambiente TWITCH_ID e TWITCH_SECRET com os valores apropriados para a execução das requisições ao [IGDB](https://api-docs.igdb.com/#about) feitas nos scripts de geração dos dados para povoamento das tabelas.