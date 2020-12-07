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
  - [vgsales_unified.csv](input_data/vgsales_unified.csv) - dataset com agrupamento por jogo
- [tables_data](./tables_data) - arquivos .csv para povoamento das tabelas
- [games.py](games.py), [platforms.py](platforms.py) - scripts de geração dos arquivos em "tables_data"
- [requirements.txt](requirements.txt) - módulos python necessários para executar os scripts (instalar com ```pip install requirements.txt```)

## Observações

É necessário uma conta [Twitch](https://www.twitch.tv) e as variáveis de ambiente TWITCH_ID e TWITCH_SECRET com os valores apropriados para a execução das requisições ao [IGDB](https://api-docs.igdb.com/#about)

