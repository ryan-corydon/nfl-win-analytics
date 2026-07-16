"""
What actually predicts wins? Correlation + feature importance analysis
on team-season efficiency metrics, plus a Chicago Bears-specific cut.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

df = pd.read_csv("../exports/team_season_summary.csv")

# Process-level features only — deliberately excluding points_per_game,
# points_allowed_per_game, and point_differential, since those are
# essentially restatements of the outcome (wins), not underlying causes.
FEATURES = [
    "off_epa_per_play", "off_success_rate", "off_third_down_pct",
    "off_turnovers", "off_penalties",
    "def_epa_per_play_allowed", "def_success_rate_allowed",
    "def_third_down_pct_allowed", "def_takeaways", "turnover_margin",
]
TARGET = "win_pct"

data = df.dropna(subset=FEATURES + [TARGET])
X = data[FEATURES]
y = data[TARGET]

# --- Correlation ---
corr = X.assign(**{TARGET: y}).corr()[TARGET].drop(TARGET).sort_values(key=abs, ascending=False)
print("=== Correlation with win_pct ===")
print(corr.to_string())
corr.rename("correlation_with_win_pct").to_csv("../exports/correlation_with_wins.csv")

# --- Random Forest feature importance ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf = RandomForestRegressor(n_estimators=400, random_state=42, max_depth=5)
rf.fit(X_train, y_train)
r2 = r2_score(y_test, rf.predict(X_test))
print(f"\n=== Random Forest ===\nHeld-out R^2: {r2:.3f}")

importance = pd.Series(rf.feature_importances_, index=FEATURES).sort_values(ascending=False)
print(importance.to_string())
importance.rename("importance").to_csv("../exports/feature_importance.csv")

# --- Standardized linear regression for interpretable direction/magnitude ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
lin = LinearRegression().fit(X_scaled, y)
coef = pd.Series(lin.coef_, index=FEATURES).sort_values(key=abs, ascending=False)
print("\n=== Standardized linear coefficients (direction + magnitude) ===")
print(coef.to_string())
coef.rename("standardized_coefficient").to_csv("../exports/linear_coefficients.csv")

# --- Feature importance chart ---
fig, ax = plt.subplots(figsize=(8, 5))
importance.sort_values().plot(kind="barh", ax=ax, color="#4f46e5")
ax.set_title("What Predicts NFL Wins? (Random Forest Feature Importance)")
ax.set_xlabel("Importance")
plt.tight_layout()
plt.savefig("../exports/feature_importance.png", dpi=150)
plt.close()

# --- Bears-specific cut ---
bears = df[df["team"] == "CHI"].sort_values("season")
league_avg = df.groupby("season")[FEATURES + ["win_pct"]].mean().add_suffix("_league_avg")
bears_vs_league = bears.set_index("season").join(league_avg)
bears_vs_league.to_csv("../exports/bears_vs_league.csv")

print("\n=== Bears seasons in sample ===")
print(bears[["season", "wins", "losses", "win_pct", "off_epa_per_play", "def_epa_per_play_allowed"]].to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(bears["season"], bears["off_epa_per_play"], marker="o", label="Bears offensive EPA/play", color="#f97316")
ax.plot(league_avg.index, league_avg["off_epa_per_play_league_avg"], marker="o", label="League average", color="#94a3b8", linestyle="--")
ax.set_title("Bears Offensive Efficiency vs League Average")
ax.set_xlabel("Season")
ax.set_ylabel("EPA per play")
ax.legend()
plt.tight_layout()
plt.savefig("../exports/bears_vs_league.png", dpi=150)
plt.close()

print("\nDone. Exports written to ../exports/")
