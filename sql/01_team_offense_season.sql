-- Team offensive efficiency, per team per regular season.
DROP TABLE IF EXISTS team_offense_season;
CREATE TABLE team_offense_season AS
SELECT
    posteam                                                  AS team,
    season,
    COUNT(*)                                                 AS off_plays,
    ROUND(AVG(epa), 4)                                       AS off_epa_per_play,
    ROUND(AVG(success), 4)                                   AS off_success_rate,
    ROUND(
        1.0 * SUM(third_down_converted)
        / NULLIF(SUM(third_down_converted) + SUM(third_down_failed), 0), 4
    )                                                        AS off_third_down_pct,
    SUM(interception) + SUM(fumble_lost)                     AS off_turnovers,
    ROUND(1.0 * SUM(penalty), 0)                             AS off_penalties
FROM raw_pbp
WHERE season_type = 'REG'
  AND play_type IN ('pass', 'run')
  AND posteam IS NOT NULL
GROUP BY posteam, season;
