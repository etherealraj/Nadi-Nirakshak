from flask import Flask, request, jsonify, render_template
import sqlite3
import joblib
import numpy as np

app = Flask(__name__)

# Load the pre-trained model (assuming you've already trained and saved it)
model = joblib.load('pollution_model.pkl')

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('water_quality.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS water_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            ph REAL,
            dissolved_oxygen REAL,
            temperature REAL,
            turbidity REAL,
            pollution_risk INTEGER,
            latitude REAL,
            longitude REAL
        )
    ''')      
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS pollution_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Endpoint to receive and store water quality data
@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    ph = data['ph']
    dissolved_oxygen = data['dissolved_oxygen']
    temperature = data['temperature']
    turbidity = data['turbidity']
    latitude = data['latitude']
    longitude = data['longitude']

    # Predict pollution risk
    features = np.array([[ph, dissolved_oxygen, temperature, turbidity]])
    pollution_risk = model.predict(features)[0]

    # Store data in the database
    conn = sqlite3.connect('water_quality.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO water_data (ph, dissolved_oxygen, temperature, turbidity, pollution_risk, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (ph, dissolved_oxygen, temperature, turbidity, pollution_risk, latitude, longitude))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'pollution_risk': int(pollution_risk)}), 200

# Endpoint to retrieve recent pollution hotspots
@app.route('/api/hotspots', methods=['GET'])
def get_hotspots():
    conn = sqlite3.connect('water_quality.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM water_data WHERE pollution_risk = 1 ORDER BY timestamp DESC LIMIT 10
    ''')
    rows = c.fetchall()
    conn.close()
    return jsonify(rows), 200

# Endpoint to retrieve recent pollution reports
@app.route('/api/reports', methods=['GET'])
def get_reports():
    conn = sqlite3.connect('water_quality.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM pollution_reports ORDER BY timestamp DESC LIMIT 10
    ''')
    rows = c.fetchall()
    conn.close()
    return jsonify(rows), 200

# Endpoint to submit a pollution report
@app.route('/api/report', methods=['POST'])
def submit_report():
    data = request.json
    location = data['location']
    description = data['description']

    conn = sqlite3.connect('water_quality.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO pollution_reports (location, description, timestamp)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', (location, description))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

