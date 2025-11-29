"""
Create demo data for testing - uses test client instead of HTTP requests
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app
import json

def create_demo_data():
    print("Creating demo data...")
    
    with app.test_client() as client:
        # Create hospitals
        hospitals = [
            {"id": "HOS-001", "name": "Central General Hospital", "address": "123 Main St"},
            {"id": "HOS-002", "name": "City Medical Center", "address": "456 Health Ave"},
            {"id": "HOS-003", "name": "Regional Hospital", "address": "789 Care Road"}
        ]
        
        for hospital in hospitals:
            response = client.post('/api/hospitals', json=hospital)
            print(f"Created hospital: {hospital['name']} - {response.status_code}")
        
        # Create patients
        patients = [
            {"national_id": "199012345678901234", "first_name": "John", "last_name": "Doe", "date_of_birth": "1990-05-15", "gender": "M"},
            {"national_id": "198511223344556677", "first_name": "Mary", "last_name": "Smith", "date_of_birth": "1985-11-22", "gender": "F"},
            {"national_id": "197808997766554433", "first_name": "Robert", "last_name": "Johnson", "date_of_birth": "1978-08-09", "gender": "M"}
        ]
        
        patient_ids = []
        for patient in patients:
            response = client.post('/api/patients', json=patient)
            if response.status_code == 201:
                patient_id = response.json['patient_id']
                patient_ids.append(patient_id)
                print(f"Created patient: {patient['first_name']} {patient['last_name']} - {patient_id}")
        
        # Create studies
        studies = [
            {"patient_id": patient_ids[0], "study_date": "2024-01-15 10:30:00", "modality": "XR", "description": "Chest X-Ray"},
            {"patient_id": patient_ids[0], "study_date": "2024-01-20 14:15:00", "modality": "CT", "description": "Head CT Scan"},
            {"patient_id": patient_ids[1], "study_date": "2024-01-18 09:45:00", "modality": "US", "description": "Abdominal Ultrasound"},
            {"patient_id": patient_ids[2], "study_date": "2024-01-22 11:20:00", "modality": "XR", "description": "Spine X-Ray"}
        ]
        
        # Distribute studies across hospitals
        hospital_ids = ["HOS-001", "HOS-002", "HOS-003"]
        
        for i, study in enumerate(studies):
            hospital_id = hospital_ids[i % len(hospital_ids)]
            response = client.post(f'/api/hospitals/{hospital_id}/studies', json=study)
            if response.status_code == 201:
                print(f"Created study at {hospital_id}: {study['description']}")
        
        print("\n✅ Demo data created successfully!")
        print(f"\nTo access the system:")
        print(f"1. Start server: cd backend && python app.py")
        print(f"2. Visit dashboard: http://localhost:5000/dashboard")
        print(f"3. Test federation: http://localhost:5000/federation-access?national_id=199012345678901234")
        print(f"4. Patient records: http://localhost:5000/patient-access/{patient_ids[0]}")

if __name__ == "__main__":
    create_demo_data()
