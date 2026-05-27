"""
Run this AFTER starting the server: uvicorn main:app --reload
Opens a second terminal, run: python test_local.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Health check
print("1. Health check...")
r = requests.get(f"{BASE_URL}/")
print(f"   {r.status_code} → {r.json()}\n")

# 2. Submit test form
print("2. Submitting test form...")
payload = {
    "full_name": "Tanish Test",
    "email_address": "tanish@example.com",
    "organisation_name": "Test Corp",
    "contact_number": "+919999999999",
    "project_type": "Interior Design",
    "location": "Gurugram, Haryana",
    "investment": "10-20 Lakhs",
    "vision": "Modern minimalist office with collaborative zones.",
    "best_time_to_reach": "Morning"
}
r = requests.post(f"{BASE_URL}/api/contact", json=payload)
resp = r.json()
print(f"   {r.status_code} → {json.dumps(resp, indent=2)}\n")

inquiry_id = resp.get("inquiry_id")

# 3. Fetch it back
if inquiry_id:
    print(f"3. Fetching record id={inquiry_id}...")
    r = requests.get(f"{BASE_URL}/api/contacts/{inquiry_id}")
    print(f"   {r.status_code} → {json.dumps(r.json(), indent=2, default=str)}\n")

# 4. List all
print("4. All contacts...")
r = requests.get(f"{BASE_URL}/api/contacts")
print(f"   Total records in DB: {r.json()['count']}")
print("\n✓ All good! DB is wired up correctly." if r.json()['count'] > 0 else "\n✗ Something went wrong.")
