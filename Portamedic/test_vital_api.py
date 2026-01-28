import requests
import json

# Test single API call
url = "https://api.tryvital.io/v3/order/area/info"
params = {"lab": "quest", "radius": 50, "zip_code": "02114"}
headers = {
    "Accept": "application/json",
    "x-vital-api-key": "pk_us_IZBQd4WTLDH2cLzRnU8CVvqDuEDL05rwQLY8fynMmh0"
}

output = []
output.append("Testing Vital API...")
output.append(f"URL: {url}")
output.append(f"ZIP: 02114 (Boston)")

try:
    r = requests.get(url, params=params, headers=headers, timeout=10)
    output.append(f"Status: {r.status_code}")
    output.append(f"Response: {r.text[:500]}")
except Exception as e:
    output.append(f"Error: {e}")

# Write to file
with open("api_test_result.txt", "w") as f:
    f.write("\n".join(output))

print("Done - check api_test_result.txt")

