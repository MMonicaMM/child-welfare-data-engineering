-- ============================================================
-- ANALYTICS LAYER
-- ============================================================

CREATE SCHEMA IF NOT EXISTS analytics;


-- ============================================================
-- 1. Children by year and category
-- ============================================================

CREATE OR REPLACE VIEW analytics.v_children_by_year_category AS

SELECT
    y.year,
    c.category_name,
    SUM(f.value) AS total_children

FROM warehouse.fact_social_protection f

JOIN warehouse.dim_year y
    ON f.year_key = y.year_key

JOIN warehouse.dim_category c
    ON f.category_key = c.category_key

GROUP BY
    y.year,
    c.category_name

ORDER BY
    y.year,
    c.category_name;


-- ============================================================
-- 2. Children by municipality and year
-- ============================================================

CREATE OR REPLACE VIEW analytics.v_children_by_municipality_year AS

SELECT
    m.municipality_name,
    y.year,
    SUM(f.value) AS total_children

FROM warehouse.fact_social_protection f

JOIN warehouse.dim_municipality m
    ON f.municipality_key = m.municipality_key

JOIN warehouse.dim_year y
    ON f.year_key = y.year_key

GROUP BY
    m.municipality_name,
    y.year

ORDER BY
    m.municipality_name,
    y.year;


-- ============================================================
-- 3. Children by municipality and category
-- ============================================================

CREATE OR REPLACE VIEW analytics.v_children_by_municipality_category AS

SELECT
    m.municipality_name,
    c.category_name,
    SUM(f.value) AS total_children

FROM warehouse.fact_social_protection f

JOIN warehouse.dim_municipality m
    ON f.municipality_key = m.municipality_key

JOIN warehouse.dim_category c
    ON f.category_key = c.category_key

GROUP BY
    m.municipality_name,
    c.category_name

ORDER BY
    m.municipality_name,
    c.category_name;


-- ============================================================
-- 4. Overall yearly statistics
-- ============================================================

CREATE OR REPLACE VIEW analytics.v_total_children_by_year AS

SELECT
    y.year,
    SUM(f.value) AS total_children

FROM warehouse.fact_social_protection f

JOIN warehouse.dim_year y
    ON f.year_key = y.year_key

GROUP BY
    y.year

ORDER BY
    y.year;

-- ============================================================
-- 5. Total children by category
-- ============================================================

CREATE OR REPLACE VIEW analytics.v_children_by_category AS

SELECT
    c.category_name,
    SUM(f.value) AS total_children

FROM warehouse.fact_social_protection f

JOIN warehouse.dim_category c
    ON f.category_key = c.category_key

GROUP BY
    c.category_name

ORDER BY
    total_children DESC;


-- ============================================================
-- 6. Category change between 2010 and 2019
-- ============================================================

CREATE OR REPLACE VIEW analytics.v_category_change_2010_2019 AS

SELECT
    c.category_name,

    SUM(
        CASE
            WHEN y.year = 2010 THEN f.value
            ELSE 0
        END
    ) AS value_2010,

    SUM(
        CASE
            WHEN y.year = 2019 THEN f.value
            ELSE 0
        END
    ) AS value_2019,

    SUM(
        CASE
            WHEN y.year = 2019 THEN f.value
            ELSE 0
        END
    )
    -
    SUM(
        CASE
            WHEN y.year = 2010 THEN f.value
            ELSE 0
        END
    ) AS absolute_change

FROM warehouse.fact_social_protection f

JOIN warehouse.dim_category c
    ON f.category_key = c.category_key

JOIN warehouse.dim_year y
    ON f.year_key = y.year_key

GROUP BY
    c.category_name

ORDER BY
    absolute_change DESC;