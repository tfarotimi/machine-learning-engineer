# Inflation Intelligence

**Research question:** Do AI-extracted signals from central-bank text improve
inflation forecasts for Chile beyond macroeconomic, market/commodity, and
inflation-expectation data?

The immediate milestone is a **data-feasibility audit for Chile**: verify access,
coverage, publication lags, revisions, and historical vintages before choosing
models. No ingestion pipelines, forecasting models, or agents are implemented.

## Planned architecture

```text
data/catalog/           Source inventory and schema
notebooks/             01_data_feasibility.ipynb: audit starting point
src/
  ingestion/           Future source retrieval and release metadata
  text/                Future central-bank document processing and signal extraction
  features/            Future time-aligned numeric and textual predictors
  forecasting/         Future baselines and augmented forecasts
  evaluation/          Future rolling-origin comparisons and text ablations
  agents/              Reserved for future workflow orchestration
  inflation_intelligence/  Shared configuration and logging
tests/                 Standard-library unit tests
```

Planned flow: source releases → ingestion/text processing → features → forecasts
→ evaluation. Later comparisons should use identical forecast origins and data
available at each origin, accounting for publication lags and revisions. Agent
design, model choices, and forecast targets/horizons remain open until the audit.

## Setup

Use **Python 3.12** (also specified in `.python-version` and `pyproject.toml`).
From this directory on Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[notebooks]"
.\.venv\Scripts\python -m unittest discover -s tests -v
.\.venv\Scripts\python -m jupyterlab notebooks/01_data_feasibility.ipynb
```

Use `pip install -e .` if notebook tooling is unnecessary. Runtime utilities use
only the standard library; setuptools builds the distribution. Domain directories
are empty Python packages, not placeholder implementations. No nested Git
repository is needed within the parent project.

## Configuration and audit

`.env.example` documents environment variables; set them in the shell or your
execution environment. Files named `.env` are not automatically loaded. Call
`load_settings()` from `inflation_intelligence.config` and, at an entry point,
`configure_logging(settings.log_level)` from `inflation_intelligence.logging`.
Logging preserves existing host handlers. Relative data paths resolve against
the current working directory; configuration creates no directories or files.

Start with [the catalog schema](data/catalog/SCHEMA.md) and populate
`data/catalog/sources.csv` only with evidence-backed records. The notebook reads
the catalog without downloading data. Record unresolved access/vintage questions
explicitly. Downloaded data and credentials are ignored by Git; catalog metadata
and notebooks are tracked. Clear notebook outputs before committing sensitive or
large results.

The September 2026 acquisition audit is documented in
[the feasibility report](data/catalog/AUDIT.md). It includes 93 BCCh numeric
series, the 2016-onward IPoM/minutes/CPI/wage document archives, survey workbooks,
and the existing RPM press releases. Source-level uncertainties remain explicit:
downloaded history is not automatically a real-time vintage dataset.

The catalog keeps its original 13-column schema. Companion JSON inventories
record file hashes, observed coverage, document dates, and workbook sheets;
the notebook reads these local artifacts without network requests. Raw files
remain under `data/raw/feasibility_2026-09-10/`; this acquisition started on
September 10 and continued on September 14, as recorded per file in the manifest.
