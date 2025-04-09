# inerG: Ohio Oil/Gas Production API

A Flask API to fetch annual production data (oil, gas, brine) for Ohio wells.

## Features
- Processes Ohio DNR quarterly data into annual sums.
- SQLite database storage.
- REST API with `/data` endpoint.

## Usage
1. Install dependencies:
   ```bash
   pip install flask pandas xlrd sqlite3