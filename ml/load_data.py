"""
Load CSV data into Snowflake table
Step 23: Load CSV to table
"""
import csv
import os
from dotenv import load_dotenv
from snowflake.connector import connect

# Load environment variables
load_dotenv()

# Snowflake connection parameters
conn_params = {
    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
    'user': os.getenv('SNOWFLAKE_USER'),
    'password': os.getenv('SNOWFLAKE_PASSWORD'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
    'database': 'LITMANEN',
    'schema': 'RAW',
    'role': os.getenv('SNOWFLAKE_ROLE', 'ACCOUNTADMIN')
}

def load_csv_to_snowflake(csv_file_path):
    """Load CSV data into Snowflake table"""
    conn = connect(**conn_params)
    cursor = conn.cursor()
    
    try:
        # Clear existing data
        cursor.execute("TRUNCATE TABLE LITMANEN.RAW.PLAYER_SEASON_DATA")
        
        # Read CSV and insert data
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Handle empty ppg values
                ppg = row['ppg'] if row['ppg'] else None
                
                insert_sql = """
                    INSERT INTO LITMANEN.RAW.PLAYER_SEASON_DATA 
                    (season, competition, club, appearances, starts, ppg, minutes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_sql, (
                    row['season'],
                    row['competition'],
                    row['club'],
                    int(row['appearances']),
                    int(row['starts']),
                    float(ppg) if ppg else None,
                    int(row['minutes'])
                ))
        
        conn.commit()
        print(f"Successfully loaded data from {csv_file_path}")
        
    except Exception as e:
        print(f"Error loading data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'litmanen_career_dataset_full.csv')
    load_csv_to_snowflake(csv_path)
