# Jari Litmanen ML Project - Presentation Guide

## Story Arc Slides (Step 60)

### Slide 1: Title Slide
**Title**: ML-Powered Career Analysis: Predicting Jari Litmanen's Availability

**Subtitle**: From Raw Data to Actionable Insights

**Key Points**:
- Data-driven approach to sports analytics
- Real-world application of ML in football
- Snowflake + Python + Streamlit stack

---

### Slide 2: Data Source
**Title**: The Data: Jari Litmanen's Illustrious Career

**Content**:
- **Source**: Career statistics 1990-2011
- **Coverage**: 58 seasons across multiple clubs and competitions
- **Clubs**: Ajax, Barcelona, Liverpool, FC Lahti, HJK Helsinki, and more
- **Competitions**: Champions League, Premier League, LaLiga, Eredivisie, Veikkausliiga
- **Metrics**: Appearances, starts, minutes, points per game

**Visual**: Timeline showing career progression

**Key Message**: Rich, historical dataset spanning 21 years of professional football

---

### Slide 3: Pipeline Architecture
**Title**: Data Pipeline: From CSV to Insights

**Content**:
```
Raw CSV → Snowflake RAW Schema → Feature Engineering → ML Model → Streamlit App
```

**Components**:
1. **Data Ingestion**: CSV files loaded into Snowflake
2. **Raw Layer**: `LITMANEN.RAW.PLAYER_SEASON_DATA`
3. **Feature Layer**: `LITMANEN.FEATURES.LITMANEN_FEATURES`
   - Calculated ratios (appearance_ratio, minutes_ratio)
   - Season normalization (season_start_year)
4. **ML Layer**: Random Forest / Logistic Regression models
5. **Visualization**: Streamlit interactive dashboard

**Visual**: Architecture diagram

**Key Message**: Clean, scalable pipeline from raw data to production-ready insights

---

### Slide 4: Feature Engineering
**Title**: Feature Engineering: Transforming Raw Stats

**Content**:
- **Raw Features**: appearances, starts, minutes, ppg
- **Derived Features**:
  - `appearance_ratio`: Player appearances / Max appearances in competition/season
  - `minutes_ratio`: Player minutes / Max minutes in competition/season
  - `season_start_year`: Normalized year for temporal analysis

**Why These Features?**
- Ratios normalize across different competitions and seasons
- Enable fair comparison across career timeline
- Capture relative workload and availability

**Visual**: Before/after feature comparison

**Key Message**: Smart feature engineering enables better predictions

---

### Slide 5: ML Model
**Title**: Machine Learning: Predicting Low Availability

**Content**:
- **Target Variable**: `label_low_availability` (minutes_ratio < 0.4)
- **Models Tested**:
  - Random Forest Classifier
  - Logistic Regression
- **Features Used**: 7 numeric features (appearances, starts, ppg, minutes, ratios, season_year)
- **Performance**: Baseline models for demonstration

**Model Selection**:
- Best performing model selected based on accuracy
- Feature importance analysis
- Model persistence for production use

**Visual**: Model comparison chart, feature importance

**Key Message**: ML models can predict availability patterns, but have limitations

---

### Slide 6: Streamlit Application
**Title**: Interactive Dashboard: Real-Time Analysis

**Content**:
- **Key Visualizations**:
  - Career timeline: Minutes ratio over time
  - Club performance: Total appearances by club
  - Competition analysis: Performance scatter plots
- **Filters**: Club, competition, season range
- **Metrics**: Total seasons, appearances, minutes, avg PPG

**Features**:
- Real-time data from Snowflake
- Interactive charts with Plotly
- Anomaly detection and highlighting

**Visual**: Screenshot of Streamlit app

**Key Message**: Democratizing data insights through interactive visualization

---

### Slide 7: What ML Cannot Predict
**Title**: The Human Element: Unusual Injuries & Anomalies

**Content**:
- **Limitations of ML in Sports**:
  - Cannot predict unusual injuries
  - Transfer decisions and team dynamics
  - Personal circumstances
  - Random events

**Jari Litmanen's Anomalies**:
- 1999-2000: Transfer to Barcelona, limited playing time
- 2000-2001: Mid-season transfers
- Various seasons: Injury patterns not correlated with workload

**Visual**: Anomaly timeline, low availability periods

**Key Message**: ML is powerful, but human context matters

**Tie to Litmanen**: His career had many unpredictable moments that data alone couldn't explain

---

### Slide 8: Lessons Learned
**Title**: Key Takeaways

