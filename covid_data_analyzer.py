"""Validate a historical country snapshot and export five reproducible figures."""

import argparse
import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
COUNTS = ("Confirmed", "Deaths", "Recovered")
REQUIRED = ("Country/Region", *COUNTS, "WHO Region")
NOTE = "Historical snapshot · observation date unverified · raw counts, not population-adjusted"


def load_data(path=ROOT / "COVID_19.csv"):
    """Never silently plot malformed or duplicate country rows."""
    frame = pd.read_csv(path)
    missing = set(REQUIRED) - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    if frame.empty or frame[list(REQUIRED)].isna().any().any():
        raise ValueError("The dataset must contain rows with no missing required values")
    for column in ("Country/Region", "WHO Region"):
        frame[column] = frame[column].astype(str).str.strip()
        if frame[column].eq("").any():
            raise ValueError(f"Blank labels in {column}")
    if frame["Country/Region"].duplicated().any():
        raise ValueError("Country/Region must be unique in a country-level snapshot")
    for column in COUNTS:
        values = pd.to_numeric(frame[column], errors="raise")
        if not np.isfinite(values).all() or (values < 0).any() or (values % 1 != 0).any():
            raise ValueError(f"{column} must contain finite, nonnegative whole counts")
        frame[column] = values.astype("int64")
    if (frame["Deaths"] + frame["Recovered"] > frame["Confirmed"]).any():
        raise ValueError("Deaths plus recoveries cannot exceed confirmed cases")
    return frame


def summarize(frame):
    total = int(frame["Confirmed"].sum())
    regions = frame.groupby("WHO Region")["Confirmed"].sum().sort_values(ascending=False)
    leaders = frame.nlargest(10, "Confirmed")
    return {
        "countries": len(frame),
        "confirmed": total,
        "deaths": int(frame["Deaths"].sum()),
        "recovered": int(frame["Recovered"].sum()),
        "top_ten_confirmed_share_percent": round(100 * int(leaders["Confirmed"].sum()) / total, 2) if total else 0.0,
        "leading_country": str(leaders.iloc[0]["Country/Region"]),
        "confirmed_by_region": {str(region): int(value) for region, value in regions.items()},
        "observation_date": None,
        "interpretation": "Descriptive totals from the included historical snapshot; not current totals or a measure of individual risk.",
    }


def make_figures(frame):
    """Return figures so callers can inspect, save, or display them explicitly."""
    import matplotlib.pyplot as plt
    from matplotlib.ticker import StrMethodFormatter

    figures = {}
    top = frame.nlargest(10, "Confirmed").sort_values("Confirmed")

    def new_figure(title):
        fig, ax = plt.subplots(figsize=(11, 6.5))
        fig.patch.set_facecolor("#faf8f3")
        ax.set_facecolor("#faf8f3")
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_title(title, loc="left", fontsize=15, fontweight="bold", pad=18)
        fig.text(0.02, 0.015, NOTE, fontsize=8, color="#555555")
        return fig, ax

    fig, ax = new_figure("Where were confirmed cases concentrated?")
    ax.barh(top["Country/Region"], top["Confirmed"], color="#24466b")
    ax.set_xlabel("Confirmed cases (count)")
    ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    figures["top_confirmed"] = fig

    fig, ax = new_figure("Deaths and recoveries in the top 10 by confirmed cases")
    positions = np.arange(len(top))
    # Separate positions keep both series visible even when one is much larger.
    ax.barh(positions - 0.2, top["Deaths"], height=0.4, label="Deaths", color="#ab5342")
    ax.barh(positions + 0.2, top["Recovered"], height=0.4, label="Recovered", color="#3a796e")
    ax.set_yticks(positions, top["Country/Region"])
    ax.set_xlabel("Recorded people (count)")
    ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    ax.legend(frameon=False)
    figures["deaths_recovered"] = fig

    fig, ax = new_figure("Recorded confirmed cases by WHO region")
    regions = frame.groupby("WHO Region")["Confirmed"].sum().sort_values()
    ax.barh(regions.index, regions.values, color="#3a796e")
    ax.set_xlabel("Confirmed cases (count)")
    ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    figures["who_regions"] = fig

    fig, ax = new_figure("Confirmed cases and deaths across countries")
    ax.scatter(frame["Confirmed"], frame["Deaths"], color="#ab5342", alpha=0.65, s=30)
    ax.set_xlabel("Confirmed cases (count)")
    ax.set_ylabel("Deaths (count)")
    ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    figures["confirmed_vs_deaths"] = fig

    fig, ax = new_figure("Top 10 countries by recorded deaths")
    deaths = frame.nlargest(10, "Deaths").sort_values("Deaths")
    ax.barh(deaths["Country/Region"], deaths["Deaths"], color="#ab5342")
    ax.set_xlabel("Deaths (count)")
    ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    figures["top_deaths"] = fig

    for figure in figures.values():
        figure.tight_layout(rect=(0, 0.055, 1, 1))
    return figures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "COVID_19.csv")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "charts")
    parser.add_argument("--show", action="store_true", help="Also display interactive chart windows")
    args = parser.parse_args()
    if not args.show:
        matplotlib.use("Agg")
    try:
        frame = load_data(args.data)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    figures = make_figures(frame)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, figure in figures.items():
        figure.savefig(args.output_dir / f"{name}.png", dpi=160, facecolor=figure.get_facecolor())
    summary = summarize(frame)
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Saved {len(figures)} figures to {args.output_dir.resolve()}")
    import matplotlib.pyplot as plt
    if args.show:
        plt.show()
    plt.close("all")


if __name__ == "__main__":
    main()
