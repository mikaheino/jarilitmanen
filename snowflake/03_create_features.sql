-- Step 30: Create feature view
CREATE OR REPLACE VIEW LITMANEN.FEATURES.LITMANEN_FEATURES AS
SELECT
  season,
  competition,
  club,
  appearances,
  starts,
  ppg,
  minutes,
  -- Calculate workload ratios
  appearances * 1.0 / NULLIF(MAX(appearances) OVER (PARTITION BY competition, season), 0) AS appearance_ratio,
  minutes * 1.0 / NULLIF(MAX(minutes) OVER (PARTITION BY competition, season), 0) AS minutes_ratio,
  -- Derive season start year for sorting (handles formats like '11/12', '2001', '99/00')
  CASE 
    WHEN season LIKE '%/%' THEN 
      CASE 
        WHEN CAST(SUBSTRING(season, 1, 2) AS INT) < 50 THEN CAST(SUBSTRING(season, 1, 2) AS INT) + 2000
        ELSE CAST(SUBSTRING(season, 1, 2) AS INT) + 1900
      END
    ELSE CAST(season AS INT)
  END AS season_start_year
FROM LITMANEN.RAW.PLAYER_SEASON_DATA
WHERE minutes IS NOT NULL;

