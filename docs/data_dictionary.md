# Data Dictionary

## SRC001 — RZS Children and Youth Receiving Social Protection

### Raw Dataset

| Column | Original Name | Data Type | Description |
|---|---|---|---|
| municipality | Град/Општина | string | Name of municipality/city |
| municipality_code | Матични број општине | integer | Official municipality identification code |
| year | Година | integer | Reference year |
| category | Категорије | string | Social protection category |
| value | Број | integer | Number of children/youth |

### Dataset Characteristics

- Geographic coverage: Niš
- Time period: 2010–2019
- Number of rows: 60
- Number of categories: 6
- Missing values: None
- Duplicate rows: None

### Grain

One record represents:

Municipality × Year × Social Protection Category

### Important Limitation

This dataset represents data for Niš and should not be interpreted
as national-level data for Serbia.

The dataset contains children and youth receiving social protection
services/categories and does not by itself represent all children
without parental care.