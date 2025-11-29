"""
XRay Federation System - Basic Starter
This is the simplest version to get started
"""
from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import uuid
import qrcode
import io

app = Flask(__name__)
CORS(app)

# Simple SQLite database setup
def init_db():
    conn = sqlite3.connect('federation.db')
    cursor = conn.cursor()
    
    # Create hospitals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hospitals (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            email TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id TEXT PRIMARY KEY,
            national_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth DATE,
            gender TEXT,
            phone TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create studies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS studies (
            id TEXT PRIMARY KEY,
            patient_id TEXT,
            hospital_id TEXT,
            study_date TIMESTAMP,
            modality TEXT,
            description TEXT,
            orthanc_study_id TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (hospital_id) REFERENCES hospitals (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

@app.route('/')
def home():
    return jsonify({
        "message": "XRay Federation System Running!",
        "version": "1.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/status')
def status():
    return jsonify({"status": "running", "database": "connected"})

@app.route('/api/hospitals', methods=['GET', 'POST'])
def hospitals():
    conn = sqlite3.connect('federation.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        cursor.execute('''
            INSERT INTO hospitals (id, name, address, phone, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['id'], data['name'], data.get('address'), data.get('phone'), data.get('email')))
        conn.commit()
        conn.close()
        return jsonify({"message": "Hospital registered successfully"}), 201
    
    else:  # GET request
        cursor.execute('SELECT * FROM hospitals')
        hospitals_data = cursor.fetchall()
        conn.close()
        
        hospital_list = []
        for hospital in hospitals_data:
            hospital_list.append({
                "id": hospital[0],
                "name": hospital[1],
                "address": hospital[2],
                "phone": hospital[3],
                "email": hospital[4],
                "created_date": hospital[5]
            })
        
        return jsonify(hospital_list)

@app.route('/api/patients', methods=['GET', 'POST'])
def patients():
    conn = sqlite3.connect('federation.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        
        # Generate patient ID
        patient_id = f"PAT-{data['national_id'][-6:]}"
        
        cursor.execute('''
            INSERT INTO patients (id, national_id, first_name, last_name, date_of_birth, gender, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (patient_id, data['national_id'], data['first_name'], data['last_name'], 
              data.get('date_of_birth'), data.get('gender'), data.get('phone')))
        
        conn.commit()
        conn.close()
        return jsonify({"message": "Patient registered", "patient_id": patient_id}), 201
    
    else:  # GET request
        cursor.execute('SELECT * FROM patients')
        patients_data = cursor.fetchall()
        conn.close()
        
        patient_list = []
        for patient in patients_data:
            patient_list.append({
                "id": patient[0],
                "national_id": patient[1],
                "first_name": patient[2],
                "last_name": patient[3],
                "date_of_birth": patient[4],
                "gender": patient[5],
                "phone": patient[6]
            })
        
        return jsonify(patient_list)

@app.route('/api/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    conn = sqlite3.connect('federation.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    return jsonify({
        "id": patient[0],
        "national_id": patient[1],
        "first_name": patient[2],
        "last_name": patient[3],
        "date_of_birth": patient[4],
        "gender": patient[5],
        "phone": patient[6]
    })

@app.route('/api/patients/<patient_id>/qr')
def generate_patient_qr(patient_id):
    """Generate QR code for patient record access"""
    try:
        # Create patient access URL
        access_url = f"http://localhost:5000/patient-access/{patient_id}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(access_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes for web response
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return send_file(img_bytes, mimetype='image/png')
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/patient-access/<patient_id>')
def patient_access(patient_id):
    """Patient access page"""
    return open('../frontend/patient-records.html').read()

@app.route('/api/hospitals/<hospital_id>/studies', methods=['GET', 'POST'])
def hospital_studies(hospital_id):
    conn = sqlite3.connect('federation.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        
        # Generate study ID with a short UUID suffix to ensure uniqueness
        study_id = f"STU-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
        
        cursor.execute('''
            INSERT INTO studies (id, patient_id, hospital_id, study_date, modality, description, orthanc_study_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (study_id, data['patient_id'], hospital_id, data.get('study_date'), 
              data.get('modality'), data.get('description'), data.get('orthanc_study_id')))
        
        conn.commit()
        conn.close()
        return jsonify({"message": "Study registered", "study_id": study_id}), 201
    
    else:  # GET request
        cursor.execute('''
            SELECT s.*, p.first_name, p.last_name, p.national_id
            FROM studies s
            JOIN patients p ON s.patient_id = p.id
            WHERE s.hospital_id = ?
        ''', (hospital_id,))
        
        studies = cursor.fetchall()
        conn.close()
        
        study_list = []
        for study in studies:
            study_list.append({
                "id": study[0],
                "patient_id": study[1],
                "hospital_id": study[2],
                "study_date": study[3],
                "modality": study[4],
                "description": study[5],
                "orthanc_study_id": study[6],
                "patient_name": f"{study[8]} {study[9]}",
                "national_id": study[10]
            })
        
        return jsonify(study_list)

@app.route('/api/studies/<study_id>/qr')
def generate_study_qr(study_id):
    """Generate QR code for specific study"""
    try:
        # Create study access URL
        access_url = f"http://localhost:5000/study-access/{study_id}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(access_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return send_file(img_bytes, mimetype='image/png')
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/federation/query')
def federation_query():
    """Query patient studies across all hospitals"""
    conn = sqlite3.connect('federation.db')
    cursor = conn.cursor()
    
    national_id = request.args.get('national_id')
    patient_id = request.args.get('patient_id')
    
    if not national_id and not patient_id:
        return jsonify({"error": "Provide national_id or patient_id"}), 400
    
    query = '''
        SELECT s.*, p.first_name, p.last_name, p.national_id, h.name as hospital_name
        FROM studies s
        JOIN patients p ON s.patient_id = p.id
        JOIN hospitals h ON s.hospital_id = h.id
        WHERE 1=1
    '''
    params = []
    
    if national_id:
        query += ' AND p.national_id = ?'
        params.append(national_id)
    
    if patient_id:
        query += ' AND p.id = ?'
        params.append(patient_id)
    
    cursor.execute(query, params)
    studies = cursor.fetchall()
    conn.close()
    
    study_list = []
    for study in studies:
        study_list.append({
            "study_id": study[0],
            "patient_id": study[1],
            "hospital_id": study[2],
            "study_date": study[3],
            "modality": study[4],
            "description": study[5],
            "orthanc_study_id": study[6],
            "patient_name": f"{study[8]} {study[9]}",
            "national_id": study[10],
            "hospital_name": study[11]
        })
    
    return jsonify({
        "patient": {
            "id": study_list[0]['patient_id'] if study_list else None,
            "name": study_list[0]['patient_name'] if study_list else None,
            "national_id": study_list[0]['national_id'] if study_list else None
        },
        "studies": study_list,
        "total_studies": len(study_list),
        "hospitals_accessed": len(set(s['hospital_id'] for s in study_list))
    })

@app.route('/federation-access')
def federation_access_page():
    """Page for cross-hospital access"""
    national_id = request.args.get('national_id')
    
    html = f"""
    <html>
    <head><title>Federation Access</title></head>
    <body>
        <h1>Cross-Hospital Medical Access</h1>
        <form method="GET">
            <label>National ID: </label>
            <input type="text" name="national_id" value="{national_id or ''}">
            <button type="submit">Search</button>
        </form>
    """
    
    if national_id:
        html += f"""
        <div id="results">
            <h2>Searching for: {national_id}</h2>
            <div id="results-content">Loading...</div>
        </div>
        <script>
            fetch('/api/federation/query?national_id={national_id}')
                .then(r => r.json())
                .then(data => {{
                    const content = document.getElementById('results-content');
                    if (data.studies.length > 0) {{
                        content.innerHTML = `
                            <h3>Patient: ${{data.patient.name}}</h3>
                            <p>Total Studies: ${{data.total_studies}} across ${{data.hospitals_accessed}} hospitals</p>
                            <ul>
                                ${{data.studies.map(study => `
                                    <li>
                                        <strong>${{study.description}}</strong> - 
                                        ${{study.hospital_name}} - 
                                        ${{new Date(study.study_date).toLocaleDateString()}}
                                        <a href="/api/studies/${{study.study_id}}/qr" target="_blank">QR Code</a>
                                    </li>
                                `).join('')}}
                            </ul>
                        `;
                    }} else {{
                        content.innerHTML = '<p>No studies found for this patient.</p>';
                    }}
                }});
        </script>
        """
    
    html += "</body></html>"
    return html

@app.route('/dashboard')
def dashboard():
    try:
        return send_from_directory('../frontend', 'dashboard.html')
    except:
        return "Dashboard file not found", 404

@app.route('/frontend/<path:path>')
def serve_frontend(path):
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    # Initialize database on first run
    if not os.path.exists('federation.db'):
        init_db()
    
    print("🚀 Starting XRay Federation System...")
    print("📍 Access at: http://localhost:5000")
    print("📍 API Status: http://localhost:5000/api/status")
    print("📍 Dashboard: http://localhost:5000/dashboard")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
