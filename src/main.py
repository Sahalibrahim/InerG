from process_data import process_data
from api import app
import sys
from pathlib import Path

def initialize():
    db_path = Path(__file__).parent.parent / 'outputs' / 'production.db'
    
    if not db_path.exists():
        print("Initializing database...")
        try:
            process_data()
            print("Database created successfully")
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    initialize()
    print("Starting API server at http://localhost:8080")
    app.run(host='0.0.0.0', port=8080)