-- Step 50-52: Create Snowflake Native Streamlit App
-- This creates a Streamlit app that runs directly inside Snowflake

-- Create Streamlit app object
CREATE OR REPLACE STREAMLIT LITMANEN.FEATURES.LITMANEN_CAREER_ANALYSIS
  ROOT_LOCATION = '@LITMANEN.FEATURES.STREAMLIT_STAGE'
  MAIN_FILE = 'app_snowflake.py'
  QUERY_WAREHOUSE = 'COMPUTE_WH';  -- Replace with your warehouse name

-- Note: After creating the app, you need to:
-- 1. Upload the app_snowflake.py file to the stage
-- 2. Grant permissions to users who should access it
-- 3. Access via Snowsight: Apps > LITMANEN_CAREER_ANALYSIS

-- Create stage for Streamlit app files
CREATE OR REPLACE STAGE LITMANEN.FEATURES.STREAMLIT_STAGE;

-- Grant usage on app
GRANT USAGE ON STREAMLIT LITMANEN.FEATURES.LITMANEN_CAREER_ANALYSIS TO ROLE PUBLIC;

-- Grant usage on stage
GRANT USAGE ON STAGE LITMANEN.FEATURES.STREAMLIT_STAGE TO ROLE PUBLIC;
