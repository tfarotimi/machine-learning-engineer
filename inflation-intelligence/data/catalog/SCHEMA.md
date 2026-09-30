# Source catalog schema

`sources.csv` is a UTF-8, comma-delimited catalog with the exact header shown in
the file. Quote fields containing commas, quotes, or line breaks using standard
CSV escaping. One row represents one provider's specific series or document
collection, frequency, and access route. Use separate rows for alternatives.
The catalog distinguishes downloaded records, verified archive routes, and
preserved legacy entries in `notes`. An entry is not a claim that every field
has been verified. Use `unknown` for unresolved properties.

All columns must exist. All cells must be nonempty except unknown historical
dates, which are blank. Use `unknown` for other unverified values; do not infer
availability from a provider's reputation. Dates describe observed coverage,
not publication dates. `historical_end` is the latest verified date, never
`present`.

| Column | Type / convention |
| --- | --- |
| variable | Stable descriptive snake_case series or corpus identifier; record units, transformations, and provider series ID in notes. |
| category | `macroeconomic`, `market`, `commodity`, `inflation_expectations`, `central_bank_text`, `official_statistics_text`, or `external_research_text`. |
| provider | Organization publishing the data. |
| source_url | Absolute HTTPS/HTTP URL for the series, collection, or authoritative documentation; `unknown` if not yet located. |
| frequency | `intraday`, `daily`, `weekly`, `monthly`, `quarterly`, `annual`, `irregular`, or `unknown`. |
| historical_start | Earliest verified reference date, ISO `YYYY-MM-DD`, or blank. |
| historical_end | Latest verified reference date, ISO `YYYY-MM-DD`, or blank; must be on or after historical_start. |
| publication_lag | Documented delay relative to the reference period, including calendar/business days and variability; otherwise `unknown`. Do not use retrieval delay. |
| revisions | `none`, `routine`, `occasional`, or `unknown`; document revision policy and evidence in notes. |
| vintage_data_available | `yes`, `partial`, `no`, or `unknown`; means historical releases as known at past forecast origins, not merely a long time series. |
| machine_access_method | `api`, `csv_download`, `xlsx_download`, `sdmx`, `html`, `pdf`, `manual_only`, or `unknown`; record endpoint, authentication, and restrictions in notes. |
| ongoing_reliability | `high`, `medium`, `low`, or `unknown`; evidence-based assessment, not a guarantee. |
| notes | Free text with evidence URLs, verification date, coverage gaps, units, series IDs, licenses, access limitations, release timestamps/timezone, and vintage retrieval details as applicable; `unknown` if not assessed. |

For monthly/quarterly/annual reference periods, normalize dates to the period's
first day and record that convention in notes. For text, coverage dates refer to
document publication dates. If only meeting/reference dates are verified, leave
the publication coverage columns blank and describe reference coverage in notes.
Archive-listed dates are identified as such; they do not prove the exact original
release timestamp. Supplementary JSON inventories keep meeting dates, reference
periods, publication-date evidence, paths, and SHA-256 hashes separate.
Assess reliability as high only with a documented
release process and verified stable access, medium with material gaps or manual
steps, and low with repeated access failures or discontinued releases. Record
the evidence and audit date in notes; leave unknown until assessed.

The feasibility audit should establish coverage, actual access, release lags,
revision/vintage support, and rights to use each source before modeling. Preserve
publication timestamps and original releases where available. A revised series
without vintages cannot support a fully real-time historical evaluation; document
that limitation explicitly rather than treating revised values as contemporaneous.
