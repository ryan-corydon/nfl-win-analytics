"""
Pull raw NFL data (play-by-play + schedules) for the seasons under study
and cache to local parquet files so downstream steps don't re-hit the source.
"""
import nfl_data_py as nfl

YEARS = list(range(2019, 2024))  # 2019-2023 seasons

print(f"Pulling play-by-play for {YEARS}...")
pbp = nfl.import_pbp_data(YEARS, downcast=True, cache=False)
pbp.to_parquet("../data/pbp.parquet")
print(f"pbp shape: {pbp.shape}")

print("Pulling schedules...")
schedules = nfl.import_schedules(YEARS)
schedules.to_parquet("../data/schedules.parquet")
print(f"schedules shape: {schedules.shape}")

print("Pulling team descriptions...")
teams = nfl.import_team_desc()
teams.to_parquet("../data/teams.parquet")
print(f"teams shape: {teams.shape}")

print("Done.")
