#!/usr/bin/env python3
"""
Portamedic API Test Script
Tests authentication and order submission to Portamedic sandbox.
"""

import requests
import json
import urllib.parse
from datetime import datetime, timedelta

# Portamedic Sandbox Configuration
TOKEN_URL = "https://auth.integratedtestingservices.com:8020/TokenService/connect/token"
ORDER_URL = "https://www.integratedtestingservices.com/clinical/NewCaseSubmit"

# Credentials
CLIENT_ID = "e7dc58ea-9859-4035-97fe-b3a4d23d5278"
CLIENT_SECRET = "!70883Test7g0hd*ohiHOPgf#$"

# Account info for IMPACT study
ACCOUNT_NUMBER = 7236  # Integer per API docs
SERVICE_SET_NAME = "IMPACT"
SERVICE_CODE = "01"
SERVICE_NAME = "BLOOD DRAW"
SERVICE_DESC = "BLOOD CLINICAL"


def test_token_auth():
    """Test various authentication methods."""
    print("=" * 60)
    print("PORTAMEDIC TOKEN SERVICE TEST")
    print("=" * 60)
    print(f"URL: {TOKEN_URL}")
    print(f"Client ID: {CLIENT_ID}")
    print(f"Client Secret: {CLIENT_SECRET[:10]}...")
    
    results = []
    
    # Method 1: Standard form data (no encoding)
    print("\n--- Method 1: Standard form-urlencoded ---")
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        r = requests.post(TOKEN_URL, data=payload, headers=headers, timeout=30)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
        results.append(("Standard form", r.status_code, r.text))
        if r.status_code == 200:
            return r.json().get("access_token")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 2: URL-encoded in body string
    print("\n--- Method 2: Manual URL-encoded body ---")
    encoded_secret = urllib.parse.quote(CLIENT_SECRET, safe='')
    encoded_id = urllib.parse.quote(CLIENT_ID, safe='')
    body = f"grant_type=client_credentials&client_id={encoded_id}&client_secret={encoded_secret}"
    
    try:
        r = requests.post(TOKEN_URL, data=body, headers=headers, timeout=30)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
        results.append(("URL-encoded body", r.status_code, r.text))
        if r.status_code == 200:
            return r.json().get("access_token")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 3: With scope parameter
    print("\n--- Method 3: With scope parameter ---")
    payload_with_scope = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "Clinical.Originator"
    }
    
    try:
        r = requests.post(TOKEN_URL, data=payload_with_scope, headers=headers, timeout=30)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
        results.append(("With scope", r.status_code, r.text))
        if r.status_code == 200:
            return r.json().get("access_token")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 4: Basic Auth header
    print("\n--- Method 4: Basic Auth header ---")
    from requests.auth import HTTPBasicAuth
    payload_basic = {"grant_type": "client_credentials"}
    
    try:
        r = requests.post(TOKEN_URL, data=payload_basic, headers=headers, 
                         auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET), timeout=30)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
        results.append(("Basic Auth", r.status_code, r.text))
        if r.status_code == 200:
            return r.json().get("access_token")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 5: JSON body
    print("\n--- Method 5: JSON body ---")
    json_headers = {"Content-Type": "application/json"}
    json_payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    
    try:
        r = requests.post(TOKEN_URL, json=json_payload, headers=json_headers, timeout=30)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
        results.append(("JSON body", r.status_code, r.text))
        if r.status_code == 200:
            return r.json().get("access_token")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("SUMMARY - All methods failed")
    print("=" * 60)
    for method, status, response in results:
        print(f"  {method}: {status} - {response[:50]}...")
    
    return None


def create_sample_order():
    """Create a sample order payload for testing."""
    # Appointment time - 7 days from now at 10:00 AM
    appt_time = (datetime.now() + timedelta(days=7)).replace(hour=10, minute=0, second=0)
    
    order = {
        "accountNumber": ACCOUNT_NUMBER,
        "serviceSet": {
            "name": SERVICE_SET_NAME,
            "services": [
                {
                    "serviceName": SERVICE_NAME,
                    "serviceCode": SERVICE_CODE,
                    "serviceDesc": SERVICE_DESC,
                    "specialInstruction": "Test order - please ignore"
                }
            ]
        },
        "contactPersonName": "Test Contact",
        "contactPhone": "5551234567",
        "contactEmail": "test@example.com",
        "subject": {
            "subjectType": "PERSON",
            "firstName": "Test",
            "lastName": "Patient",
            "age": 35,
            "addresses": [
                {
                    "addressType": "HOME",
                    "line1": "123 Test Street",
                    "city": "Boston",
                    "stateAbbr": "MA",
                    "zipCode": "02114",
                    "serviceAddress": True
                }
            ],
            "phones": [
                {
                    "phoneType": "MOBILE",
                    "phoneNumber": "5559876543"
                }
            ],
            "emails": [
                {
                    "emailType": "PERSONAL",
                    "address": "testpatient@example.com"
                }
            ]
        },
        "instructions": "Test order - please ignore",
        "appointment": appt_time.strftime("%Y-%m-%d %H:%M:%S"),
        "durationMinutes": 30,
        "refNumber": f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "ExternalGuid": "00000000-0000-0000-0000-000000000000"
    }
    
    return order


def test_order_submission(access_token):
    """Test submitting an order to Portamedic."""
    print("\n" + "=" * 60)
    print("ORDER SUBMISSION TEST")
    print("=" * 60)
    print(f"URL: {ORDER_URL}")
    
    if not access_token:
        print("ERROR: No access token available - cannot test order submission")
        return
    
    order = create_sample_order()
    print(f"\nSample Order:")
    print(json.dumps(order, indent=2, default=str))
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        r = requests.post(ORDER_URL, json=order, headers=headers, timeout=30)
        print(f"\nStatus: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    print("\n" + "#" * 60)
    print("  PORTAMEDIC SANDBOX API TEST")
    print("  Account: 07236 (IMPACT Study)")
    print("#" * 60 + "\n")
    
    # Test authentication
    access_token = test_token_auth()
    
    if access_token:
        print("\n✅ Authentication successful!")
        print(f"Token: {access_token[:50]}...")
        
        # Test order submission
        test_order_submission(access_token)
    else:
        print("\n❌ Authentication failed - all methods returned errors")
        print("\nPossible issues:")
        print("  1. Credentials may be expired or invalid")
        print("  2. Client ID/Secret may need to be re-issued by Portamedic")
        print("  3. Account may not be configured for sandbox access")
        print("\nRecommendation: Contact Portamedic to verify credentials")


if __name__ == "__main__":
    main()

