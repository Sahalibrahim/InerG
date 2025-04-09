from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)

def get_db_path():
    return Path(__file__).parent.parent / 'outputs' / 'production.db'

def get_well_data(api_well_number):
    db_path = get_db_path()
    if not db_path.exists():
        return None

    conn = sqlite3.connect(str(db_path))  # Convert to string for SQLite
    cursor = conn.cursor()
    
    cursor.execute('SELECT oil, gas, brine FROM production WHERE api_well_number = ?', 
                  (api_well_number,))
    
    result = cursor.fetchone()
    conn.close()
    
    return {
        'oil': result[0],
        'gas': result[1],
        'brine': result[2]
    } if result else None

@app.route('/data')
def get_data():
    well = request.args.get('well')
    if not well:
        return jsonify({'error': 'Missing well parameter'}), 400
    
    try:
        well = str(int(well))  # Validate numeric input
    except ValueError:
        return jsonify({'error': 'Well number must be numeric'}), 400
    
    data = get_well_data(well)
    return jsonify(data) if data else jsonify({'error': 'Well not found'}), 404

if __name__ == '__main__':
    app.run(port=8080)