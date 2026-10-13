# COVID-19 Data Visualization

Five static charts that explore the country-level COVID-19 snapshot included in `COVID_19.csv`. This is an exploratory analysis of a historical file, not a live dashboard or a source for current case totals.

## Run

Python 3.11 or newer:

```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python covid_data_analyzer.py
```

The script reads the CSV beside itself, validates the required columns and numeric values, and writes charts to `charts/`. Add `--show` to open the figures interactively. It also saves `charts/summary.json` with the row count, aggregate totals, and top-country summary. Values are reproduced from this file and should not be interpreted as current statistics.

## Charts

The output includes top countries by confirmed cases, deaths and recoveries for the leading countries, confirmed cases by WHO region, confirmed cases versus deaths, and top countries by deaths. The comparisons use labeled axes and separate series so magnitudes can be read without relying on color alone.

## Data and caveats

The repository's CSV is the sole input. Its observation date and original source are not documented in the repository, so this project does not assign it a date or claim to verify its provenance. The file is a static snapshot; definitions, missingness, and reporting practices may differ by location. There is no time-series analysis or live data fetching.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests cover schema and value validation, summary calculations, chart generation, and output-directory handling. GitHub Actions runs the suite on Python 3.11 and 3.12.
