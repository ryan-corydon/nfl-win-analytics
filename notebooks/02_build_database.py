"""
Load the raw parquet files into a SQLite database so the aggregation
logic can live in real SQL rather than pandas.
"""
import sqlite3
import pandas as pd

DB_PATH = "../data/nfl.db"

pbp = pd.read_parquet("../data/pbp.parquet")
schedules = pd.read_parquet("../data/schedules.parquet")
teams = pd.read_parquet("../data/teams.parquet")

# Keep pbp to a manageable, relevant column set — the full 397-column
# table has a lot of player-id/tracking noise we don't need for team
# season aggregation.
pbp_cols = [
    "season", "season_type", "week", "posteam", "defteam", "play_type",
    "down", "yards_gained", "epa", "success",
    "third_down_converted", "third_down_failed",
    "fourth_down_converted", "fourth_down_failed",
    "interception", "fumble_lost", "penalty", "penalty_team",
    "touchdown", "yardline_100", "field_goal_result",
]
pbp_slim = pbp[[c for c in pbp_cols if c in pbp.columns]].copy()

con = sqlite3.connect(DB_PATH)
pbp_slim.to_sql("raw_pbp", con, if_exists="replace", index=False)
schedules.to_sql("schedules", con, if_exists="replace", index=False)
teams.to_sql("teams", con, if_exists="replace", index=False)

con.execute("CREATE INDEX IF NOT EXISTS idx_pbp_posteam ON raw_pbp(posteam, season)")
con.execute("CREATE INDEX IF NOT EXISTS idx_pbp_defteam ON raw_pbp(defteam, season)")
con.commit()

print("Tables loaded:")
for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print(" -", row[0])
print(f"raw_pbp rows: {len(pbp_slim)}")
con.close()
