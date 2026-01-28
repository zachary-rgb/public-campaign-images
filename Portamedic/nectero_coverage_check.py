#!/usr/bin/env python3
"""
Nectero Coverage Check
Queries the Vital API to check phlebotomy and Quest PSC coverage
for zip codes within 100 miles of each Nectero site.
"""

import requests
import json
import time
from math import radians, cos, sin, asin, sqrt

# Vital API Configuration
VITAL_API_KEY = "pk_us_IZBQd4WTLDH2cLzRnU8CVvqDuEDL05rwQLY8fynMmh0"
PSC_INFO_URL = "https://api.tryvital.io/v3/order/psc/info"
AREA_INFO_URL = "https://api.tryvital.io/v3/order/area/info"

HEADERS = {
    "Accept": "application/json",
    "x-vital-api-key": VITAL_API_KEY
}

# Nectero site locations with coordinates
NECTERO_SITES = {
    "Boston, MA": {"zip": "02114", "lat": 42.3601, "lon": -71.0589},
    "Stony Brook, NY": {"zip": "11794", "lat": 40.9257, "lon": -73.1409},
    "Scottsdale, AZ": {"zip": "85260", "lat": 33.4942, "lon": -111.9261},
    "Columbus, OH": {"zip": "43210", "lat": 39.9612, "lon": -82.9988},
    "Seattle, WA": {"zip": "98104", "lat": 47.6062, "lon": -122.3321},
    "Philadelphia, PA": {"zip": "19107", "lat": 39.9526, "lon": -75.1652},
    "Washington, DC": {"zip": "20010", "lat": 38.9072, "lon": -77.0369},
    "Plano, TX": {"zip": "75093", "lat": 33.0198, "lon": -96.6989},
    "Greenville, SC": {"zip": "29615", "lat": 34.8526, "lon": -82.3940},
    "Augusta, GA": {"zip": "30912", "lat": 33.4735, "lon": -82.0105},
    "Houston, TX": {"zip": "77004", "lat": 29.7604, "lon": -95.3698},
    "Salt Lake City, UT": {"zip": "84132", "lat": 40.7608, "lon": -111.8910},
    "St. Louis, MO": {"zip": "63110", "lat": 38.6270, "lon": -90.1994},
    "Pittsburgh, PA": {"zip": "15219", "lat": 40.4406, "lon": -79.9959},
    "Allentown, PA": {"zip": "18102", "lat": 40.6084, "lon": -75.4902},
    "Portland, OR": {"zip": "97239", "lat": 45.5152, "lon": -122.6784},
    "Worcester, MA": {"zip": "01655", "lat": 42.2626, "lon": -71.8023},
    "Cleveland, OH": {"zip": "44106", "lat": 41.4993, "lon": -81.6944},
    "Fairfax, VA": {"zip": "22031", "lat": 38.8462, "lon": -77.3064},
    "Green Bay, WI": {"zip": "54301", "lat": 44.5133, "lon": -88.0133},
    "Royal Oak, MI": {"zip": "48073", "lat": 42.4895, "lon": -83.1446},
    "Omaha, NE": {"zip": "68198", "lat": 41.2565, "lon": -95.9345},
    "Delray Beach, FL": {"zip": "33446", "lat": 26.4615, "lon": -80.0728},
    "Nashville, TN": {"zip": "37232", "lat": 36.1627, "lon": -86.7816},
    "Aurora, CO": {"zip": "80045", "lat": 39.7294, "lon": -104.8319},
    "Durham, NC": {"zip": "27710", "lat": 35.9940, "lon": -78.8986},
    "Chicago, IL": {"zip": "60637", "lat": 41.8781, "lon": -87.6298},
    "Cincinnati, OH": {"zip": "45219", "lat": 39.1031, "lon": -84.5120},
    "Lebanon, NH": {"zip": "03756", "lat": 43.6423, "lon": -72.2518},
    "Tulsa, OK": {"zip": "74104", "lat": 36.1540, "lon": -95.9928},
    "Norfolk, VA": {"zip": "23507", "lat": 36.8508, "lon": -76.2859},
    "Scarborough, ME": {"zip": "04074", "lat": 43.5781, "lon": -70.3222},
    "Rochester, NY": {"zip": "14642", "lat": 43.1566, "lon": -77.6088},
}


