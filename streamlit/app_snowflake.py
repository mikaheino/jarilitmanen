"""
Snowflake Native Streamlit App - Step 50-52
Runs directly inside Snowflake using Snowflake's Streamlit support
"""
import streamlit as st
from snowflake.snowpark import Session
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Jari Litmanen Career Analysis",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Snowflake session
@st.cache_resource
def init_session():
    """Initialize Snowflake session using Streamlit's connection"""
    try:
        conn = st.connection("snowflake")
        return conn.session()
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {e}")
        import traceback
        st.code(traceback.format_exc())
        st.stop()

@st.cache_data(ttl=300)
def load_data(_session):
    """Load data from Snowflake using Snowpark"""
    try:
        df = _session.table("LITMANEN.FEATURES.LITMANEN_FEATURES")
        pandas_df = df.to_pandas()
        
        # Convert all numeric columns explicitly
        numeric_cols = ['APPEARANCES', 'STARTS', 'MINUTES', 'PPG', 'APPEARANCE_RATIO', 'MINUTES_RATIO', 'SEASON_START_YEAR']
        for col_name in numeric_cols:
            if col_name in pandas_df.columns:
                pandas_df[col_name] = pd.to_numeric(pandas_df[col_name], errors='coerce')
        
        return pandas_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        import traceback
        st.code(traceback.format_exc())
        return None

def safe_int(value):
    """Safely convert value to int"""
    try:
        if pd.isna(value):
            return 0
        return int(float(value))
    except:
        return 0

def safe_float(value):
    """Safely convert value to float"""
    try:
        if pd.isna(value):
            return 0.0
        return float(value)
    except:
        return 0.0

