-- Final team-season summary: one row per team per season, combining
-- record, offensive efficiency, and defensive efficiency. This is the
-- modeling table for "what predicts wins."
DROP TABLE IF EXISTS team_season_summary;
CREATE TABLE team_season_summary AS
SELECT
    r.team,
    r.season,
    r.games_played,
    r.wins,
    r.losses,
    r.win_pct,
    r.points_per_game,
    r.points_allowed_per_game,
    ROUND(r.points_per_game - r.points_allowed_per_game, 2)   AS point_differential,
    o.off_epa_per_play,
    o.off_success_rate,
    o.off_third_down_pct,
    o.off_turnovers,
    o.off_penalties,
    d.def_epa_per_play_allowed,
    d.def_success_rate_allowed,
    d.def_third_down_pct_allowed,
    d.def_takeaways,
    (d.def_takeaways - o.off_turnovers)                       AS turnover_margin
FROM team_record_season r
JOIN team_offense_season o ON o.team = r.team AND o.season = r.season
JOIN team_defense_season d ON d.team = r.team AND d.season = r.season
ORDER BY r.season, r.wins DESC;
