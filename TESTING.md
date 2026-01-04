# Testing Guide - Jari Litmanen ML Project

This guide provides step-by-step instructions to test the Snowflake solution.

## Prerequisites

1. **Snowflake Account** with access to create databases
2. **Snowflake MCP Server** configured (or direct Snowflake access)
3. **Python 3.11+** installed
4. **Git** installed

## Step 1: Clone the Repository

```bash
git clone https://github.com/mikaheino/jarilitmanen.git
cd jarilitmanen
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Configure Snowflake Connection

### Option A: Using Snowflake MCP Server (Recommended)

If you're using Cursor with Snowflake MCP server configured, you can skip this step. The MCP server handles authentication automatically.

### Option B: Using Python Scripts

Create a `.env` file in the project root:

```bash
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=LITMANEN
SNOWFLAKE_SCHEMA=RAW
SNOWFLAKE_ROLE=ACCOUNTADMIN
```

## Step 4: Create Snowflake Database and Schema

### Using SQL Scripts (Recommended)

Execute the SQL scripts in order:

```bash
# Option 1: Using Snowflake CLI (if installed)
snowflake-sql < snowflake/01_create_database_schema.sql

# Option 2: Using Snowflake Web UI (Snowsight)
# Copy and paste the contents of snowflake/01_create_database_schema.sql
# into Snowsight SQL worksheet and execute
```

**Expected Result:**
- Database `LITMANEN` created
- Schema `RAW` created
- Schema `FEATURES` created
- Stage `STAGE_CSV` created
- Table `PLAYER_SEASON_DATA` created

### Verification Query

```sql
SHOW DATABASES LIKE 'LITMANEN';
SHOW SCHEMAS IN DATABASE LITMANEN;
SHOW TABLES IN SCHEMA LITMANEN.RAW;
```

## Step 5: Load Data into Snowflake

### Option A: Using Direct SQL Insert (Recommended for Testing)

```bash
# Using Snowflake CLI
snowflake-sql < snowflake/02_load_data_direct.sql

# Or copy/paste into Snowsight
```

**Expected Result:** 58 rows inserted

### Option B: Using Python Script

```bash
python ml/load_data.py
```

**Expected Result:** "Successfully loaded data from ..."

### Option C: Using Stage (Advanced)

1. Upload CSV to Snowflake stage:
   ```sql
   PUT file:///path/to/data/litmanen_career_dataset_full.csv @LITMANEN.RAW.STAGE_CSV;
   ```

2. Load from stage:
   ```bash
   snowflake-sql < snowflake/02_load_data.sql
   ```

### Verification Query

```sql
SELECT COUNT(*) as total_records FROM LITMANEN.RAW.PLAYER_SEASON_DATA;
-- Expected: 58

SELECT * FROM LITMANEN.RAW.PLAYER_SEASON_DATA 
ORDER BY season DESC 
LIMIT 5;
-- Should show recent seasons (2011, 2010, etc.)
```

## Step 6: Create Feature View

```bash
# Using Snowflake CLI
snowflake-sql < snowflake/03_create_features.sql

# Or copy/paste into Snowsight
```

**Expected Result:** View `LITMANEN_FEATURES` created

### Verification Query

```sql
SELECT COUNT(*) as total_records FROM LITMANEN.FEATURES.LITMANEN_FEATURES;
-- Expected: 58 (or 57 if one record has NULL minutes)

SELECT 
  season,
  club,
  competition,
  appearances,
  minutes,
  appearance_ratio,
  minutes_ratio,
  season_start_year
FROM LITMANEN.FEATURES.LITMANEN_FEATURES
ORDER BY season_start_year DESC
LIMIT 10;
-- Should show data with calculated ratios and proper year sorting
```

## Step 7: Test Feature Calculations

### Test 1: Verify Season Start Year Calculation

```sql
SELECT 
  season,
  season_start_year,
  CASE 
    WHEN season LIKE '%/%' THEN 
      CASE 
        WHEN CAST(SUBSTRING(season, 1, 2) AS INT) < 50 THEN CAST(SUBSTRING(season, 1, 2) AS INT) + 2000
        ELSE CAST(SUBSTRING(season, 1, 2) AS INT) + 1900
      END
    ELSE CAST(season AS INT)
  END AS expected_year
FROM LITMANEN.FEATURES.LITMANEN_FEATURES
WHERE season_start_year != expected_year;
-- Expected: 0 rows (all years should match)
```

### Test 2: Verify Ratio Calculations

```sql
-- Check that ratios are between 0 and 1
SELECT 
  season,
  competition,
  appearance_ratio,
  minutes_ratio
FROM LITMANEN.FEATURES.LITMANEN_FEATURES
WHERE appearance_ratio > 1 OR minutes_ratio > 1 
   OR appearance_ratio < 0 OR minutes_ratio < 0;
-- Expected: 0 rows (all ratios should be between 0 and 1)
```

### Test 3: Verify Data Completeness

```sql
-- Check for NULL values in key fields
SELECT 
  COUNT(*) as total_records,
  COUNT(season) as seasons_with_data,
  COUNT(club) as clubs_with_data,
  COUNT(minutes) as minutes_with_data,
  COUNT(appearance_ratio) as ratios_calculated
