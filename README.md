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
│   ├── train_model.py
│   └── README.md
├── streamlit/                     # Streamlit application
│   ├── app.py
│   └── README.md
├── presentation/                  # Presentation materials
│   ├── PRESENTATION.md
│   └── DEMO_SCRIPT.md
└── .devcontainer/                 # Dev container configuration
```

## Quick Start

### Prerequisites
- Snowflake account with database creation privileges
- Python 3.11+ installed
- Git installed

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mikaheino/jarilitmanen.git
   cd jarilitmanen
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Snowflake connection:**
   - **Option A:** Using Snowflake MCP Server (if configured in Cursor)
   - **Option B:** Create `.env` file with your Snowflake credentials:
     ```
     SNOWFLAKE_ACCOUNT=your_account
     SNOWFLAKE_USER=your_user
     SNOWFLAKE_PASSWORD=your_password
     SNOWFLAKE_WAREHOUSE=your_warehouse
     SNOWFLAKE_DATABASE=LITMANEN
     SNOWFLAKE_SCHEMA=RAW
     SNOWFLAKE_ROLE=ACCOUNTADMIN
     ```

4. **Create Snowflake objects:**
   
   **Using Snowflake CLI:**
   ```bash
   # 1. Create database and schema
   snowflake-sql < snowflake/01_create_database_schema.sql
   
   # 2. Load data
   snowflake-sql < snowflake/02_load_data_direct.sql
   
   # 3. Create features view
   snowflake-sql < snowflake/03_create_features.sql
   ```
   
   **Using Snowflake Web UI (Snowsight):**
   - Open Snowsight SQL worksheet
   - Copy and paste each SQL script content
   - Execute in order: 01 → 02 → 03

5. **Verify setup:**
   ```sql
   SELECT COUNT(*) FROM LITMANEN.RAW.PLAYER_SEASON_DATA;
   -- Expected: 58 records
   
   SELECT * FROM LITMANEN.FEATURES.LITMANEN_FEATURES LIMIT 5;
   -- Should show data with calculated features
   ```

## Testing

For detailed step-by-step testing instructions, see **[TESTING.md](TESTING.md)**.

### Quick Test

```sql
-- Verify data loaded
SELECT COUNT(*) as total_records FROM LITMANEN.RAW.PLAYER_SEASON_DATA;

-- Test feature view
SELECT 
  season,
  club,
  competition,
  appearance_ratio,
  minutes_ratio,
  season_start_year
FROM LITMANEN.FEATURES.LITMANEN_FEATURES
ORDER BY season_start_year DESC
LIMIT 10;
```

## Running the ML Model

```bash
# Train the model
python ml/train_model.py
```

This will:
- Pull features from Snowflake
- Define target variable (low availability)
- Train Random Forest and Logistic Regression models
- Save the best model and feature importance

See [ml/README.md](ml/README.md) for details.

## Running the Streamlit App

```bash
# Launch the dashboard
streamlit run streamlit/app.py
```

This will:
- Connect to Snowflake
- Load career data
- Display interactive charts and filters
- Show anomaly detection section

See [streamlit/README.md](streamlit/README.md) for details.

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

- [x] Train ML model (Step 40-43) ✅
- [x] Build Streamlit app (Step 50-52) ✅
- [x] Create presentation materials (Step 60-61) ✅

## Documentation

- **[TESTING.md](TESTING.md)** - Comprehensive testing guide with step-by-step instructions
- **[plan_and_progress.md](plan_and_progress.md)** - Project progress tracking
- **[ml/README.md](ml/README.md)** - ML model training guide
- **[streamlit/README.md](streamlit/README.md)** - Streamlit app guide
- **[presentation/PRESENTATION.md](presentation/PRESENTATION.md)** - Presentation slides and guide
- **[presentation/DEMO_SCRIPT.md](presentation/DEMO_SCRIPT.md)** - Live demo script

## References

Based on project instructions from `jari_litmanen_ml_project_instructions.csv`
