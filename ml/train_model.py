"""
ML Model Training - Step 40-43
Pull features with Snowpark, define target, train baseline model, persist model
"""
import os
import pickle
from dotenv import load_dotenv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import snowflake.connector

# Load environment variables
load_dotenv()

def get_snowflake_connection():
    """Create Snowflake connection"""
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

def pull_features():
    """Step 40: Pull features with Snowpark -> pandas"""
    print("Step 40: Pulling features from Snowflake...")
    
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    
    try:
        # Query the features view
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
        print(f"Pulled {len(df)} records from Snowflake")
        return df
        
    finally:
        cursor.close()
        conn.close()

def define_target(df):
    """Step 41: Define simple target - label_low_availability = minutes_ratio < 0.4"""
    print("\nStep 41: Defining target variable...")
    
    # Create target: low availability = minutes_ratio < 0.4
    df['label_low_availability'] = (df['minutes_ratio'] < 0.4).astype(int)
    
    # Show distribution
    print(f"Target distribution:")
    print(df['label_low_availability'].value_counts())
    print(f"\nLow availability rate: {df['label_low_availability'].mean():.2%}")
    
    return df

def prepare_features(df):
    """Prepare features for modeling"""
    # Select numeric features
    feature_cols = [
        'appearances',
        'starts',
        'ppg',
        'minutes',
        'appearance_ratio',
        'minutes_ratio',
        'season_start_year'
    ]
    
    # Create feature matrix
    X = df[feature_cols].fillna(0)
    y = df['label_low_availability']
    
    return X, y, feature_cols

def train_baseline_model(X_train, y_train, X_test, y_test):
    """Step 42: Train baseline model - Random Forest and Logistic Regression"""
    print("\nStep 42: Training baseline models...")
    
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5),
        'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        print(f"{name} Accuracy: {accuracy:.3f}")
        print(f"\n{classification_report(y_test, y_pred)}")
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
    
    # Select best model
    best_model_name = max(results, key=lambda k: results[k]['accuracy'])
    print(f"\nBest model: {best_model_name} (Accuracy: {results[best_model_name]['accuracy']:.3f})")
    
    return results[best_model_name]['model'], best_model_name, results

def persist_model(model, model_name, feature_cols):
    """Step 43: Persist model artifact"""
    print(f"\nStep 43: Persisting model '{model_name}'...")
    
    # Save model locally
    model_path = f'ml/model_{model_name.lower()}.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump({
            'model': model,
            'feature_columns': feature_cols,
            'model_name': model_name
        }, f)
    
    print(f"Model saved to: {model_path}")
    
    # Optionally save feature importance if Random Forest
    if hasattr(model, 'feature_importances_'):
        importance_df = pd.DataFrame({
            'feature': feature_cols,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        importance_path = 'ml/feature_importance.csv'
        importance_df.to_csv(importance_path, index=False)
        print(f"Feature importance saved to: {importance_path}")
        print("\nFeature Importance:")
        print(importance_df.to_string(index=False))
    
    return model_path

def main():
    """Main training pipeline"""
    print("=" * 60)
    print("Jari Litmanen ML Model Training")
    print("=" * 60)
    
    # Step 40: Pull features
    df = pull_features()
    
    # Step 41: Define target
    df = define_target(df)
    
    # Prepare features
    X, y, feature_cols = prepare_features(df)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    print(f"\nTrain set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Step 42: Train baseline model
    best_model, model_name, all_results = train_baseline_model(X_train, y_train, X_test, y_test)
    
    # Step 43: Persist model
    model_path = persist_model(best_model, model_name, feature_cols)
    
    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print(f"Best model: {model_name}")
    print(f"Model saved to: {model_path}")
    print("=" * 60)
    
    return best_model, model_name, all_results

if __name__ == "__main__":
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Warning: .env file not found. Using Snowflake MCP server connection.")
        print("If using direct connection, create .env file with Snowflake credentials.")
    
    try:
        model, name, results = main()
    except Exception as e:
        print(f"\nError during training: {e}")
        import traceback
        traceback.print_exc()