**Content**:
1. **Data Quality Matters**: Clean, normalized data enables better models
2. **Feature Engineering is Critical**: Ratios and normalization improve predictions
3. **ML Has Limitations**: Cannot account for all human factors
4. **Visualization Adds Value**: Interactive dashboards make insights accessible
5. **Real-World Context**: Domain knowledge enhances ML predictions

**Technical Lessons**:
- Snowflake provides scalable data infrastructure
- Streamlit enables rapid dashboard development
- Baseline models can provide valuable insights

**Visual**: Key points with icons

**Key Message**: Combining ML with domain expertise yields best results

---

## Live Demo Checklist (Step 61)

### Pre-Demo Setup
- [ ] Snowflake database `LITMANEN` is created and populated
- [ ] Feature view `LITMANEN_FEATURES` is accessible
- [ ] Python environment has all dependencies installed
- [ ] `.env` file configured (or MCP server connected)
- [ ] Streamlit app tested locally
- [ ] ML model trained and saved
- [ ] Backup screenshots prepared

### Demo Flow

#### 1. Show Databases (2 minutes)
- [ ] Open Snowsight
- [ ] Show `LITMANEN` database structure
- [ ] Show `RAW` schema with `PLAYER_SEASON_DATA` table
- [ ] Show `FEATURES` schema with `LITMANEN_FEATURES` view
- [ ] Query: `SELECT COUNT(*) FROM LITMANEN.RAW.PLAYER_SEASON_DATA;`
- [ ] Expected: 58 records

#### 2. Query Features (3 minutes)
- [ ] Query feature view: `SELECT * FROM LITMANEN.FEATURES.LITMANEN_FEATURES LIMIT 10;`
- [ ] Show calculated ratios
- [ ] Show season normalization
- [ ] Query: Career summary by club
- [ ] Query: Performance by competition

#### 3. Run Streamlit (5 minutes)
- [ ] Navigate to project directory
- [ ] Run: `streamlit run streamlit/app.py`
- [ ] Show dashboard loading
- [ ] Demonstrate filters (club, competition, year range)
- [ ] Show key metrics
- [ ] Show career timeline chart
- [ ] Show club performance chart
- [ ] Show competition analysis
- [ ] Highlight anomaly section

#### 4. Change Threshold (2 minutes)
- [ ] Explain low availability threshold (currently 0.4)
- [ ] Modify threshold in sidebar (if implemented) or code
- [ ] Show how results change
- [ ] Discuss impact on predictions

#### 5. ML Model Demo (3 minutes)
- [ ] Show trained model file
- [ ] Explain feature importance
- [ ] Show model predictions
- [ ] Discuss accuracy and limitations

### Backup Plan
- [ ] Screenshot deck ready if live demo fails
- [ ] Pre-recorded video as fallback
- [ ] Static charts prepared
- [ ] Sample queries ready to copy/paste

### Q&A Preparation
- [ ] Why Jari Litmanen? (Interesting career, data availability)
- [ ] Why these features? (Normalization, comparability)
- [ ] Model accuracy? (Baseline model, can be improved)
- [ ] Production readiness? (Demo, needs refinement)
- [ ] Next steps? (More features, better models, injury data)

### Time Allocation
- **Total**: ~15 minutes
- **Setup**: 2 minutes
- **Database/Queries**: 5 minutes
- **Streamlit Demo**: 5 minutes
- **ML Model**: 3 minutes
- **Q&A**: 5 minutes (if time permits)

---

## Presentation Tips

1. **Start with the Story**: Why Jari Litmanen? Why ML for sports?
2. **Show, Don't Tell**: Live demos are more engaging than slides
3. **Highlight Anomalies**: Makes it memorable and shows ML limitations
4. **Keep It Simple**: Focus on insights, not technical complexity
5. **Be Honest**: Acknowledge limitations and areas for improvement

---

## Visual Assets Needed

1. **Architecture Diagram**: Data pipeline flow
2. **Feature Engineering**: Before/after comparison
3. **Model Comparison**: Accuracy metrics
4. **Dashboard Screenshots**: Streamlit app views
5. **Anomaly Timeline**: Low availability periods
6. **Career Timeline**: Visual progression

---

## Key Messages to Emphasize

1. **Data-Driven Insights**: ML enables new perspectives on sports data
2. **Practical Application**: Real-world use case with real data
3. **Technology Stack**: Modern tools (Snowflake, Python, Streamlit)
4. **Limitations Awareness**: ML is powerful but not perfect
5. **Human Context**: Domain knowledge enhances ML predictions
