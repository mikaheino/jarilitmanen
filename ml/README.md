# ML Model Training

## Overview

This directory contains the ML model training script for predicting Jari Litmanen's availability based on career statistics.

## Quick Start

### Prerequisites
- Snowflake database `LITMANEN` created and populated
- Feature view `LITMANEN_FEATURES` accessible
- Python dependencies installed: `pip install -r ../requirements.txt`

### Running the Model

1. **Configure Snowflake connection** (if not using MCP server):
   - Create `.env` file in project root with Snowflake credentials

2. **Train the model**:
   ```bash
   python ml/train_model.py
   ```

3. **Check outputs**:
   - Model file: `ml/model_*.pkl`
   - Feature importance: `ml/feature_importance.csv` (if Random Forest)

## Model Details

### Target Variable
- `label_low_availability`: Binary classification (1 if minutes_ratio < 0.4, else 0)

### Features Used
- appearances
- starts
- ppg (points per game)
- minutes
- appearance_ratio
- minutes_ratio
- season_start_year

### Models Tested
- Random Forest Classifier
- Logistic Regression

### Output
- Best performing model saved as pickle file
- Feature importance analysis (for tree-based models)
- Classification report with accuracy metrics

## Usage Example

```python
import pickle
import pandas as pd

# Load model
with open('ml/model_randomforest.pkl', 'rb') as f:
    model_data = pickle.load(f)
    model = model_data['model']
    feature_cols = model_data['feature_columns']

# Prepare features (example)
features = pd.DataFrame({
    'appearances': [20],
    'starts': [18],
    'ppg': [2.0],
    'minutes': [1500],
    'appearance_ratio': [0.8],
    'minutes_ratio': [0.75],
    'season_start_year': [2005]
})

# Predict
prediction = model.predict(features)
probability = model.predict_proba(features)[:, 1]

print(f"Low availability prediction: {prediction[0]}")
print(f"Probability: {probability[0]:.2%}")
```
