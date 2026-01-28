#!/usr/bin/env python3
"""
DEV Endpoint Test Script
Tests connectivity to the DEV Integrations API endpoint.
Also tests Portamedic token service authentication.
"""

import requests
import json
import sys

# Configuration - DEV Environment
DEV_ENDPOINT = "https://ejouyl4cgd.execute-api.us-east-1.amazonaws.com/event"

# Portamedic OAuth Credentials (for token service)
TOKEN_URL = "https://auth.integratedtestingservices.com:8020/TokenService/connect/token"
CLIENT_ID = "e7dc58ea-9859-4035-97fe-b3a4d23d5278"
CLIENT_SECRET = "!70883Test7g0hd*ohiHOPgf#$"
USERNAME = "Curebase"
PASSWORD = "TESTcureb20231213#"


def test_dev_endpoint_direct():
    """Test the DEV endpoint directly without authentication first."""
    print("=" * 60)
    print("TEST 1: Direct Endpoint Connectivity (No Auth)")
    print("=" * 60)
    print(f"DEV Endpoint: {DEV_ENDPOINT}")
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Try POST with empty body (no auth)
        print("\n> Testing POST request (no auth)...")
        response = requests.post(DEV_ENDPOINT, headers=headers, json={}, timeout=30)
        print(f"  Status: {response.status_code}")
        try:
            print(f"  Body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"  Body: {response.text[:500]}" if response.text else "  Body: (empty)")
        
        # Try POST with Basic Auth (username/password)
        print("\n> Testing POST with Basic Auth (username/password)...")
        auth = (USERNAME, PASSWORD)
        sample_event = {
            "event": "test",
            "participantUuid": "test-123",
            "studySlug": "test-study"
        }
        response = requests.post(DEV_ENDPOINT, headers=headers, json=sample_event, auth=auth, timeout=30)
        print(f"  Status: {response.status_code}")
        try:
            print(f"  Body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"  Body: {response.text[:500]}" if response.text else "  Body: (empty)")
        
        # Try POST with x-api-key header
        print("\n> Testing POST with x-api-key header...")
        headers_with_key = {
            "Content-Type": "application/json",
            "x-api-key": CLIENT_SECRET
        }
        response = requests.post(DEV_ENDPOINT, headers=headers_with_key, json=sample_event, timeout=30)
        print(f"  Status: {response.status_code}")
        try:
            print(f"  Body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"  Body: {response.text[:500]}" if response.text else "  Body: (empty)")
        
        # Try POST with Authorization header using password
        print("\n> Testing POST with Bearer token (using password as token)...")
        headers_bearer = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {PASSWORD}"
        }
        response = requests.post(DEV_ENDPOINT, headers=headers_bearer, json=sample_event, timeout=30)
        print(f"  Status: {response.status_code}")
        try:
            print(f"  Body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"  Body: {response.text[:500]}" if response.text else "  Body: (empty)")
            
        return response.status_code
        
    except requests.exceptions.RequestException as e:
        print(f"\n  ERROR: {e}")
        return None


def test_portamedic_token():
    """Test Portamedic token service authentication."""
    print("\n" + "=" * 60)
    print("TEST 2: Portamedic Token Service")
    print("=" * 60)
    print(f"Token URL: {TOKEN_URL}")
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Try client_credentials grant
    print("\n> Testing client_credentials grant...")
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    
    try:
        response = requests.post(TOKEN_URL, data=payload, headers=headers, timeout=30)
        print(f"  Status: {response.status_code}")
        print(f"  Body: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"\n  SUCCESS! Token received.")
            print(f"  Token Type: {token_data.get('token_type')}")
            print(f"  Expires In: {token_data.get('expires_in')} seconds")
            return token_data.get("access_token")
        
        # Try password grant if client_credentials failed
        print("\n> Testing password grant...")
        payload = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "username": USERNAME,
            "password": PASSWORD,
        }
        response = requests.post(TOKEN_URL, data=payload, headers=headers, timeout=30)
        print(f"  Status: {response.status_code}")
        print(f"  Body: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"\n  SUCCESS! Token received.")
            return token_data.get("access_token")
            
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"\n  ERROR: {e}")
        return None


def main():
    """Main entry point for the test script."""
    print("\n" + "#" * 60)
    print("  PORTAMEDIC DEV ENDPOINT TEST")
    print("#" * 60 + "\n")
    
    # Test 1: Direct endpoint connectivity
    endpoint_status = test_dev_endpoint_direct()
    
    # Test 2: Portamedic token service
    token = test_portamedic_token()
    
    # Summary
    print("\n" + "#" * 60)
    print("  TEST SUMMARY")
    print("#" * 60)
    print(f"DEV Endpoint Reachable: {'YES' if endpoint_status else 'NO'}")
    print(f"Portamedic Token: {'SUCCESS' if token else 'FAILED (credentials may be expired)'}")
    print("#" * 60 + "\n")


if __name__ == "__main__":
    main()

