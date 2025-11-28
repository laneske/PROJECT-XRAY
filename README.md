# 🏥 XRay Federation System

Secure medical image sharing and federation system for hospitals across regions using QR codes and centralized patient records.

## 📋 System Overview

The XRay Federation System enables:
- **Hospital Registration**: Register multiple hospital locations
- **Patient Management**: Centralized patient database across hospitals
- **Medical Studies**: Track X-Ray, CT, Ultrasound and other imaging studies
- **Federation Queries**: Retrieve all studies for a patient across hospitals
- **QR Code Integration**: Generate secure QR codes for study/patient access
- **Web Dashboard**: Beautiful interface for managing the system

## 🏗️ Project Structure

```
Xray-Federation/
├── backend/                    # Flask API backend
│   ├── app.py                 # Main application with all routes
│   ├── config.py              # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   └── federation.db          # SQLite database (auto-created)
├── frontend/                   # Web interfaces
│   ├── dashboard.html         # Main admin dashboard
│   └── patient-records.html   # Patient medical access page
├── orthanc-config/            # Orthanc DICOM server config
│   └── orthanc.json          # Orthanc configuration
├── scripts/                    # Utility scripts
│   ├── test_orthanc.py       # Test Orthanc connection
│   └── create_demo_data.py   # Create sample data for testing
├── docs/                       # Documentation
├── deploy.bat                 # Windows deployment script
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Orthanc DICOM server (optional)
- Windows/Linux/macOS

### Installation

#### Option 1: Automatic Deployment (Windows)
```bash
cd C:\Xray-Federation
deploy.bat
```

#### Option 2: Manual Setup
```bash
# Navigate to project directory
cd C:\Users\Bima\Documents\PROJECT XRAY\Xray-Federation

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Starting the System

```bash
# Navigate to backend directory
cd backend

# Run the Flask app
python app.py
```

You should see:
```
🚀 Starting XRay Federation System...
📍 Access at: http://localhost:5000
📍 API Status: http://localhost:5000/api/status
📍 Dashboard: http://localhost:5000/dashboard
 * Running on http://0.0.0.0:5000
```

## 📍 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Web Dashboard | http://localhost:5000/dashboard | Admin interface |
| API Base | http://localhost:5000/api | REST API endpoints |
| Orthanc DICOM | http://localhost:8042 | DICOM image server |
| System Status | http://localhost:5000/api/status | API health check |

## 🔧 API Endpoints

### Hospitals

**Register Hospital**
```bash
POST /api/hospitals
Content-Type: application/json

{
  "id": "HOS-001",
  "name": "General Hospital",
  "address": "123 Medical St",
  "phone": "+255-22-1234567",
  "email": "admin@hospital.org"
}
```

**List Hospitals**
```bash
GET /api/hospitals
```

### Patients

**Register Patient**
```bash
POST /api/patients
Content-Type: application/json

{
  "national_id": "199012345678901234",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-05-15",
  "gender": "M",
  "phone": "+255712345678"
}
```

**List Patients**
```bash
GET /api/patients
```

**Get Patient Details**
```bash
GET /api/patients/PAT-901234
```

### Studies

**Register Study**
```bash
POST /api/hospitals/HOS-001/studies
Content-Type: application/json

{
  "patient_id": "PAT-901234",
  "study_date": "2024-01-15 10:30:00",
  "modality": "XR",
  "description": "Chest X-Ray",
  "orthanc_study_id": "orthanc-id-123"
}
```

**Get Hospital Studies**
```bash
GET /api/hospitals/HOS-001/studies
```

### QR Codes

**Patient QR Code**
```
GET /api/patients/PAT-901234/qr
```
Returns PNG image of QR code linking to patient records

**Study QR Code**
```
GET /api/studies/STU-20240115103000/qr
```
Returns PNG image of QR code linking to specific study

### Federation

**Query Patient Records Across Hospitals**
```bash
# By National ID
GET /api/federation/query?national_id=199012345678901234

# By Patient ID
GET /api/federation/query?patient_id=PAT-901234
```

Response:
```json
{
  "patient": {
    "id": "PAT-901234",
    "name": "John Doe",
    "national_id": "199012345678901234"
  },
  "studies": [
    {
      "study_id": "STU-20240115103000",
      "patient_id": "PAT-901234",
      "hospital_id": "HOS-001",
      "study_date": "2024-01-15 10:30:00",
      "modality": "XR",
      "description": "Chest X-Ray",
      "hospital_name": "General Hospital"
    }
  ],
  "total_studies": 1,
  "hospitals_accessed": 1
}
```

## 📊 Creating Demo Data

To populate the system with sample data:

```bash
# Make sure the API is running first
# In another terminal:
cd scripts
python create_demo_data.py
```

This creates:
- 3 sample hospitals
- 3 sample patients
- 4 sample medical studies

Then visit:
- Dashboard: http://localhost:5000/dashboard
- Federation Access: http://localhost:5000/federation-access?national_id=199012345678901234

## 🔐 Database

The system uses **SQLite** for simplicity. The database is automatically created on first run.

### Database Tables

**hospitals**
- id (TEXT, PRIMARY KEY)
- name (TEXT)
- address (TEXT)
- phone (TEXT)
- email (TEXT)
- created_date (TIMESTAMP)