def check_coverage(zip_code):
    """Check phlebotomy and Quest PSC coverage for a zip code."""
    result = {
        "zip": zip_code,
        "mobile_phlebotomy": False,
        "quest_psc_count": 0,
        "nearest_quest_miles": None,
        "error": None
    }
    
    try:
        # Check area info for mobile phlebotomy
        area_response = requests.get(
            AREA_INFO_URL,
            params={"lab": "quest", "radius": 50, "zip_code": zip_code},
            headers=HEADERS,
            timeout=10
        )
        
        if area_response.status_code == 200:
            area_data = area_response.json()
            if area_data.get("phlebotomy", {}).get("is_served"):
                result["mobile_phlebotomy"] = True
        
        # Check PSC info for Quest locations
        psc_response = requests.get(
            PSC_INFO_URL,
            params={"lab_id": 7, "radius": 50, "zip_code": zip_code},
            headers=HEADERS,
            timeout=10
        )
        
        if psc_response.status_code == 200:
            psc_data = psc_response.json()
            centers = psc_data.get("patient_service_centers", [])
            result["quest_psc_count"] = len(centers)
            
            if centers:
                # Find nearest
                distances = [c.get("distance", 999) for c in centers]
                nearest = min(distances)
                result["nearest_quest_miles"] = nearest if nearest < 999 else None
                
    except Exception as e:
        result["error"] = str(e)
    
    return result


def main():
    """Check coverage for all Nectero site zip codes."""
    print("\n" + "=" * 70)
    print("  NECTERO COVERAGE CHECK - Vital API")
    print("=" * 70)
    print(f"\nChecking {len(NECTERO_SITES)} site locations...\n")
    
    results = []
    
    for site_name, site_data in NECTERO_SITES.items():
        zip_code = site_data["zip"]
        print(f"Checking {site_name} (ZIP: {zip_code})...", end=" ")
        
        coverage = check_coverage(zip_code)
        coverage["site"] = site_name
        results.append(coverage)
        
        # Status indicator
        mobile = "✓" if coverage["mobile_phlebotomy"] else "✗"
        quest = coverage["quest_psc_count"]
        nearest = coverage["nearest_quest_miles"]
        nearest_str = f"{nearest:.1f}mi" if nearest is not None else "N/A"
        
        print(f"Mobile: {mobile} | Quest PSCs: {quest} | Nearest: {nearest_str}")
        
        # Rate limiting - be nice to the API
        time.sleep(0.3)
    
    # Summary
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    
    mobile_yes = sum(1 for r in results if r["mobile_phlebotomy"])
    mobile_no = len(results) - mobile_yes
    
    print(f"\nMobile Phlebotomy Available: {mobile_yes}/{len(results)} sites")
    print(f"Mobile Phlebotomy NOT Available: {mobile_no}/{len(results)} sites")
    
    # Sites without mobile phlebotomy
    if mobile_no > 0:
        print("\n⚠️  Sites WITHOUT mobile phlebotomy:")
        for r in results:
            if not r["mobile_phlebotomy"]:
                quest_info = f"Quest PSCs: {r['quest_psc_count']}"
                if r["nearest_quest_miles"]:
                    quest_info += f" (nearest: {r['nearest_quest_miles']:.1f}mi)"
                print(f"   - {r['site']} ({r['zip']}) - {quest_info}")
    
    # Sites with mobile phlebotomy
    print("\n✅ Sites WITH mobile phlebotomy:")
    for r in results:
        if r["mobile_phlebotomy"]:
            print(f"   - {r['site']} ({r['zip']})")
    
    # Save results to JSON
    with open("nectero_coverage_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Also save a text summary
    with open("nectero_coverage_summary.txt", "w") as f:
        f.write("NECTERO COVERAGE CHECK RESULTS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total Sites: {len(results)}\n")
        f.write(f"Mobile Phlebotomy Available: {mobile_yes}\n")
        f.write(f"Mobile Phlebotomy NOT Available: {mobile_no}\n\n")
        
        f.write("DETAILED RESULTS:\n")
        f.write("-" * 50 + "\n")
        for r in results:
            mobile = "YES" if r["mobile_phlebotomy"] else "NO"
            quest = r["quest_psc_count"]
            nearest = f"{r['nearest_quest_miles']:.1f}mi" if r["nearest_quest_miles"] else "N/A"
            f.write(f"{r['site']} ({r['zip']})\n")
            f.write(f"  Mobile Phlebotomy: {mobile}\n")
            f.write(f"  Quest PSCs within 50mi: {quest}\n")
            f.write(f"  Nearest Quest: {nearest}\n\n")
    
    print(f"\nResults saved to:")
    print(f"  - nectero_coverage_results.json")
    print(f"  - nectero_coverage_summary.txt")
    
    return results


if __name__ == "__main__":
    main()

