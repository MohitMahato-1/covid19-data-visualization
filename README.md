# COVID-19 Data Visualization

A small Python project that reads the included country-level COVID-19 CSV and displays five static Matplotlib charts. It is a data-visualization exercise using a historical snapshot, not a live dashboard or a source for current case totals.

## Visualizations

The script generates:

1. Top 10 countries by confirmed cases.
2. Deaths and recoveries for those countries.
3. Confirmed cases grouped by WHO region.
4. Confirmed cases versus deaths.
5. Top 10 countries by deaths.

## Dataset

The repository includes `COVID_19.csv`. The script uses these columns:

- `Country/Region`
- `Confirmed`
- `Deaths`
- `Recovered`
- `WHO Region`

The data is static. The charts reflect the values in this file and do not update automatically.

## Requirements

- Python 3
- pandas
- NumPy
- Matplotlib

## Run

From the repository root:

```bash
python -m pip install pandas numpy matplotlib
python covid_data_analyzer.py
```

The script reads `COVID_19.csv` from the current working directory and opens each chart with Matplotlib.

## Files

```text
.
├── COVID_19.csv
├── covid_data_analyzer.py
└── README.md
```

## Limitations

- The dataset is a fixed historical snapshot, not real-time data.
- Charts are static; there is no interactive dashboard or time-series analysis.
- Results depend on the accuracy and definitions used in the supplied dataset.
