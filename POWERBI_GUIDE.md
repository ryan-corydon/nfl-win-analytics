# Power BI Dashboard Build Guide

Once Power BI Desktop is installed, follow these steps to build the dashboard from the exported data.

## 1. Import the data

Home → Get Data → Text/CSV, and import each of these from the `exports/` folder:

- `team_season_summary.csv` — the main fact table (159 rows: one per team per season, with record + efficiency metrics)
- `teams.csv` — team names, conference/division, colors, logos
- `feature_importance.csv` — the "what predicts wins" ranking
- `correlation_with_wins.csv` — correlation of each stat with win_pct
- `bears_vs_league.csv` — Bears season-by-season vs league average

## 2. Set up the relationship

In Model view, drag a relationship from `team_season_summary[team]` to `teams[team_abbr]`. This lets you pull in full team names, colors, and logos anywhere you use the abbreviation.

## 3. Add these DAX measures

Right-click `team_season_summary` in the Fields pane → New Measure, and add each of these:

```dax
Avg Win Pct = AVERAGE(team_season_summary[win_pct])

Avg Off EPA per Play = AVERAGE(team_season_summary[off_epa_per_play])

Avg Def EPA Allowed = AVERAGE(team_season_summary[def_epa_per_play_allowed])

Total Wins = SUM(team_season_summary[wins])

Bears Win Pct =
CALCULATE(
    [Avg Win Pct],
    team_season_summary[team] = "CHI"
)

League Avg Off EPA =
CALCULATE(
    [Avg Off EPA per Play],
    ALL(team_season_summary[team])
)
```

## 4. Build these pages/visuals

**Page 1 — League Overview**
- Scatter chart: X = `off_epa_per_play`, Y = `win_pct`, size = `wins`, legend = `team` (color by team using `teams[team_color]` if you set up conditional formatting). This is the single chart that visually proves the finding — teams cluster along a clear upward trend.
- Bar chart: `feature_importance.csv` values, sorted descending — the "what matters" chart.
- Table: top 10 teams by `win_pct` with `off_epa_per_play`, `def_epa_per_play_allowed`, `turnover_margin`.
- Slicer: `season`

**Page 2 — Bears Deep Dive**
- Line chart from `bears_vs_league.csv`: Bears `off_epa_per_play` vs `off_epa_per_play_league_avg` across seasons (recreates the Python chart, but interactive).
- KPI cards: Bears' `wins`, `win_pct`, `off_epa_per_play` rank among all 32 teams for the selected season.
- Table: Bears' season-by-season record.

**Page 3 — Team Explorer**
- Slicer: `team` (use `teams[team_logo_espn]` if you want logos via an image URL column — set the column's "Data category" to "Image URL" in Power Query first)
- All the efficiency metrics for the selected team/season, styled as KPI cards.

## 5. Style

- Use a dark or light theme consistent with what you'd want on your portfolio site — a clean, executive-report look matches the "presented insights directly to the CEO/CFO" framing from your resume.
- Title the report something like **"What Actually Predicts NFL Wins?"**

## 6. Publish / export for the portfolio

- File → Export → Export to PDF, or take clean screenshots of each page, to embed on the portfolio Projects page.
- If you have a Power BI Pro/free account, you can also Publish to Power BI Service and use "Publish to web" for a live embeddable version — same approach as your Tableau Public projects.
