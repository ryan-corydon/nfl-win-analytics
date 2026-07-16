"""
Run the SQL aggregation pipeline (sql/01 -> 04) against the SQLite
database and export the final team-season summary table to CSV.
"""
import sqlite3
from pathlib import Path

DB_PATH = "../data/nfl.db"
SQL_DIR = Path("../sql")

con = sqlite3.connect(DB_PATH)

for sql_file in sorted(SQL_DIR.glob("*.sql")):
    print(f"Running {sql_file.name}...")
    script = sql_file.read_text()
    con.executescript(script)
    con.commit()

df = con.execute("SELECT * FROM team_season_summary").fetchall()
cols = [d[0] for d in con.execute("SELECT * FROM team_season_summary LIMIT 1").description]

import pandas as pd
summary = pd.DataFrame(df, columns=cols)
summary.to_csv("../exports/team_season_summary.csv", index=False)

print(f"\nteam_season_summary: {summary.shape[0]} rows, {summary.shape[1]} cols")
print(summary.head(10).to_string())

con.close()
