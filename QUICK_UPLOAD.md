# Quick Upload Guide - Streamlit App to Snowflake

## ✅ What's Already Deployed

Everything is deployed in Snowflake except the file upload:

- ✅ Database `LITMANEN`
- ✅ Schemas `RAW` and `FEATURES`
- ✅ Table `PLAYER_SEASON_DATA` (58 records)
- ✅ View `LITMANEN_FEATURES`
- ✅ Streamlit app object `LITMANEN_CAREER_ANALYSIS`
- ✅ Stage `STREAMLIT_STAGE`

## 🚀 Upload the File (Choose One Method)

### Method 1: Snowsight Web UI (Easiest - 2 minutes)

1. **Open Snowsight**: https://app.snowflake.com
2. **Navigate to Stage**:
   - Click **Data** in left sidebar
   - Expand **Databases** > **LITMANEN** > **FEATURES**
   - Click on **STREAMLIT_STAGE**
3. **Upload File**:
   - Click **Upload Files** button (top right)
   - Select `/workspace/streamlit/app_snowflake.py` from your computer
   - Click **Upload**
   - Wait for "Upload successful" message
4. **Access App**:
   - Click **Apps** in left sidebar
   - Click **LITMANEN_CAREER_ANALYSIS**
   - App should load! 🎉

### Method 2: SnowSQL (If Installed)

```bash
# Connect to Snowflake
snowsql -a <your_account> -u <your_user>

# Upload the file
PUT file:///workspace/streamlit/app_snowflake.py @LITMANEN.FEATURES.STREAMLIT_STAGE/app_snowflake.py AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

# Verify upload
LIST @LITMANEN.FEATURES.STREAMLIT_STAGE;

# Exit
!exit
```

### Method 3: Snowflake CLI (If Installed)

```bash
snowflake sql -q "PUT file://streamlit/app_snowflake.py @LITMANEN.FEATURES.STREAMLIT_STAGE/app_snowflake.py AUTO_COMPRESS=FALSE OVERWRITE=TRUE;"
```

## 📍 File Location

The file to upload is located at:
```
/workspace/streamlit/app_snowflake.py
```

Or relative to project root:
```
streamlit/app_snowflake.py
```

## ✅ Verify Upload

After uploading, verify with:

```sql
LIST @LITMANEN.FEATURES.STREAMLIT_STAGE;
```

You should see `app_snowflake.py` in the results.

## 🎯 Access Your App

Once uploaded:

1. Open **Snowsight**
2. Click **Apps** in left sidebar
3. Click **LITMANEN_CAREER_ANALYSIS**
4. The app will load automatically!

## 🆘 Troubleshooting

### File Not Uploading
- Check file path is correct
- Verify you have WRITE permissions on the stage
- Try uploading via Snowsight Web UI (most reliable)

### App Not Appearing
- Verify file was uploaded: `LIST @LITMANEN.FEATURES.STREAMLIT_STAGE;`
- Check app exists: `SHOW STREAMLITS IN SCHEMA LITMANEN.FEATURES;`
- Refresh Snowsight Apps page

### App Not Loading
- Check warehouse is running: `ALTER WAREHOUSE COMPUTE_WH RESUME;`
- Verify data exists: `SELECT COUNT(*) FROM LITMANEN.FEATURES.LITMANEN_FEATURES;`
- Check app logs in Snowsight (click on app, then "Logs" tab)

## 📊 Current Deployment Status

| Component | Status |
|-----------|--------|
| Database | ✅ Deployed |
| Schemas | ✅ Deployed |
| Data | ✅ Deployed (58 records) |
| Feature View | ✅ Deployed |
| Streamlit App Object | ✅ Deployed |
| Stage | ✅ Deployed |
| **File Upload** | ⏳ **Pending** |

**Next Step**: Upload `app_snowflake.py` using one of the methods above!
