"""
Test script to verify Orthanc connection
"""
import requests
import json

def test_orthanc():
    orthanc_url = "http://localhost:8042"
    
    try:
        # Test connection
        response = requests.get(f"{orthanc_url}/system")
        if response.status_code == 200:
            print("✅ Orthanc is running!")
            print(f"📍 Orthanc URL: {orthanc_url}")
        else:
            print("❌ Cannot connect to Orthanc")
            return False
        
        # Check studies
        studies_response = requests.get(f"{orthanc_url}/studies")
        studies = studies_response.json()
        print(f"📊 Current studies in Orthanc: {len(studies)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Orthanc: {e}")
        return False

if __name__ == "__main__":
    test_orthanc()
