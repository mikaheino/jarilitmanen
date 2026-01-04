# Streamlit Application

## Overview

Interactive dashboard for analyzing Jari Litmanen's career statistics with ML-powered insights.

## Quick Start

### Prerequisites
- Snowflake database `LITMANEN` created and populated
- Feature view `LITMANEN_FEATURES` accessible
- Python dependencies installed: `pip install -r ../requirements.txt`

### Running the App

1. **Configure Snowflake connection** (if not using MCP server):
   - Create `.env` file in project root with Snowflake credentials

2. **Launch Streamlit**:
   ```bash
   streamlit run streamlit/app.py
   ```

3. **Access the app**:
   - Open browser to `http://localhost:8501`
   - App will automatically load data from Snowflake

## Features

### Interactive Filters
- **Club**: Filter by specific clubs (Ajax, Liverpool, Barcelona, etc.)
- **Competition**: Filter by competition type (Champions League, Premier League, etc.)
- **Season Range**: Slider to select year range

### Visualizations
1. **Key Metrics**: Total seasons, appearances, minutes, average PPG
2. **Career Timeline**: Minutes ratio over time with low availability threshold
3. **Club Performance**: Total appearances by club
4. **Competition Analysis**: Performance scatter plot by competition
5. **Anomaly Detection**: Low availability periods that don't correlate with workload

### Data Table
- Detailed view of all filtered data
- Sortable columns
- Exportable data

## Troubleshooting

### Connection Issues
- Verify `.env` file has correct Snowflake credentials
- Check Snowflake warehouse is running
- Verify network connectivity

### Data Not Loading
- Check Snowflake database and schema exist
- Verify feature view is accessible
- Check query permissions

### Charts Not Displaying
- Ensure Plotly is installed: `pip install plotly`
- Check browser console for errors
- Try clearing browser cache

## Customization

### Adding New Charts
Edit `streamlit/app.py` and add new visualizations using Plotly or Streamlit charts.

### Changing Threshold
Modify the low availability threshold (currently 0.4) in the code or add as a sidebar parameter.

### Styling
Customize CSS in the `st.markdown()` section at thetop of `app.py`.