FROM LITMANEN.FEATURES.LITMANEN_FEATURES;
-- Expected: All counts should be 58 (or 57 if one record excluded)
```

## Step 8: Test Data Analysis Queries

### Query 1: Career Summary by Club

```sql
SELECT 
  club,
  COUNT(*) as seasons_played,
  SUM(appearances) as total_appearances,
  SUM(minutes) as total_minutes,
  AVG(ppg) as avg_points_per_game
FROM LITMANEN.FEATURES.LITMANEN_FEATURES
GROUP BY club
ORDER BY total_minutes DESC;
-- Should show clubs like Ajax, Liverpool, Barcelona, etc.
```

### Query 2: Performance by Competition

```sql
SELECT 
  competition,
  COUNT(*) as seasons,
  AVG(minutes_ratio) as avg_minutes_ratio,
  AVG(ppg) as avg_points_per_game
FROM LITMANEN.FEATURES.LITMANEN_FEATURES
GROUP BY competition
ORDER BY avg_minutes_ratio DESC;
-- Should show different competitions with their statistics
```

### Query 3: Career Timeline

```sql
SELECT 
  season_start_year,
  club,
  competition,
  appearances,
  minutes,
  ppg
FROM LITMANEN.FEATURES.LITMANEN_FEATURES
ORDER BY season_start_year ASC;
-- Should show career progression from 1990 to 2011
```

## Step 9: Test Edge Cases

### Test 1: NULL Handling

```sql
-- Verify that NULL minutes are excluded from features view
SELECT COUNT(*) 
FROM LITMANEN.RAW.PLAYER_SEASON_DATA 
WHERE minutes IS NULL;
-- Check if any NULL minutes exist

SELECT COUNT(*) 
FROM LITMANEN.FEATURES.LITMANEN_FEATURES 
WHERE minutes IS NULL;
-- Expected: 0 (NULL minutes should be filtered out)
```

### Test 2: Division by Zero Protection

```sql
-- Verify that NULLIF prevents division by zero
SELECT 
  season,
  competition,
  appearance_ratio,
  minutes_ratio
FROM LITMANEN.FEATURES.LITMANEN_FEATURES
WHERE appearance_ratio IS NULL OR minutes_ratio IS NULL;
-- Should only return rows where max appearances/minutes were 0 for that competition/season
```

## Step 10: Performance Testing

### Test Query Performance

```sql
-- Test view performance
EXPLAIN SELECT * FROM LITMANEN.FEATURES.LITMANEN_FEATURES 
WHERE season_start_year >= 2000;

-- Test aggregation performance
EXPLAIN SELECT club, AVG(minutes_ratio) 
FROM LITMANEN.FEATURES.LITMANEN_FEATURES 
GROUP BY club;
```

## Troubleshooting

### Issue: Database/Schema Already Exists

**Solution:** The scripts use `IF NOT EXISTS`, so they're safe to run multiple times. If you need to recreate:

```sql
DROP SCHEMA IF EXISTS LITMANEN.FEATURES CASCADE;
DROP SCHEMA IF EXISTS LITMANEN.RAW CASCADE;
DROP DATABASE IF EXISTS LITMANEN CASCADE;
```

Then re-run the setup scripts.

### Issue: Data Not Loading

**Check:**
1. Verify CSV file exists: `ls -la data/litmanen_career_dataset_full.csv`
2. Check CSV format matches table schema
3. Verify Snowflake connection credentials
4. Check warehouse is running: `ALTER WAREHOUSE <warehouse> RESUME;`

### Issue: Feature View Returns No Rows

**Check:**
1. Verify data exists in raw table: `SELECT COUNT(*) FROM LITMANEN.RAW.PLAYER_SEASON_DATA;`
2. Check if all minutes are NULL: `SELECT COUNT(*) FROM LITMANEN.RAW.PLAYER_SEASON_DATA WHERE minutes IS NULL;`
3. Verify view was created: `SHOW VIEWS IN SCHEMA LITMANEN.FEATURES;`

### Issue: Ratios Are NULL

**Check:**
1. Verify window function is working: Check if MAX() returns values
2. Check for competition/season combinations with only one record
3. Verify NULLIF is working correctly

## Success Criteria

✅ All tests pass:
- [ ] Database and schemas created successfully
- [ ] 58 records loaded into raw table
- [ ] Feature view created and returns data
- [ ] Season start year calculated correctly
- [ ] Ratios calculated correctly (between 0 and 1)
- [ ] No NULL values in key fields (except where expected)
- [ ] Analysis queries return expected results

## Next Steps

After successful testing:
1. Proceed with ML model training (Step 40-43 from project instructions)
2. Build Streamlit application (Step 50-52)
3. Create presentation materials (Step 60-61)

## Additional Resources

- [Snowflake Documentation](https://docs.snowflake.com/)
- [Project README](README.md)
- [Project Instructions](jari_litmanen_ml_project_instructions.csv)
