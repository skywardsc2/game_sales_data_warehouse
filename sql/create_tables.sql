CREATE TABLE periods
(
    "month" smallint NOT NULL,
    "month_name" character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "year" smallint NOT NULL,
    "bimester" smallint NOT NULL,
    "trimester" smallint NOT NULL,
    "semester" smallint NOT NULL,
    "key" integer NOT NULL,
    CONSTRAINT periods_pk PRIMARY KEY ("key")
);

CREATE TABLE games
(
    "name" character varying(300) COLLATE pg_catalog."default" NOT NULL,
    "basename" character varying(300) COLLATE pg_catalog."default" NOT NULL,
    "release_date" character varying(20) COLLATE pg_catalog."default",
    "age_rating" character varying(20) COLLATE pg_catalog."default",
    "single_player" boolean,
    "multi_player" boolean,
    "franchise" character varying(300) COLLATE pg_catalog."default",
    CONSTRAINT games_pk PRIMARY KEY ("basename")
);

CREATE TABLE platforms
(
    "name" character varying(50) COLLATE pg_catalog."default" NOT NULL,
    "abbreviation" character varying(5) COLLATE pg_catalog."default" NOT NULL,
    "first_release_date" date,
    "generation" smallint,
    "family" character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT platforms_pk PRIMARY KEY ("abbreviation")
);

CREATE TABLE regions
(
    "continent" character varying(30) COLLATE pg_catalog."default" NOT NULL,
    "region" character varying(30) COLLATE pg_catalog."default" NOT NULL,
    "country" character varying(30) COLLATE pg_catalog."default" NOT NULL,
    "key" character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT regions_pk PRIMARY KEY ("key")
);

CREATE TABLE platform_sales
(
    "game" character varying(300) NOT NULL,
    "region" character varying(100) NOT NULL,
    "period" integer NOT NULL,
    "platform" character varying(50) NOT NULL,
    "sales" bigint NOT NULL,
    CONSTRAINT "game_fk" FOREIGN KEY ("game")
        REFERENCES games ("basename") MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT "period_fk" FOREIGN KEY ("period")
        REFERENCES periods ("key") MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT "platform_fk" FOREIGN KEY ("platform")
        REFERENCES platforms ("abbreviation") MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT "region_fk" FOREIGN KEY ("region")
        REFERENCES regions ("key") MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);