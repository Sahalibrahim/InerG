import pandas as pd
import sqlite3
import os
from pathlib import Path

def process_data():
    # Define paths
    data_dir = Path(__file__).parent.parent / 'data'
    output_dir = Path(__file__).parent.parent / 'outputs'
    
    # Looking for the specific ET.Xls.6 file
    excel_file = data_dir / 'ohio_production_2020.ET.Xls.6'
    db_file = output_dir / 'production.db'

    # Create directories if needed
    data_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    # Load the Excel file - using engine='xlrd' for .ET.Xls.6 files
    try:
        df = pd.read_excel(excel_file, engine='xlrd')
        print(f"Successfully loaded data from {excel_file}")
    except FileNotFoundError:
        available_files = "\n".join([f.name for f in data_dir.glob('*')])
        raise FileNotFoundError(
            f"Excel file not found at {excel_file}\n"
            f"Available files in data directory:\n{available_files}"
        )
    except Exception as e:
        raise Exception(f"Error reading Excel file: {str(e)}\n"
                      "You may need to install xlrd: pip install xlrd")

    # Process data
    annual_data = df.groupby('API WELL  NUMBER').agg({
        'OIL': 'sum',
        'GAS': 'sum',
        'BRINE': 'sum'
    }).reset_index()

    annual_data.columns = ['api_well_number', 'oil', 'gas', 'brine']

    # Save to SQLite
    if db_file.exists():
        db_file.unlink()

    conn = sqlite3.connect(db_file)
    annual_data.to_sql('production', conn, index=False, if_exists='replace')
    conn.close()

    print(f"Database created at {db_file}")
    return annual_data

if __name__ == '__main__':
    process_data()