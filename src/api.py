from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path
import pandas as pd
import json

app = Flask(__name__)

def get_db_path():
    return Path(__file__).parent.parent / 'outputs' / 'production.db'

def get_well_data(api_well_number, year=None):
    db_path = get_db_path()
    if not db_path.exists():
        return None

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    if year:
        # Query for specific well and year
        cursor.execute('''
            SELECT oil, gas, brine 
            FROM production 
            WHERE api_well_number = ? AND year = ?
        ''', (api_well_number, year))
    else:
        # Query for all years for this well
        cursor.execute('''
            SELECT year, oil, gas, brine 
            FROM production 
            WHERE api_well_number = ?
            ORDER BY year
        ''', (api_well_number,))
    
    if year:
        result = cursor.fetchone()
        data = {
            'oil': result[0],
            'gas': result[1],
            'brine': result[2]
        } if result else None
    else:
        results = cursor.fetchall()
        data = [{
            'year': row[0],
            'oil': row[1],
            'gas': row[2],
            'brine': row[3]
        } for row in results] if results else None
    
    conn.close()
    return data

@app.route('/data')
def get_data():
    well = request.args.get('well')
    year = request.args.get('year')
    
    if not well:
        return jsonify({'error': 'Missing well parameter'}), 400
    
    try:
        well = str(int(well))  # Validate numeric input
    except ValueError:
        return jsonify({'error': 'Well number must be numeric'}), 400
    
    # Convert year to int if provided
    try:
        year = int(year) if year else None
    except ValueError:
        return jsonify({'error': 'Year must be numeric'}), 400

    data = get_well_data(well, year)
    
    if data is None:
        return jsonify({'error': 'Well not found'}), 404
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=8080)