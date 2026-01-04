"""
Streamlit App - Step 50-52
Connect to Snowflake, query features, create charts + narrative
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv
import snowflake.connector

# Load environment variables
load_dotenv()

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
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def get_snowflake_connection():
    """Create Snowflake connection"""
    try:
        conn = snowflake.connector.connect(
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database='LITMANEN',
            schema='FEATURES',
            role=os.getenv('SNOWFLAKE_ROLE', 'ACCOUNTADMIN')
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {e}")
        st.info("Note: If using Snowflake MCP server, you may need to configure .env file")
        return None

@st.cache_data(ttl=300)
def load_data():
    """Load data from Snowflake"""
    conn = get_snowflake_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        query = """
        SELECT 
            season,
            club,
            competition,
            appearances,
            starts,
            ppg,
            minutes,
            appearance_ratio,
            minutes_ratio,
            season_start_year
        FROM LITMANEN.FEATURES.LITMANEN_FEATURES
        ORDER BY season_start_year
        """
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        cursor.close()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
    finally:
        conn.close()

def main():
    """Main Streamlit app"""
    # Header
    st.markdown('<div class="main-header">⚽ Jari Litmanen Career Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">ML-Powered Career Statistics & Availability Analysis</div>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    if df is None:
        st.stop()
    
    # Sidebar
    st.sidebar.header("Filters")
    
    # Club filter
    clubs = ['All'] + sorted(df['club'].unique().tolist())
    selected_club = st.sidebar.selectbox("Select Club", clubs)
    
    # Competition filter
    competitions = ['All'] + sorted(df['competition'].unique().tolist())
    selected_competition = st.sidebar.selectbox("Select Competition", competitions)
    
    # Year range filter
    min_year = int(df['season_start_year'].min())
    max_year = int(df['season_start_year'].max())
    year_range = st.sidebar.slider("Season Range", min_year, max_year, (min_year, max_year))
    
    # Filter data
    filtered_df = df[
        (df['season_start_year'] >= year_range[0]) &
        (df['season_start_year'] <= year_range[1])
    ]
    
    if selected_club != 'All':
        filtered_df = filtered_df[filtered_df['club'] == selected_club]
    
    if selected_competition != 'All':
        filtered_df = filtered_df[filtered_df['competition'] == selected_competition]
    
    # Key Metrics
    st.header("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Seasons", len(filtered_df))
    with col2:
        st.metric("Total Appearances", int(filtered_df['appearances'].sum()))
    with col3:
        st.metric("Total Minutes", f"{int(filtered_df['minutes'].sum()):,}")
    with col4:
        st.metric("Avg Points/Game", f"{filtered_df['ppg'].mean():.2f}")
    
    # Chart 1: Minutes Ratio Over Time
    st.header("📈 Career Timeline: Minutes Ratio")
    fig1 = px.line(
        filtered_df,
        x='season_start_year',
        y='minutes_ratio',
        color='club',
        markers=True,
        title='Minutes Ratio by Season',
        labels={'season_start_year': 'Season Start Year', 'minutes_ratio': 'Minutes Ratio'}
    )
    fig1.add_hline(y=0.4, line_dash="dash", line_color="red", 
                   annotation_text="Low Availability Threshold (0.4)")
    st.plotly_chart(fig1, use_container_width=True)
    
    # Chart 2: Appearances by Club
    st.header("🏆 Appearances by Club")
    club_stats = filtered_df.groupby('club').agg({
        'appearances': 'sum',
        'minutes': 'sum',
        'ppg': 'mean'
    }).reset_index().sort_values('appearances', ascending=False)
    
    fig2 = px.bar(
        club_stats,
        x='club',
        y='appearances',
        title='Total Appearances by Club',
        labels={'appearances': 'Total Appearances', 'club': 'Club'}
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Chart 3: Performance by Competition
    st.header("🎯 Performance by Competition")
    comp_stats = filtered_df.groupby('competition').agg({
        'minutes_ratio': 'mean',
        'ppg': 'mean',
        'appearances': 'sum'
    }).reset_index().sort_values('minutes_ratio', ascending=False)
    
    fig3 = px.scatter(
        comp_stats,
        x='minutes_ratio',
        y='ppg',
        size='appearances',
        hover_name='competition',
        title='Performance by Competition',
        labels={'minutes_ratio': 'Average Minutes Ratio', 'ppg': 'Average Points per Game'}
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
    low_availability = filtered_df[filtered_df['minutes_ratio'] < 0.4].copy()
    
    if len(low_availability) > 0:
        anomaly_df = low_availability[['season', 'club', 'competition', 'minutes_ratio', 'ppg']].sort_values('season_start_year')
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
        filtered_df[['season', 'club', 'competition', 'appearances', 'minutes', 'ppg', 
                    'minutes_ratio', 'season_start_year']].sort_values('season_start_year'),
        use_container_width=True,
        height=400
    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Data Source**: Jari Litmanen Career Statistics (1990-2011)  
    **Analysis**: ML-powered availability prediction with anomaly detection  
    **Built with**: Snowflake, Streamlit, Plotly
    """)

if __name__ == "__main__":
    main()
