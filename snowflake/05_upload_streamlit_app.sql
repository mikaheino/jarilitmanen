-- Instructions for uploading Streamlit app to Snowflake
-- Run these commands using SnowSQL or Snowflake CLI

-- Step 1: Upload the Streamlit app file to the stage
-- PUT file:///workspace/streamlit/app_snowflake.py @LITMANEN.FEATURES.STREAMLIT_STAGE/app_snowflake.py;

-- Step 2: Verify the file was uploaded
-- LIST @LITMANEN.FEATURES.STREAMLIT_STAGE;

-- Step 3: The Streamlit app should now be accessible in Snowsight
-- Navigate to: Apps > LITMANEN_CAREER_ANALYSIS

-- Note: If you need to update the app, upload the new version and refresh the app in Snowsight
