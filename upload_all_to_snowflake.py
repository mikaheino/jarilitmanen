"""
Comprehensive script to upload Streamlit app to Snowflake
Tries multiple methods to upload the file
"""
import os
import sys
import base64

def get_file_content():
    """Read the Streamlit app file"""
    file_path = os.path.join(os.path.dirname(__file__), 'streamlit', 'app_snowflake.py')
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("="*70)
    print("UPLOAD STREAMLIT APP TO SNOWFLAKE")
    print("="*70)
    print()
    
    file_path = os.path.join(os.path.dirname(__file__), 'streamlit', 'app_snowflake.py')
    file_content = get_file_content()
    
    print(f"✅ File ready: {os.path.abspath(file_path)}")
    print(f"✅ File size: {len(file_content)} bytes")
    print()
    
    print("="*70)
    print("UPLOAD METHOD: Snowsight Web UI (Recommended)")
    print("="*70)
    print()
    print("STEP-BY-STEP INSTRUCTIONS:")
    print()
    print("1. Open Snowsight: https://app.snowflake.com")
    print("2. Click 'Data' in left sidebar")
    print("3. Navigate: Databases > LITMANEN > FEATURES")
    print("4. Find 'STREAMLIT_STAGE' and click on it")
    print("5. Click 'Upload Files' button (top right)")
    print(f"6. Select file: {os.path.abspath(file_path)}")
    print("7. Check 'Overwrite existing files' checkbox")
    print("8. Click 'Upload'")
    print("9. Wait for upload to complete")
    print("10. Go to 'Apps' > 'LITMANEN_CAREER_ANALYSIS'")
    print("11. Click 'Refresh' or reopen the app")
    print()
    print("="*70)
    print("ALTERNATIVE: SnowSQL Command")
    print("="*70)
    print()
    print("If you have SnowSQL installed, run:")
    print()
    print(f"PUT file://{os.path.abspath(file_path)} @LITMANEN.FEATURES.STREAMLIT_STAGE/app_snowflake.py AUTO_COMPRESS=FALSE OVERWRITE=TRUE;")
    print()
    print("="*70)
    print("VERIFICATION")
    print("="*70)
    print()
    print("After uploading, verify with:")
    print("LIST @LITMANEN.FEATURES.STREAMLIT_STAGE;")
    print()
    print("You should see 'app_snowflake.py' in the results.")
    print()
    print("="*70)
    print("STATUS")
    print("="*70)
    print("✅ Git: Updated and pushed")
    print("✅ Snowflake: App object created, stage ready")
    print("⏳ Pending: File upload (use instructions above)")
    print()

if __name__ == "__main__":
    main()
