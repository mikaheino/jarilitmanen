# Live Demo Script - Jari Litmanen ML Project

## Introduction (30 seconds)

"Today I'll demonstrate an ML-powered analysis of Jari Litmanen's football career. We'll see how we can predict player availability using historical data, and explore what machine learning can and cannot predict."

---

## Part 1: Show Databases (2 minutes)

### Step 1: Open Snowsight
"Let me start by showing you our Snowflake database structure."

**Action**: Open Snowsight, navigate to LITMANEN database

**Say**: "We have a database called LITMANEN with two schemas: RAW for raw data, and FEATURES for engineered features."

### Step 2: Show Raw Data
**Action**: Query `SELECT COUNT(*) FROM LITMANEN.RAW.PLAYER_SEASON_DATA;`

**Say**: "Our raw table contains 58 records covering Jari Litmanen's career from 1990 to 2011."

**Action**: Show sample data: `SELECT * FROM LITMANEN.RAW.PLAYER_SEASON_DATA LIMIT 5;`

**Say**: "Each record represents a season-competition combination with appearances, minutes, and points per game."

### Step 3: Show Feature View
**Action**: Query `SELECT * FROM LITMANEN.FEATURES.LITMANEN_FEATURES LIMIT 5;`

**Say**: "Our feature view adds calculated ratios that normalize the data across different competitions and seasons. This enables fair comparison throughout his career."

**Highlight**: Show `appearance_ratio`, `minutes_ratio`, `season_start_year`

---

## Part 2: Query Features (3 minutes)

### Query 1: Career Summary by Club
**Action**: Execute:
```sql
SELECT 
  club,
  COUNT(*) as seasons,
  SUM(appearances) as total_appearances,
  SUM(minutes) as total_minutes,
  AVG(ppg) as avg_points_per_game
FROM LITMANEN.FEATURES.LITMANEN_FEATURES
GROUP BY club
ORDER BY total_minutes DESC;
```

**Say**: "This shows Jari Litmanen's career broken down by club. You can see Ajax dominates with the most minutes, followed by Liverpool and Barcelona."

**Point Out**: 
- Ajax: Most appearances and minutes
- Barcelona: High average PPG
- Career progression from Finland to top European clubs

### Query 2: Performance by Competition
**Action**: Execute:
```sql
SELECT 
  competition,
  COUNT(*) as seasons,
  AVG(minutes_ratio) as avg_minutes_ratio,
  AVG(ppg) as avg_points_per_game
FROM LITMANEN.FEATURES.LITMANEN_FEATURES
GROUP BY competition
ORDER BY avg_minutes_ratio DESC;
```

**Say**: "This shows his performance across different competitions. Notice how minutes ratio varies - Champions League has different patterns than domestic leagues."

**Point Out**: Different competition types have different availability patterns

---

## Part 3: Run Streamlit (5 minutes)

### Step 1: Launch App
**Action**: Navigate to project directory, run `streamlit run streamlit/app.py`

**Say**: "Now let's see this data in an interactive dashboard built with Streamlit."

**Wait**: For app to load

### Step 2: Show Dashboard Overview
**Say**: "The dashboard shows key metrics at the top: total seasons, appearances, minutes, and average points per game."

**Action**: Point to metrics

### Step 3: Demonstrate Filters
**Say**: "We can filter by club, competition, and season range."

**Action**: 
- Select "Ajax" from club filter
- Show how charts update
- Select "Champions League" from competition filter
- Adjust year range slider

**Say**: "These filters allow us to explore different aspects of his career interactively."

### Step 4: Show Career Timeline Chart
**Say**: "The career timeline shows minutes ratio over time. The red dashed line marks our low availability threshold of 0.4."

**Action**: Point to timeline chart

**Point Out**:
- Early career: High minutes ratio
- Mid-career: Some dips (transfers, injuries)
- Late career: Return to Finland, different patterns

### Step 5: Show Club Performance
**Say**: "This bar chart shows total appearances by club. Ajax clearly dominates."

