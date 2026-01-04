-- Step 23: Load CSV to table
-- Note: This assumes the CSV file has been uploaded to the stage
-- Upload command: PUT file:///workspace/data/litmanen_career_dataset_full.csv @LITMANEN.RAW.STAGE_CSV;

COPY INTO LITMANEN.RAW.PLAYER_SEASON_DATA
FROM @LITMANEN.RAW.STAGE_CSV/litmanen_career_dataset_full.csv
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1);

