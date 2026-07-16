-- Team win/loss record per regular season, unioning home and away games
-- into one team-per-row perspective.
DROP TABLE IF EXISTS team_record_season;
CREATE TABLE team_record_season AS
WITH games AS (
    SELECT season, home_team AS team, home_score AS points_for, away_score AS points_against
    FROM schedules
    WHERE game_type = 'REG' AND home_score IS NOT NULL
    UNION ALL
    SELECT season, away_team AS team, away_score AS points_for, home_score AS points_against
    FROM schedules
    WHERE game_type = 'REG' AND away_score IS NOT NULL
)
SELECT
    team,
    season,
    COUNT(*)                                                          AS games_played,
    SUM(CASE WHEN points_for > points_against THEN 1 ELSE 0 END)      AS wins,
    SUM(CASE WHEN points_for < points_against THEN 1 ELSE 0 END)      AS losses,
    SUM(CASE WHEN points_for = points_against THEN 1 ELSE 0 END)      AS ties,
    ROUND(1.0 * SUM(CASE WHEN points_for > points_against THEN 1 ELSE 0 END) / COUNT(*), 4)
                                                                       AS win_pct,
    ROUND(1.0 * SUM(points_for) / COUNT(*), 2)                        AS points_per_game,
    ROUND(1.0 * SUM(points_against) / COUNT(*), 2)                    AS points_allowed_per_game
FROM games
GROUP BY team, season;
