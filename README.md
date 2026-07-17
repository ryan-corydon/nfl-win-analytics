# What Actually Predicts NFL Wins?

An end-to-end data analytics project — SQL, Python, and Power BI — built to answer a real business-style question: **if you were advising an NFL front office on where to invest (coaching, personnel, scheme), which team performance metrics should you prioritize to maximize win probability?**

## Business question

Points and record are the *outcome*. This project looks upstream at the *process* metrics — offensive/defensive efficiency, turnovers, third-down performance — to find which ones actually move the needle on winning, independent of the score itself.

As a case study, the analysis also breaks out the **Chicago Bears** specifically across the sample period.

## Data

Play-by-play and schedule data for the 2019-2023 NFL regular seasons, pulled via [`nfl_data_py`](https://github.com/nflverse/nfl_data_py) (public, from the nflverse project). ~244,000 plays across 159 team-seasons.

## Key finding

**Offensive efficiency (EPA per play) is, by a wide margin, the strongest predictor of winning** — it outranks every other metric across all three methods used (correlation, Random Forest importance, and linear regression), well ahead of defense, turnovers, or third-down conversion rate.

| Metric | Correlation with win % | RF importance |
|---|---|---|
| Offensive EPA/play | 0.74 | 0.43 |
| Defensive takeaways | 0.52 | 0.12 |
| Turnover margin | 0.64 | 0.12 |
| Defensive EPA/play allowed | -0.55 | 0.09 |

**Bears case study**: across all five seasons in the sample (2019-2023), the Bears' offensive EPA/play was *below* league average every single year — directly in line with a losing record in 4 of those 5 seasons. The data points to offensive efficiency as the clearest lever for the franchise to improve win probability.
