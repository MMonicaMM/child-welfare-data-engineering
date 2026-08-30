-- ============================================================
-- DATA WAREHOUSE
-- ============================================================

CREATE SCHEMA IF NOT EXISTS warehouse;


-- ============================================================
-- DIMENSION: MUNICIPALITY
-- ============================================================

CREATE TABLE IF NOT EXISTS warehouse.dim_municipality (
    municipality_key SERIAL PRIMARY KEY,
    municipality_code INTEGER NOT NULL,
    municipality_name VARCHAR(255) NOT NULL,

    CONSTRAINT uq_dim_municipality_code
        UNIQUE (municipality_code)
);


-- ============================================================
-- DIMENSION: CATEGORY
-- ============================================================

CREATE TABLE IF NOT EXISTS warehouse.dim_category (
    category_key SERIAL PRIMARY KEY,
    category_name VARCHAR(500) NOT NULL,

    CONSTRAINT uq_dim_category_name
        UNIQUE (category_name)
);


-- ============================================================
-- DIMENSION: YEAR
-- ============================================================

CREATE TABLE IF NOT EXISTS warehouse.dim_year (
    year_key INTEGER PRIMARY KEY,
    year INTEGER NOT NULL,

    CONSTRAINT uq_dim_year_year
        UNIQUE (year)
);


-- ============================================================
-- FACT: SOCIAL PROTECTION
-- ============================================================

CREATE TABLE IF NOT EXISTS warehouse.fact_social_protection (
    municipality_key INTEGER NOT NULL,
    category_key INTEGER NOT NULL,
    year_key INTEGER NOT NULL,

    value INTEGER NOT NULL,

    source_id VARCHAR(50) NOT NULL,
    loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_fact_municipality
        FOREIGN KEY (municipality_key)
        REFERENCES warehouse.dim_municipality(municipality_key),

    CONSTRAINT fk_fact_category
        FOREIGN KEY (category_key)
        REFERENCES warehouse.dim_category(category_key),

    CONSTRAINT fk_fact_year
        FOREIGN KEY (year_key)
        REFERENCES warehouse.dim_year(year_key),

    CONSTRAINT chk_fact_value
        CHECK (value >= 0),

    CONSTRAINT uq_fact_social_protection
        UNIQUE (
            municipality_key,
            category_key,
            year_key,
            source_id
        )
);