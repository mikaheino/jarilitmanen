# Deploying Streamlit App to Snowflake

This guide explains how to deploy the Streamlit application to run natively inside Snowflake.

## Prerequisites

- Snowflake account with Streamlit support
- SnowSQL or Snowflake CLI installed
- Appropriate permissions (CREATE STREAMLIT, CREATE STAGE)

## Step 1: Create Stage and Streamlit App

Execute the SQL script to create the necessary objects:

```bash
# Using Snowflake CLI
snowflake-sql < snowflake/04_create_streamlit_app.sql

# Or copy/paste into Snowsight SQL worksheet
```

This will:
- Create a stage for storing the Streamlit app files
- Create the Streamlit app object
- Grant necessary permissions

## Step 2: Upload App File

Upload the Streamlit app file to the stage:

### Using SnowSQL:

```bash
snowsql -a <account> -u <user> -d LITMANEN -s FEATURES

PUT file:///workspace/streamlit/app_snowflake.py @LITMANEN.FEATURES.STREAMLIT_STAGE/app_snowflake.py;
```

### Using Snowflake CLI:

```bash
snowflake sql -q "PUT file://streamlit/app_snowflake.py @LITMANEN.FEATURES.STREAMLIT_STAGE/app_snowflake.py"
```

### Using Snowsight:

1. Navigate to **Data** > **Databases** > **LITMANEN** > **FEATURES** > **STREAMLIT_STAGE**
2. Click **Upload Files**
3. Select `app_snowflake.py`
4. Upload

## Step 3: Verify Upload

Check that the file was uploaded:

```sql
LIST @LITMANEN.FEATURES.STREAMLIT_STAGE;
```

## Step 4: Access the App

1. Open **Snowsight**
2. Navigate to **Apps** in the left sidebar
3. Click on **LITMANEN_CAREER_ANALYSIS**
4. The app should load automatically

## Step 5: Update App (if needed)

If you make changes to the app:

1. Upload the updated file:
   ```bash
   PUT file:///workspace/streamlit/app_snowflake.py @LITMANEN.FEATURES.STREAMLIT_STAGE/app_snowflake.py OVERWRITE;
   ```

2. Refresh the app in Snowsight (click the refresh button)

## Differences from Local Streamlit

### Connection Handling

Snowflake native Streamlit apps automatically have access to a Snowflake session. The app uses:

```python
@st.cache_resource
def init_session():
    try:
        conn = st.connection("snowflake")
        return conn.session()
    except:
        # Fallback to manual connection
        ...
```

### Column Names

Snowflake returns column names in UPPERCASE by default. The app handles this by using uppercase column names (`CLUB`, `COMPETITION`, etc.).

### Performance

- Uses Snowpark DataFrames for better performance
- Leverages Snowflake's compute for filtering and aggregation
- Caching with `@st.cache_data` and `@st.cache_resource`

## Troubleshooting

### App Not Appearing

- Check that the Streamlit app was created successfully
- Verify permissions: `SHOW GRANTS ON STREAMLIT LITMANEN.FEATURES.LITMANEN_CAREER_ANALYSIS;`
- Ensure the file was uploaded to the stage

### Connection Errors

- Verify the app has access to the LITMANEN database
- Check that the warehouse is running
- Ensure the session has proper role permissions

### Import Errors

- Snowflake native Streamlit includes common packages (pandas, plotly, etc.)
- If you need additional packages, you may need to create a Python environment or use Snowpark Python UDFs

### Data Not Loading

- Verify the LITMANEN.FEATURES.LITMANEN_FEATURES view exists
- Check that the session has SELECT permissions
- Test the query manually: `SELECT * FROM LITMANEN.FEATURES.LITMANEN_FEATURES LIMIT 5;`

## Benefits of Snowflake Native Streamlit

1. **No Local Setup**: Runs entirely in Snowflake
2. **Automatic Scaling**: Uses Snowflake's compute resources
3. **Integrated Security**: Uses Snowflake's security model
4. **Easy Sharing**: Share with other Snowflake users via permissions
5. **No Infrastructure**: No need to manage servers or deployments

## Alternative: Hybrid Approach

You can also keep the local Streamlit app (`app.py`) for development and use the Snowflake version (`app_snowflake.py`) for production deployment.
