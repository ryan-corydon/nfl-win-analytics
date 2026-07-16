# What Actually Predicts NFL Wins?

An end-to-end data analytics project — SQL, Python, and Power BI — built to answer a real business-style question: **if you were advising an NFL front office on where to invest (coaching, personnel, scheme), which team performance metrics should you prioritize to maximize win probability?**

## Business question

Points and record are the *outcome*. This project looks upstream at the *process* metrics — offensive/defensive efficiency, turnovers, third-down performance — to find which ones actually move the needle on winning, independent of the score itself.

As a case study, the analysis also breaks out the **Chicago Bears** specifically across the sample period.

## Data

Play-by-play and schedule data for the 2019-2023 NFL regular seasons, pulled via [`nfl_data_py`](https://github.com/nflverse/nfl_data_py) (public, from the nflverse project). ~244,000 plays across 159 team-seasons.

## Pipeline

1. **Python** (`notebooks/01_pull_data.py`) — pulls raw play-by-play, schedules, and team metadata.
2. **SQL** (`sql/*.sql`, run via `notebooks/02_build_database.py` and `03_run_sql_aggregation.py`) — loads raw data into SQLite and aggregates it into team-season offensive efficiency, defensive efficiency, and win/loss records, joined into one modeling table.
3. **Python / data science** (`notebooks/04_analysis.py`) — correlation analysis, a Random Forest regression (held-out R² = 0.78), and standardized linear regression coefficients to rank which metrics predict `win_pct`, plus a Bears-vs-league-average breakdown.
4. **Power BI** (`POWERBI_GUIDE.md`) — interactive dashboard built from the exported tables.

## Key finding

**Offensive efficiency (EPA per play) is, by a wide margin, the strongest predictor of winning** — it outranks every other metric across all three methods used (correlation, Random Forest importance, and linear regression), well ahead of defense, turnovers, or third-down conversion rate.

| Metric | Correlation with win % | RF importance |
|---|---|---|
| Offensive EPA/play | 0.74 | 0.43 |
| Defensive takeaways | 0.52 | 0.12 |
| Turnover margin | 0.64 | 0.12 |
| Defensive EPA/play allowed | -0.55 | 0.09 |

**Bears case study**: across all five seasons in the sample (2019-2023), the Bears' offensive EPA/play was *below* league average every single year — directly in line with a losing record in 4 of those 5 seasons. The data points to offensive efficiency as the clearest lever for the franchise to improve win probability.

See `exports/feature_importance.png` and `exports/bears_vs_league.png` for the supporting charts.

## Repo structure

```
data/          raw pulled data (parquet, gitignored) + SQLite database
sql/           the actual SQL aggregation logic
notebooks/     pipeline scripts, run in order (01 -> 05)
exports/       final CSVs/charts, ready for Power BI import
POWERBI_GUIDE.md   step-by-step dashboard build instructions
```

## Reproducing this

```
python -m venv venv
venv\Scripts\pip install nfl_data_py pandas scikit-learn matplotlib seaborn pyarrow
cd notebooks
python 01_pull_data.py
python 02_build_database.py
python 03_run_sql_aggregation.py
python 04_analysis.py
python 05_export_for_powerbi.py
```

Then follow `POWERBI_GUIDE.md` to build the dashboard.

## Tools

SQL (SQLite) · Python (pandas, scikit-learn, matplotlib) · Power BI
