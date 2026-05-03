# 📊 COVID-19 Data Visualization Project

## 📌 Overview

This project analyzes and visualizes global COVID-19 data using Python. It focuses on extracting meaningful insights through different types of visualizations such as bar charts, pie charts, scatter plots, and horizontal bar charts.

The dataset used contains country-wise COVID-19 statistics including confirmed cases, deaths, recoveries, and WHO region classification.

---

## 🛠️ Technologies Used

* Python
* Pandas (Data Manipulation)
* NumPy (Numerical Operations)
* Matplotlib (Data Visualization)

---

## 📂 Dataset

* File Name: `COVID_19.csv`
* Expected Columns:

  * `Country/Region`
  * `Confirmed`
  * `Deaths`
  * `Recovered`
  * `WHO Region`

---

## 📈 Visualizations Included

### 1. Top 10 Countries by Confirmed Cases

* A vertical bar chart displaying the countries with the highest confirmed COVID-19 cases.
* Helps identify the most affected regions globally.

### 2. Deaths vs Recoveries Comparison

* A grouped bar chart comparing deaths and recoveries among the top 10 countries.
* Useful for understanding recovery efficiency vs fatality.

### 3. Region-wise Distribution (Pie Chart)

* A pie chart showing the proportion of confirmed cases across WHO regions.
* Provides a macro-level regional analysis.

### 4. Scatter Plot (Deaths vs Confirmed Cases)

* Displays the relationship between confirmed cases and deaths.
* Helps identify trends and correlations.

### 5. Top 10 Countries by Deaths (Horizontal Bar Chart)

* Highlights countries with the highest death counts.
* Easier comparison using horizontal layout.

---

## ▶️ How to Run the Project

1. Install required libraries:

```bash
pip install pandas matplotlib numpy
```

2. Place the dataset file `COVID_19.csv` in the project directory.

3. Run the Python script:

```bash
python your_script_name.py
```

---

## 📊 Key Features

* Data cleaning and aggregation using Pandas
* Multiple visualization techniques
* Formatted large numbers for readability
* Clear labeling and layout adjustments

---

## ⚠️ Limitations

* Static dataset (no real-time updates)
* No interactive dashboards
* Dependent on dataset accuracy

---

## 🚀 Future Improvements

* Add interactive dashboards using Plotly or Streamlit
* Include time-series analysis
* Automate data updates using APIs

---

## 📎 Author

Mohit Mahato



Feel free to fork this repository and improve the project. Suggestions and contributions are welcome!
