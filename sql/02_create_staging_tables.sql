CREATE TABLE IF NOT EXISTS staging.rzs_social_protection (
    municipality VARCHAR(100) NOT NULL,
    municipality_code INTEGER NOT NULL,
    year INTEGER NOT NULL,
    category TEXT NOT NULL,
    value INTEGER NOT NULL,

    source_id VARCHAR(50) NOT NULL,
    loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_year
        CHECK (year >= 1900 AND year <= 2100),

    CONSTRAINT chk_value
        CHECK (value >= 0)
);