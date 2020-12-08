-- Consultar a quantidade de vendas de jogos para PlayStation 3, por ano, entre os anos de 2010 e 2019.

-- Interessante caso a empresa tenha um bom palpite quanto a viabilidade da produção de jogos para uma plataforma especifica 
-- (no caso, o PlayStation 3) e deseje confirmar sua hipótese

SELECT
	platforms.name AS platform, 
	periods.year, 
	sum(platform_sales.sales) AS sales
    FROM 
    	platforms, periods, platform_sales
    WHERE 
    	platform_sales.platform = platforms.abbreviation 
    	AND platform_sales.period = periods.key
    	AND platforms.name = 'PlayStation 3'
    	AND periods.year BETWEEN 2010 AND 2019
    GROUP BY 
    	periods.year, platforms.name;


-- Quais as 5 plataformas com maior quantidade de vendas nos ultimos 5 anos em cada continente do mundo

-- Interessante para descobrir o tamanho do mercado consumidor de cada plataforma em diferentes regioes do mundo,
-- além de quais plataformas possuem maior popularidade no geral

SELECT 
	r.continent AS continent,
	r.platform AS platform,
	r.sales AS sales
	FROM
		(SELECT
			x.continent AS continent,
			x.platform AS platform,
			x.sales AS sales,
			ROW_NUMBER() OVER (PARTITION BY x.continent ORDER BY x.sales DESC) AS num
			FROM
				(SELECT
					regions.continent AS continent,
     				platforms.name AS platform,
     				sum(platform_sales.sales) AS sales
					FROM
						platform_sales,
						regions,
						platforms,
						periods
					WHERE
						platform_sales.region = regions.key 
						AND platform_sales.platform = platforms.abbreviation
						AND platform_sales.period = periods.key
						AND periods.year > EXTRACT( year FROM CURRENT_DATE )::int - 5
					GROUP BY
						platforms.name, regions.continent
				) x
		) r
	WHERE
		r.num <= 5;
		

-- Quantidade de vendas de jogos para cada plataforma, por classificação etária, para as plataformas mais populares lançadas nos ultimos 10 anos

-- Interessante para analisar a interferência da classificação etária nas vendas de jogos para as plataformas atuais de maior sucesso. Isso pode
-- influenciar no tipo de conteudo que a empresa irá apresentar em seu proximo jogo

SELECT 
    platforms.name as platform,
    games.age_rating,
    sum(platform_sales.sales) AS sales
    FROM
        games, platforms, platform_sales
    WHERE
        platform_sales.game = games.basename
        AND platform_sales.platform = platforms.abbreviation
        AND games.age_rating IS NOT NULL
        AND platforms.name IN (
                SELECT platforms.name
                    FROM
                        platform_sales, platforms
                    WHERE
                        platform_sales.platform = platforms.abbreviation
                        AND EXTRACT( year FROM platforms.first_release_date )::int > EXTRACT( year FROM CURRENT_DATE )::int - 10
                    GROUP BY
                        platforms.name
                    ORDER BY
                        sum(platform_sales.sales) DESC
                    LIMIT 10
            )
    GROUP BY
        games.age_rating, platforms.name
    ORDER BY
        platforms.name, sales DESC;



		
