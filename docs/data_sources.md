# Data Sources

This document contains the registry of public data sources used
for the Child Welfare Data Engineering project.

The project focuses on publicly available data related to:

- children without parental care
- foster care
- residential care
- social protection
- child welfare institutions
- regional and local social services

Only publicly available data will be collected.

No personally identifiable information about individual children
will be collected or processed.

---

## Source Registry

| ID | Source | Organization | Data Type | Format | Extraction Method | Frequency | Status |
|----|--------|--------------|-----------|--------|-------------------|-----------|--------|
| SRC001 | TBD | TBD | TBD | HTML | BeautifulSoup | TBD | Planned |
| SRC002 | TBD | TBD | TBD | HTML Table | Pandas / BeautifulSoup | TBD | Planned |
| SRC003 | TBD | TBD | TBD | PDF | PDF extraction | TBD | Planned |
| SRC004 | TBD | TBD | TBD | API | REST API | TBD | Planned |
| SRC005 | TBD | TBD | TBD | Open Data | CSV / API | TBD | Planned |

---

# Source Details

## SRC001

**Source:** Deca i omladina korisnici socijalne zaštite

**Organization:** Republički zavod za statistiku (RZS)

**URL:** https://data.gov.rs/sr/datasets/statistichki-godishnjak-2019-sotsijalna-zashtita/

**Data type:** Social protection statistics

**Format:** XLSX

**Extraction method:** Python / HTTP download / Pandas

**Relevant attributes:**

- Grad/Opština
- Matični broj opštine
- Godina
- Kategorija
- Broj

**Geographical level:**

City / Municipality

**Time period:**

Available years in the source

**Update frequency:**

Depends on RZS publication

**Purpose in project:**

Used as a structured public data source for children
and youth receiving social protection services.

**Status:**

Selected

## SRC002

**Source:** TBD

**Organization:** TBD

**URL:** TBD

**Data type:** TBD

**Format:** TBD

**Extraction method:** TBD

**Relevant indicators:**

- TBD

**Geographical level:**

- TBD

**Time period:**

- TBD

**Update frequency:**

- TBD

**Notes:**

TBD

# Source Assessment

| ID | Publicly Accessible | Structured Data | Historical Data | Geographic Detail | Scraping Complexity | Data Quality |
|----|---------------------|------------------|------------------|-------------------|---------------------|--------------|
| SRC001 | TBD | TBD | TBD | TBD | TBD | TBD |
| SRC002 | TBD | TBD | TBD | TBD | TBD | TBD |
| SRC003 | TBD | TBD | TBD | TBD | TBD | TBD |
| SRC004 | TBD | TBD | TBD | TBD | TBD | TBD |
| SRC005 | TBD | TBD | TBD | TBD | TBD | TBD |