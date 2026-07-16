"""
Export a clean team metadata table (names, conference/division, colors,
logo URLs) so the Power BI dashboard can display real team names and
brand colors instead of raw abbreviations.
"""
import pandas as pd

teams = pd.read_parquet("../data/teams.parquet")
teams_out = teams[[
    "team_abbr", "team_name", "team_nick", "team_conf", "team_division",
    "team_color", "team_color2", "team_logo_espn",
]].drop_duplicates(subset="team_abbr")
teams_out.to_csv("../exports/teams.csv", index=False)
print(f"teams.csv: {teams_out.shape[0]} rows")
