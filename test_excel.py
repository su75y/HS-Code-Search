import pandas as pd
import os

def test_excel_file(file_path):
    print(f"\nTesting file: {file_path}")
    if not os.path.exists(file_path):
        print(f"ERROR: File not found at {file_path}")
        return False
    
    try:
        df = pd.read_excel(file_path)
        print("SUCCESS: File loaded successfully")
        print("Columns:", df.columns.tolist())
        print("\nFirst row:")
        print(df.iloc[0])
        return True
    except Exception as e:
        print(f"ERROR: Could not read file: {str(e)}")
        return False

# Test both Excel files
current_dir = os.path.dirname(os.path.abspath(__file__))
des_hsc_path = os.path.join(current_dir, 'des_hsc.xlsx')
hsc_des_path = os.path.join(current_dir, 'hsc_des.xlsx')

print("Testing Excel files...")
des_hsc_ok = test_excel_file(des_hsc_path)
hsc_des_ok = test_excel_file(hsc_des_path)

if des_hsc_ok and hsc_des_ok:
    print("\nAll files are valid!")
else:
    print("\nSome files have issues. Please check the errors above.") 