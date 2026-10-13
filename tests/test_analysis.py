"""Regression checks for misleading charts, invalid data, and launch portability."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import covid_data_analyzer as analysis


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.frame = analysis.load_data()

    def tearDown(self):
        plt.close("all")

    def assert_invalid(self, frame, message):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.csv"
            frame.to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, message):
                analysis.load_data(path)

    def test_schema_and_duplicate_validation(self):
        self.assert_invalid(self.frame.drop(columns="Deaths"), "Missing required")
        self.assert_invalid(pd.concat([self.frame, self.frame.iloc[:1]]), "must be unique")

    def test_negative_missing_and_impossible_counts_rejected(self):
        for value in (-1, float("inf"), 0.5):
            frame = self.frame.copy()
            frame["Deaths"] = frame["Deaths"].astype(float)
            frame.loc[0, "Deaths"] = value
            self.assert_invalid(frame, "finite, nonnegative whole")
        frame = self.frame.copy()
        frame.loc[0, "Deaths"] = frame.loc[0, "Confirmed"] + 1
        self.assert_invalid(frame, "cannot exceed")
        frame.loc[0, "Country/Region"] = None
        self.assert_invalid(frame, "missing required")

    def test_scatter_axes_match_the_actual_data(self):
        ax = analysis.make_figures(self.frame)["confirmed_vs_deaths"].axes[0]
        points = ax.collections[0].get_offsets()
        self.assertEqual(ax.get_xlabel(), "Confirmed cases (count)")
        self.assertEqual(ax.get_ylabel(), "Deaths (count)")
        self.assertEqual(list(points[:, 0]), list(self.frame["Confirmed"]))
        self.assertEqual(list(points[:, 1]), list(self.frame["Deaths"]))

    def test_comparison_bars_do_not_obscure_each_other(self):
        ax = analysis.make_figures(self.frame)["deaths_recovered"].axes[0]
        self.assertEqual([text.get_text() for text in ax.get_legend().get_texts()], ["Deaths", "Recovered"])
        for death, recovery in zip(*ax.containers):
            self.assertLessEqual(death.get_y() + death.get_height(), recovery.get_y() + 1e-10)

    def test_historical_totals_regression(self):
        result = analysis.summarize(self.frame)
        self.assertEqual(result["countries"], 187)
        self.assertEqual(result["confirmed"], 16480485)
        self.assertEqual(sum(result["confirmed_by_region"].values()), result["confirmed"])
        self.assertIsNone(result["observation_date"])

    def test_command_runs_from_an_unrelated_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run(
                [sys.executable, str(analysis.ROOT / "covid_data_analyzer.py"), "--output-dir", folder],
                cwd=folder, capture_output=True, text=True, timeout=90,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(list(Path(folder).glob("*.png"))), 5)
            self.assertTrue((Path(folder) / "summary.json").is_file())


if __name__ == "__main__":
    unittest.main()
