# Jari Litmanen Career Data Analysis

ML project analyzing Jari Litmanen's football career data using Snowflake, Python, and Streamlit.

## Project Structure

```
.
├── data/                          # Raw data files
│   └── litmanen_career_dataset_full.csv
├── snowflake/                     # Snowflake SQL scripts
│   ├── 01_create_database_schema.sql
│   ├── 02_load_data.sql
│   ├── 02_load_data_direct.sql
│   └── 03_create_features.sql
├── ml/                            # Machine learning scripts
│   └── load_data.py
├── streamlit/                     # Streamlit application
└── .devcontainer/                 # Dev container configuration
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Snowflake connection:**
   - Copy `.env.example` to `.env` (if available)
   - Fill in your Snowflake credentials

3. **Create Snowflake objects:**
   ```bash
   # Run SQL scripts in order:
   # 1. Create database and schema
   snowflake-sql < snowflake/01_create_database_schema.sql
   
   # 2. Load data
   snowflake-sql < snowflake/02_load_data_direct.sql
   
   # 3. Create features view
   snowflake-sql < snowflake/03_create_features.sql
   ```

## Snowflake Database Structure

- **Database:** `LITMANEN`
- **Schemas:**
  - `RAW` - Raw data tables
  - `FEATURES` - Feature views

### Tables & Views

- `LITMANEN.RAW.PLAYER_SEASON_DATA` - Raw career statistics
- `LITMANEN.FEATURES.LITMANEN_FEATURES` - Feature engineering view with calculated ratios

## Data

The dataset contains Jari Litmanen's career statistics from 1990-2011, including:
- Season information
- Competition type
- Club
- Appearances, starts, minutes played
- Points per game (ppg)

## Features

The feature view calculates:
- `appearance_ratio` - Ratio of appearances vs max in competition/season
- `minutes_ratio` - Ratio of minutes vs max in competition/season
- `season_start_year` - Derived year for sorting (handles formats like '11/12', '2001')

## Next Steps

- [ ] Train ML model (Step 40-43)
- [ ] Build Streamlit app (Step 50-52)
- [ ] Create presentation materials (Step 60-61)

## References

Based on project instructions from `jari_litmanen_ml_project_instructions.csv`