**patients**
- id (TEXT, PRIMARY KEY)
- national_id (TEXT, UNIQUE)
- first_name (TEXT)
- last_name (TEXT)
- date_of_birth (DATE)
- gender (TEXT)
- phone (TEXT)
- created_date (TIMESTAMP)

**studies**
- id (TEXT, PRIMARY KEY)
- patient_id (TEXT, FOREIGN KEY)
- hospital_id (TEXT, FOREIGN KEY)
- study_date (TIMESTAMP)
- modality (TEXT)
- description (TEXT)
- orthanc_study_id (TEXT)
- created_date (TIMESTAMP)

## 🧪 Testing

### Test Orthanc Connection
```bash
cd scripts
python test_orthanc.py
```

### Manual API Testing with curl

Register a hospital:
```bash
curl -X POST http://localhost:5000/api/hospitals \
  -H "Content-Type: application/json" \
  -d '{
    "id": "HOS-001",
    "name": "Demo Hospital",
    "address": "123 Medical Street",
    "phone": "+255-22-1234567"
  }'
```

Register a patient:
```bash
curl -X POST http://localhost:5000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "national_id": "199012345678901234",
    "first_name": "John",
    "last_name": "Doe",
    "gender": "M"
  }'
```

Get QR code:
```bash
curl http://localhost:5000/api/patients/PAT-901234/qr -o patient-qr.png
```

Query federation:
```bash
curl "http://localhost:5000/api/federation/query?national_id=199012345678901234"
```

## 🌐 Web Dashboard Features

### System Status
- Check API server status
- Check Orthanc connection
- View hospital count
- View patient count

### Quick Actions
- Register new patients
- Register hospitals
- View recent studies
- Access Orthanc interface

### Patient Registration
- Collect patient details (name, ID, DOB, etc.)
- Auto-generate patient ID
- Display patient QR code

### Recent Studies
- View latest medical studies across hospitals
- Filter by hospital
- Generate study-specific QR codes

## 🔗 Pages

### Dashboard
- **URL**: http://localhost:5000/dashboard
- **Purpose**: Main admin interface
- **Features**: Patient/hospital registration, system monitoring

### Patient Access
- **URL**: http://localhost:5000/patient-access/{patient_id}
- **Purpose**: View patient's medical records
- **Features**: Display all studies from all hospitals

### Federation Access
- **URL**: http://localhost:5000/federation-access?national_id={id}
- **Purpose**: Search patient records by national ID
- **Features**: Cross-hospital patient lookup

## 🛠️ Configuration

Edit `backend/config.py` to customize:

```python
# Secret key for Flask
SECRET_KEY = 'your-secret-key'

# Database URI
SQLALCHEMY_DATABASE_URI = 'sqlite:///federation.db'

# Orthanc URL
ORTHANC_URL = 'http://localhost:8042'

# Debug mode
DEBUG = True  # Set to False in production
```

## 📦 Dependencies

- **flask** (2.3.3): Web framework
- **flask-cors** (4.0.0): Cross-origin requests
- **qrcode** (7.4.2): QR code generation
- **pillow** (10.0.0): Image processing
- **requests** (2.31.0): HTTP library
- **pydicom** (2.3.1): DICOM file handling

## 🚨 Troubleshooting

### Port Already in Use
```bash
# If port 5000 is already in use:
# Change port in app.py
app.run(port=5001)
```

### CORS Issues
- CORS is already enabled for all origins
- Check browser console for specific errors

### Database Locked
```bash
# Delete the database and restart
rm federation.db
python app.py
```

### Orthanc Connection Failed
- Ensure Orthanc is running on port 8042
- Check Orthanc configuration in `orthanc-config/orthanc.json`

## 📝 Usage Workflow

1. **Register Hospital**
   - Use dashboard or API to register hospital location

2. **Register Patients**
   - Add patients with their national ID and details
   - System generates unique patient ID

3. **Record Studies**
   - Register X-Ray, CT, or other medical studies
   - Associate with patient and hospital
   - Link to Orthanc if using DICOM server

4. **Generate QR Codes**
   - Create QR codes for patient access
   - Create QR codes for specific studies
   - Share via email, print, or display

5. **Query Federation**
   - Look up patient across all hospitals
   - View all their studies
   - Access medical records securely

## 🔄 System Architecture

```
┌─────────────────┐
│  Web Dashboard  │
│   (Frontend)    │
└────────┬────────┘
         │ HTTP
         ↓
┌─────────────────────────────────┐
│   Flask API Backend             │
│  ├─ Hospital Management         │
│  ├─ Patient Management          │
│  ├─ Study Management            │
│  ├─ QR Code Generation          │
│  └─ Federation Queries          │
└────────┬────────────────────────┘
         │
    ┌────┴─────────┐
    ↓              ↓
┌──────────┐  ┌──────────────┐
│ SQLite   │  │ Orthanc      │
│Database  │  │ DICOM Server │
└──────────┘  └──────────────┘
```

## 📄 License

This is a demo/starter system for medical image federation.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API endpoint documentation
3. Check application logs in console

---

**Version**: 1.0  
**Last Updated**: November 2025  
**Status**: Development Ready