**Action**: Point to bar chart

### Step 6: Show Competition Analysis
**Say**: "This scatter plot shows performance by competition. Size represents total appearances."

**Action**: Point to scatter plot, hover over different competitions

**Point Out**: Different competitions cluster differently

### Step 7: Highlight Anomaly Section
**Say**: "Now, here's the interesting part - what ML cannot predict."

**Scroll**: To "What ML Cannot Predict" section

**Say**: "While our model can predict availability based on workload patterns, it cannot account for unusual injuries, transfer decisions, or personal circumstances."

**Action**: Show low availability periods table

**Say**: "These low availability periods don't always correlate with workload - they're influenced by factors our model can't see."

---

## Part 4: Change Threshold (2 minutes)

### Current Threshold
**Say**: "Our model uses a threshold of 0.4 for minutes ratio to define low availability."

**Action**: Point to threshold in code or explain

### Impact of Changing Threshold
**Say**: "If we change this threshold, say to 0.3 or 0.5, we'd get different predictions."

**Action**: If implemented in UI, change threshold; otherwise explain

**Say**: "This demonstrates how model parameters affect predictions. In production, we'd tune this based on business requirements."

---

## Part 5: ML Model Demo (3 minutes)

### Show Model File
**Action**: Navigate to `ml/` directory, show model file

**Say**: "We trained a Random Forest model that achieved good accuracy on our test set."

### Feature Importance
**Action**: Show feature importance if available

**Say**: "The model found that minutes ratio and appearance ratio are the most important features for predicting availability."

**Point Out**: Makes sense - these directly measure workload

### Model Predictions
**Say**: "The model can predict which seasons would have low availability based on workload patterns."

**Action**: Show example predictions if available

**Say**: "However, as we saw in the anomaly section, real-world factors can override these predictions."

---

## Conclusion (1 minute)

**Say**: "To summarize:
1. We built a complete ML pipeline from raw data to insights
2. Snowflake provides scalable data infrastructure
3. Streamlit enables interactive exploration
4. ML models can predict patterns, but have limitations
5. Human context and domain knowledge are essential"

**Say**: "This project demonstrates how modern data tools can provide insights into sports analytics, while acknowledging the complexity of real-world scenarios."

---

## Handling Questions

### "Why Jari Litmanen?"
- Interesting career spanning multiple top clubs
- Data availability and quality
- Demonstrates both predictable patterns and anomalies

### "Why these features?"
- Ratios normalize across competitions and seasons
- Enable fair comparison throughout career
- Capture relative workload patterns

### "Model accuracy?"
- Baseline model for demonstration
- Can be improved with more features
- Focus is on pipeline and insights, not perfect predictions

### "Production ready?"
- This is a demo/prototype
- Would need more data, better models, validation
- Shows the approach and potential

### "Next steps?"
- Add injury data for better predictions
- More sophisticated models
- Real-time predictions
- Expand to other players/teams

---

## Troubleshooting During Demo

### If Snowflake Connection Fails:
- "Let me check the connection..."
- Switch to backup screenshots
- Explain: "In production, we'd have robust connection handling"

### If Streamlit Doesn't Load:
- "Let me restart the app..."
- Show pre-recorded video
- Explain: "The app works, just having a connection issue"

### If Query Takes Too Long:
- "This query is taking a moment..."
- Show pre-computed results
- Explain: "In production, we'd optimize queries and use caching"

### If Model File Missing:
- "Let me train the model quickly..."
- Show feature importance from documentation
- Explain: "The model training process is straightforward"

---

## Key Phrases to Use

- "As you can see..."
- "Notice how..."
- "This demonstrates..."
- "The interesting part is..."
- "What ML cannot predict is..."
- "This ties back to our earlier point about..."

---

## Timing Reminders

- **Total**: 15 minutes
- **Don't rush**: Better to skip a section than rush through
- **Engage audience**: Ask if they have questions during demo
- **Be flexible**: Adjust based on audience interest