def main():
    """Main Streamlit app"""
    # Header
    st.markdown('<div class="main-header">⚽ Jari Litmanen Career Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">ML-Powered Career Statistics & Availability Analysis</div>', unsafe_allow_html=True)
    
    # Initialize session
    try:
        session = init_session()
    except Exception as e:
        st.error(f"Error initializing session: {e}")
        import traceback
        st.code(traceback.format_exc())
        st.stop()
    
    # Load data
    df = load_data(session)
    
    if df is None or df.empty:
        st.error("Unable to load data. Please check your Snowflake connection.")
        st.stop()
    
    # Sidebar
    st.sidebar.header("Filters")
    
    # Club filter
    try:
        club_values = [str(c) for c in df['CLUB'].dropna().unique() if c is not None]
        clubs = ['All'] + sorted(club_values)
        selected_club = st.sidebar.selectbox("Select Club", clubs)
    except Exception as e:
        st.sidebar.error(f"Error loading clubs: {e}")
        selected_club = 'All'
        clubs = ['All']
    
    # Competition filter
    try:
        comp_values = [str(c) for c in df['COMPETITION'].dropna().unique() if c is not None]
        competitions = ['All'] + sorted(comp_values)
        selected_competition = st.sidebar.selectbox("Select Competition", competitions)
    except Exception as e:
        st.sidebar.error(f"Error loading competitions: {e}")
        selected_competition = 'All'
        competitions = ['All']
    
    # Year range filter
    try:
        year_col = df['SEASON_START_YEAR'].dropna()
        if len(year_col) > 0:
            min_year = safe_int(year_col.min())
            max_year = safe_int(year_col.max())
        else:
            min_year = 1990
            max_year = 2011
        
        year_range = st.sidebar.slider("Season Range", min_year, max_year, (min_year, max_year))
        
        # Extract year values safely
        if isinstance(year_range, (list, tuple)) and len(year_range) >= 2:
            year_min = safe_int(year_range[0])
            year_max = safe_int(year_range[1])
        else:
            year_min = safe_int(year_range)
            year_max = safe_int(year_range)
    except Exception as e:
        st.sidebar.error(f"Error setting year range: {e}")
        year_min = 1990
        year_max = 2011
        year_range = (1990, 2011)
    
    # Filter data
    try:
        year_col_filter = pd.to_numeric(df['SEASON_START_YEAR'], errors='coerce').fillna(0)
        filtered_df = df[
            (year_col_filter >= year_min) &
            (year_col_filter <= year_max)
        ].copy()
        
        if selected_club != 'All':
            filtered_df = filtered_df[filtered_df['CLUB'] == selected_club]
        
        if selected_competition != 'All':
            filtered_df = filtered_df[filtered_df['COMPETITION'] == selected_competition]
    except Exception as e:
        st.error(f"Error filtering data: {e}")
        import traceback
        st.code(traceback.format_exc())
        filtered_df = df.copy()
    
    # Key Metrics
    st.header("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        with col1:
            st.metric("Total Seasons", len(filtered_df))
        with col2:
            appearances_sum = pd.to_numeric(filtered_df['APPEARANCES'], errors='coerce').fillna(0).sum()
            st.metric("Total Appearances", safe_int(appearances_sum))
        with col3:
            minutes_sum = pd.to_numeric(filtered_df['MINUTES'], errors='coerce').fillna(0).sum()
            st.metric("Total Minutes", f"{safe_int(minutes_sum):,}")
        with col4:
            ppg_mean = pd.to_numeric(filtered_df['PPG'], errors='coerce').fillna(0).mean()
            st.metric("Avg Points/Game", f"{ppg_mean:.2f}")
    except Exception as e:
        st.error(f"Error calculating metrics: {e}")
    
    # Chart 1: Minutes Ratio Over Time
    st.header("📈 Career Timeline: Minutes Ratio")
    
    try:
        import plotly.express as px
        
        chart_df = filtered_df[['SEASON_START_YEAR', 'MINUTES_RATIO', 'CLUB']].copy()
        chart_df['SEASON_START_YEAR'] = pd.to_numeric(chart_df['SEASON_START_YEAR'], errors='coerce')
        chart_df['MINUTES_RATIO'] = pd.to_numeric(chart_df['MINUTES_RATIO'], errors='coerce')
        chart_df = chart_df.dropna(subset=['SEASON_START_YEAR', 'MINUTES_RATIO'])
        
        if len(chart_df) > 0:
            fig1 = px.line(
                chart_df,
                x='SEASON_START_YEAR',
                y='MINUTES_RATIO',
                color='CLUB',
                markers=True,
                title='Minutes Ratio by Season',
                labels={'SEASON_START_YEAR': 'Season Start Year', 'MINUTES_RATIO': 'Minutes Ratio'}
            )
            fig1.add_hline(y=0.4, line_dash="dash", line_color="red", 
                           annotation_text="Low Availability Threshold (0.4)")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("No data available for the selected filters.")
    except Exception as e:
        st.error(f"Error creating timeline chart: {e}")
        import traceback
        st.code(traceback.format_exc())
    
    # Chart 2: Appearances by Club
    st.header("🏆 Appearances by Club")
    try:
        club_stats = filtered_df.groupby('CLUB').agg({
            'APPEARANCES': lambda x: pd.to_numeric(x, errors='coerce').fillna(0).sum(),
            'MINUTES': lambda x: pd.to_numeric(x, errors='coerce').fillna(0).sum(),
            'PPG': lambda x: pd.to_numeric(x, errors='coerce').fillna(0).mean()
        }).reset_index()
        club_stats = club_stats.sort_values('APPEARANCES', ascending=False)
        
        import plotly.express as px
        fig2 = px.bar(
            club_stats,
            x='CLUB',
            y='APPEARANCES',
            title='Total Appearances by Club',
            labels={'APPEARANCES': 'Total Appearances', 'CLUB': 'Club'}
        )
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating club chart: {e}")
        import traceback
        st.code(traceback.format_exc())
    
    # Chart 3: Performance by Competition
    st.header("🎯 Performance by Competition")
    try:
        comp_stats = filtered_df.groupby('COMPETITION').agg({
            'MINUTES_RATIO': lambda x: pd.to_numeric(x, errors='coerce').fillna(0).mean(),
            'PPG': lambda x: pd.to_numeric(x, errors='coerce').fillna(0).mean(),
            'APPEARANCES': lambda x: pd.to_numeric(x, errors='coerce').fillna(0).sum()
        }).reset_index()
        comp_stats = comp_stats.sort_values('MINUTES_RATIO', ascending=False)
        
        import plotly.express as px
        fig3 = px.scatter(
            comp_stats,
            x='MINUTES_RATIO',
            y='PPG',
            size='APPEARANCES',
            hover_name='COMPETITION',
            title='Performance by Competition',
            labels={'MINUTES_RATIO': 'Average Minutes Ratio', 'PPG': 'Average Points per Game'}
        )
        st.plotly_chart(fig3, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating competition chart: {e}")
        import traceback
        st.code(traceback.format_exc())
    
    # Step 51: What ML Cannot Predict
    st.header("🚑 What ML Cannot Predict: Unusual Injuries & Anomalies")
    st.markdown("""
    ### The Human Element in Sports Analytics
    
    While machine learning models can predict availability based on workload patterns, 
    they cannot account for the unpredictable nature of injuries, especially unusual ones.
    
    **Known Anomalies in Jari Litmanen's Career:**
    - **1999-2000**: Transfer to Barcelona, limited playing time despite high performance
    - **2000-2001**: Brief return to Barcelona, then move to Liverpool mid-season
    - **2004-2005**: Return to Finland, playing in Bundesliga with Hansa Rostock
    - **Various seasons**: Unusual injury patterns that don't correlate with workload
    
    These anomalies highlight the limitations of purely data-driven predictions in sports.
    """)
    
    # Highlight anomalies
    st.subheader("📉 Low Availability Periods")
    try:
        minutes_ratio_col = pd.to_numeric(filtered_df['MINUTES_RATIO'], errors='coerce').fillna(1.0)
        low_availability = filtered_df[minutes_ratio_col < 0.4].copy()
        
        if len(low_availability) > 0:
            anomaly_df = low_availability[['SEASON', 'CLUB', 'COMPETITION', 'MINUTES_RATIO', 'PPG']].copy()
            if 'SEASON_START_YEAR' in anomaly_df.columns:
                anomaly_df['SEASON_START_YEAR'] = pd.to_numeric(anomaly_df['SEASON_START_YEAR'], errors='coerce')
                anomaly_df = anomaly_df.sort_values('SEASON_START_YEAR')
            else:
                anomaly_df = anomaly_df.sort_values('SEASON')
            st.dataframe(anomaly_df, use_container_width=True)
            
            st.markdown("""
            **Analysis**: These low-availability periods may not always correlate with 
            workload patterns, demonstrating the complexity of predicting athlete availability.
            """)
        else:
            st.info("No low availability periods found in the filtered data.")
    except Exception as e:
        st.warning(f"Error displaying anomalies: {e}")
    
    # Data Table
    st.header("📋 Detailed Data")
    try:
        display_cols = ['SEASON', 'CLUB', 'COMPETITION', 'APPEARANCES', 'MINUTES', 'PPG', 'MINUTES_RATIO']
        if 'SEASON_START_YEAR' in filtered_df.columns:
            display_cols.append('SEASON_START_YEAR')
            sort_col = 'SEASON_START_YEAR'
        else:
            sort_col = 'SEASON'
        
        display_df = filtered_df[display_cols].copy()
        if sort_col in display_df.columns:
            display_df[sort_col] = pd.to_numeric(display_df[sort_col], errors='coerce')
            display_df = display_df.sort_values(sort_col)
        st.dataframe(display_df, use_container_width=True, height=400)
    except Exception as e:
        st.error(f"Error displaying data table: {e}")
        import traceback
        st.code(traceback.format_exc())
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Data Source**: Jari Litmanen Career Statistics (1990-2011)  
    **Analysis**: ML-powered availability prediction with anomaly detection  
    **Built with**: Snowflake Native Streamlit, Snowpark, Plotly
    """)

if __name__ == "__main__":
    main()
