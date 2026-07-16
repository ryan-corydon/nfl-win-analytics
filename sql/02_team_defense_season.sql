-- Team defensive efficiency (what the defense allowed), per team per regular season.
DROP TABLE IF EXISTS team_defense_season;
CREATE TABLE team_defense_season AS
SELECT
    defteam                                                  AS team,
    season,
    COUNT(*)                                                 AS def_plays,
    ROUND(AVG(epa), 4)                                       AS def_epa_per_play_allowed,
    ROUND(AVG(success), 4)                                   AS def_success_rate_allowed,
    ROUND(
        1.0 * SUM(third_down_converted)
        / NULLIF(SUM(third_down_converted) + SUM(third_down_failed), 0), 4
    )                                                        AS def_third_down_pct_allowed,
    SUM(interception) + SUM(fumble_lost)                     AS def_takeaways
FROM raw_pbp
WHERE season_type = 'REG'
  AND play_type IN ('pass', 'run')
  AND defteam IS NOT NULL
GROUP BY defteam, season;
