"""
Snowflake Native Streamlit App - Step 50-52
Runs directly inside Snowflake using Snowflake's Streamlit support
"""
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, sum as sum_func, avg, count, max as max_func
import pandas as pd

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
    # Snowflake Streamlit apps automatically provide a session
    # Access it via st.connection or create new session
    try:
        # Try to use Streamlit's Snowflake connection
        conn = st.connection("snowflake")
        return conn.session()
    except:
        # Fallback: create session from config
        import os
        from snowflake.snowpark import Session
        
        connection_parameters = {
            "account": os.getenv("SNOWFLAKE_ACCOUNT"),
            "user": os.getenv("SNOWFLAKE_USER"),
            "password": os.getenv("SNOWFLAKE_PASSWORD"),
            "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
            "database": "LITMANEN",
            "schema": "FEATURES",
            "role": os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
        }
        return Session.builder.configs(connection_parameters).create()

@st.cache_data(ttl=300)
def load_data(_session):
    """Load data from Snowflake using Snowpark"""
    try:
        # Query the features view using Snowpark DataFrame
        df = _session.table("LITMANEN.FEATURES.LITMANEN_FEATURES")
        
        # Convert to pandas for easier manipulation
        pandas_df = df.to_pandas()
        
        return pandas_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    """Main Streamlit app"""
    # Header
    st.markdown('<div class="main-header">⚽ Jari Litmanen Career Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">ML-Powered Career Statistics & Availability Analysis</div>', unsafe_allow_html=True)
    
    # Initialize session
    session = init_session()
    
    # Load data
    df = load_data(session)
    
    if df is None or df.empty:
        st.error("Unable to load data. Please check your Snowflake connection.")
        st.stop()
    
    # Sidebar
    st.sidebar.header("Filters")
    
    # Club filter
    clubs = ['All'] + sorted(df['CLUB'].unique().tolist())
    selected_club = st.sidebar.selectbox("Select Club", clubs)
    
    # Competition filter
    competitions = ['All'] + sorted(df['COMPETITION'].unique().tolist())
    selected_competition = st.sidebar.selectbox("Select Competition", competitions)
    
    # Year range filter
    min_year = int(df['SEASON_START_YEAR'].min())
    max_year = int(df['SEASON_START_YEAR'].max())
    year_range = st.sidebar.slider("Season Range", min_year, max_year, (min_year, max_year))
    
    # Filter data
    filtered_df = df[
        (df['SEASON_START_YEAR'] >= year_range[0]) &
        (df['SEASON_START_YEAR'] <= year_range[1])
    ]
    
    if selected_club != 'All':
        filtered_df = filtered_df[filtered_df['CLUB'] == selected_club]
    
    if selected_competition != 'All':
        filtered_df = filtered_df[filtered_df['COMPETITION'] == selected_competition]
    
    # Key Metrics
    st.header("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Seasons", len(filtered_df))
    with col2:
        st.metric("Total Appearances", int(filtered_df['APPEARANCES'].sum()))
    with col3:
        st.metric("Total Minutes", f"{int(filtered_df['MINUTES'].sum()):,}")
    with col4:
        st.metric("Avg Points/Game", f"{filtered_df['PPG'].mean():.2f}")
    
    # Chart 1: Minutes Ratio Over Time
    st.header("📈 Career Timeline: Minutes Ratio")
    
    # Use Snowpark DataFrame for better performance
    try:
        # Create filtered Snowpark DataFrame
        snowpark_df = session.table("LITMANEN.FEATURES.LITMANEN_FEATURES")
        
        # Apply filters
        if selected_club != 'All':
            snowpark_df = snowpark_df.filter(col("CLUB") == selected_club)
        if selected_competition != 'All':
            snowpark_df = snowpark_df.filter(col("COMPETITION") == selected_competition)
        snowpark_df = snowpark_df.filter(
            (col("SEASON_START_YEAR") >= year_range[0]) &
            (col("SEASON_START_YEAR") <= year_range[1])
        )
        
        # Convert to pandas for plotting
        chart_df = snowpark_df.select(
            col("SEASON_START_YEAR"),
            col("MINUTES_RATIO"),
            col("CLUB")
        ).to_pandas()
        
        # Create chart
        import plotly.express as px
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
    except Exception as e:
        st.warning(f"Could not create Snowpark chart, using pandas fallback: {e}")
        # Fallback to pandas
        import plotly.express as px
        fig1 = px.line(
            filtered_df,
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
    
    # Chart 2: Appearances by Club
    st.header("🏆 Appearances by Club")
    club_stats = filtered_df.groupby('CLUB').agg({
        'APPEARANCES': 'sum',
        'MINUTES': 'sum',
        'PPG': 'mean'
    }).reset_index().sort_values('APPEARANCES', ascending=False)
    
    import plotly.express as px
    fig2 = px.bar(
        club_stats,
        x='CLUB',
        y='APPEARANCES',
        title='Total Appearances by Club',
        labels={'APPEARANCES': 'Total Appearances', 'CLUB': 'Club'}
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Chart 3: Performance by Competition
    st.header("🎯 Performance by Competition")
    comp_stats = filtered_df.groupby('COMPETITION').agg({
        'MINUTES_RATIO': 'mean',
        'PPG': 'mean',
        'APPEARANCES': 'sum'
    }).reset_index().sort_values('MINUTES_RATIO', ascending=False)
    
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
    
    # Step 51: What ML Cannot Predict - Unusual Injuries Section
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
    
    # Highlight anomalies in the data
    st.subheader("📉 Low Availability Periods")
    low_availability = filtered_df[filtered_df['MINUTES_RATIO'] < 0.4].copy()
    
    if len(low_availability) > 0:
        anomaly_df = low_availability[['SEASON', 'CLUB', 'COMPETITION', 'MINUTES_RATIO', 'PPG']].sort_values('SEASON_START_YEAR')
        st.dataframe(anomaly_df, use_container_width=True)
        
        st.markdown("""
        **Analysis**: These low-availability periods may not always correlate with 
        workload patterns, demonstrating the complexity of predicting athlete availability.
        """)
    else:
        st.info("No low availability periods found in the filtered data.")
    
    # Data Table
    st.header("📋 Detailed Data")
    st.dataframe(
        filtered_df[['SEASON', 'CLUB', 'COMPETITION', 'APPEARANCES', 'MINUTES', 'PPG', 
                    'MINUTES_RATIO', 'SEASON_START_YEAR']].sort_values('SEASON_START_YEAR'),
        use_container_width=True,
        height=400
    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Data Source**: Jari Litmanen Career Statistics (1990-2011)  
    **Analysis**: ML-powered availability prediction with anomaly detection  
    **Built with**: Snowflake Native Streamlit, Snowpark, Plotly
    """)

if __name__ == "__main__":
    main()
