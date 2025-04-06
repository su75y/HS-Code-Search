import pandas as pd
import os

def check_excel_file(file_path):
    print(f"\nChecking file: {file_path}")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    try:
        df = pd.read_excel(file_path)
        print("Columns:", df.columns.tolist())
        print("\nFirst few rows:")
        print(df.head())
        print("\nData types:")
        print(df.dtypes)
    except Exception as e:
        print(f"Error reading file: {str(e)}")

# Check both Excel files
current_dir = os.path.dirname(os.path.abspath(__file__))
des_hsc_path = os.path.join(current_dir, 'des_hsc.xlsx')
hsc_des_path = os.path.join(current_dir, 'hsc_des.xlsx')

check_excel_file(des_hsc_path)
check_excel_file(hsc_des_path) 