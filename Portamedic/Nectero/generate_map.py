#!/usr/bin/env python3
"""
Generate a US map visualization of Nectero sites with coverage data.
Includes all locations even if same city with different zip codes.
"""

import plotly.graph_objects as go
import pandas as pd
import json
import numpy as np

# All 38 site locations (including duplicates with different zips)
sites = [
    {"city": "Boston", "state": "MA", "zip": "02114", "lat": 42.3601, "lon": -71.0589},
    {"city": "Stony Brook", "state": "NY", "zip": "11794", "lat": 40.9257, "lon": -73.1409},
    {"city": "Scottsdale", "state": "AZ", "zip": "85260", "lat": 33.4942, "lon": -111.9261},
    {"city": "Columbus", "state": "OH", "zip": "43210", "lat": 39.9612, "lon": -82.9988},
    {"city": "Seattle", "state": "WA", "zip": "98104", "lat": 47.6062, "lon": -122.3321},
    {"city": "Philadelphia", "state": "PA", "zip": "19107", "lat": 39.9526, "lon": -75.1652},
    {"city": "Washington", "state": "DC", "zip": "20010", "lat": 38.9072, "lon": -77.0369},
    {"city": "Plano", "state": "TX", "zip": "75093", "lat": 33.0198, "lon": -96.6989},
    {"city": "Greenville", "state": "SC", "zip": "29615", "lat": 34.8526, "lon": -82.3940},
    {"city": "Augusta", "state": "GA", "zip": "30912", "lat": 33.4735, "lon": -82.0105},
    {"city": "Houston", "state": "TX", "zip": "77004", "lat": 29.7604, "lon": -95.3698},
    {"city": "Salt Lake City", "state": "UT", "zip": "84132", "lat": 40.7608, "lon": -111.8910},
    {"city": "St. Louis", "state": "MO", "zip": "63110", "lat": 38.6270, "lon": -90.1994},
    {"city": "Philadelphia", "state": "PA", "zip": "19104", "lat": 39.9496, "lon": -75.1952},  # Slightly offset
    {"city": "Pittsburgh", "state": "PA", "zip": "15219", "lat": 40.4406, "lon": -79.9959},
    {"city": "Allentown", "state": "PA", "zip": "18102", "lat": 40.6084, "lon": -75.4902},
    {"city": "Portland", "state": "OR", "zip": "97239", "lat": 45.5152, "lon": -122.6784},
    {"city": "Worcester", "state": "MA", "zip": "01655", "lat": 42.2626, "lon": -71.8023},
    {"city": "Cleveland", "state": "OH", "zip": "44106", "lat": 41.4993, "lon": -81.6944},
    {"city": "Fairfax", "state": "VA", "zip": "22031", "lat": 38.8462, "lon": -77.3064},
    {"city": "Green Bay", "state": "WI", "zip": "54301", "lat": 44.5133, "lon": -88.0133},
    {"city": "Royal Oak", "state": "MI", "zip": "48073", "lat": 42.4895, "lon": -83.1446},
    {"city": "Omaha", "state": "NE", "zip": "68198", "lat": 41.2565, "lon": -95.9345},
    {"city": "Portland", "state": "OR", "zip": "97239", "lat": 45.5152, "lon": -122.6784},  # Duplicate - same zip
    {"city": "Delray Beach", "state": "FL", "zip": "33446", "lat": 26.4615, "lon": -80.0728},
    {"city": "Columbus", "state": "OH", "zip": "43214", "lat": 39.9812, "lon": -83.0188},  # Slightly offset
    {"city": "Nashville", "state": "TN", "zip": "37232", "lat": 36.1627, "lon": -86.7816},
    {"city": "Cleveland", "state": "OH", "zip": "44195", "lat": 41.5093, "lon": -81.6144},  # Slightly offset
    {"city": "Aurora", "state": "CO", "zip": "80045", "lat": 39.7294, "lon": -104.8319},
    {"city": "Boston", "state": "MA", "zip": "02215", "lat": 42.3471, "lon": -71.1029},  # Slightly offset
    {"city": "Durham", "state": "NC", "zip": "27710", "lat": 35.9940, "lon": -78.8986},
    {"city": "Chicago", "state": "IL", "zip": "60637", "lat": 41.8781, "lon": -87.6298},
    {"city": "Cincinnati", "state": "OH", "zip": "45219", "lat": 39.1031, "lon": -84.5120},
    {"city": "Lebanon", "state": "NH", "zip": "03756", "lat": 43.6423, "lon": -72.2518},
    {"city": "Tulsa", "state": "OK", "zip": "74104", "lat": 36.1540, "lon": -95.9928},
    {"city": "Norfolk", "state": "VA", "zip": "23507", "lat": 36.8508, "lon": -76.2859},
    {"city": "Scarborough", "state": "ME", "zip": "04074", "lat": 43.5781, "lon": -70.3222},
    {"city": "Rochester", "state": "NY", "zip": "14642", "lat": 43.1566, "lon": -77.6088},
]

# Coverage data by zip code (from API results)
coverage_by_zip = {
    "02114": {"mobile": True, "quest_count": 30, "nearest": 2},
    "11794": {"mobile": True, "quest_count": 12, "nearest": 17},
    "85260": {"mobile": True, "quest_count": 30, "nearest": 2},
    "43210": {"mobile": True, "quest_count": 29, "nearest": 1},
    "98104": {"mobile": True, "quest_count": 15, "nearest": 0},
    "19107": {"mobile": True, "quest_count": 21, "nearest": 0},
    "20010": {"mobile": True, "quest_count": 30, "nearest": 2},
    "75093": {"mobile": True, "quest_count": 30, "nearest": 1},
    "29615": {"mobile": False, "quest_count": 2, "nearest": 2},
    "30912": {"mobile": False, "quest_count": 1, "nearest": 10},
    "77004": {"mobile": True, "quest_count": 30, "nearest": 1},
    "84132": {"mobile": True, "quest_count": 3, "nearest": 7},
    "63110": {"mobile": True, "quest_count": 26, "nearest": 1},
    "19104": {"mobile": True, "quest_count": 21, "nearest": 0},  # Philadelphia 2
    "15219": {"mobile": True, "quest_count": 30, "nearest": 1},
    "18102": {"mobile": True, "quest_count": 29, "nearest": 0},
    "97239": {"mobile": True, "quest_count": 10, "nearest": 2},
    "01655": {"mobile": False, "quest_count": 28, "nearest": 1},
    "44106": {"mobile": True, "quest_count": 30, "nearest": 0},
    "22031": {"mobile": True, "quest_count": 30, "nearest": 1},
    "54301": {"mobile": False, "quest_count": 1, "nearest": 6},
    "48073": {"mobile": True, "quest_count": 21, "nearest": 4},
    "68198": {"mobile": False, "quest_count": 2, "nearest": 4},
    "33446": {"mobile": True, "quest_count": 30, "nearest": 3},
    "43214": {"mobile": True, "quest_count": 29, "nearest": 1},  # Columbus 2
    "37232": {"mobile": True, "quest_count": 5, "nearest": 2},
    "44195": {"mobile": True, "quest_count": 30, "nearest": 0},  # Cleveland 2
    "80045": {"mobile": True, "quest_count": 20, "nearest": 4},
    "02215": {"mobile": True, "quest_count": 30, "nearest": 2},  # Boston 2
    "27710": {"mobile": True, "quest_count": 5, "nearest": 15},
    "60637": {"mobile": True, "quest_count": 30, "nearest": 7},
    "45219": {"mobile": True, "quest_count": 7, "nearest": 4},
    "03756": {"mobile": False, "quest_count": 3, "nearest": 21},
    "74104": {"mobile": False, "quest_count": 8, "nearest": 5},
    "23507": {"mobile": True, "quest_count": 8, "nearest": 6},
    "04074": {"mobile": False, "quest_count": 4, "nearest": 4},
    "14642": {"mobile": False, "quest_count": 0, "nearest": None},
}

# Remove exact duplicates (same city + same zip)
seen = set()
unique_sites = []
for site in sites:
    key = f"{site['city']}_{site['state']}_{site['zip']}"
    if key not in seen:
        seen.add(key)
        unique_sites.append(site)

sites = unique_sites

# Create the map figure
fig = go.Figure()

# Separate sites by coverage status
sites_with_mobile = []
sites_without_mobile = []

for site in sites:
    zip_code = site["zip"]
    cov = coverage_by_zip.get(zip_code, {"mobile": False, "quest_count": 0, "nearest": None})
    has_mobile = cov.get("mobile", False)
    quest_count = cov.get("quest_count", 0)
    nearest = cov.get("nearest")
    nearest_str = f"{nearest} mi" if nearest is not None else "N/A"
    
    display_name = f"{site['city']}, {site['state']}"
    full_name = f"{site['city']}, {site['state']} ({zip_code})"
    
    site_info = {
        "name": display_name,
        "full_name": full_name,
        "zip": zip_code,
        "lat": site["lat"],
        "lon": site["lon"],
        "mobile": has_mobile,
        "quest_count": quest_count,
        "nearest": nearest_str,
        "hover": f"<b>{full_name}</b><br>" +
                 f"Mobile Phlebotomy: {'✅ Yes' if has_mobile else '❌ No'}<br>" +
                 f"Quest PSCs (50mi): {quest_count}<br>" +
                 f"Nearest Quest: {nearest_str}"
    }
    
    if has_mobile:
        sites_with_mobile.append(site_info)
    else:
        sites_without_mobile.append(site_info)

# Add coverage radius circles for sites WITH mobile (green)
if sites_with_mobile:
    fig.add_trace(go.Scattergeo(
        lon=[s["lon"] for s in sites_with_mobile],
        lat=[s["lat"] for s in sites_with_mobile],
        mode='markers',
        marker=dict(
            size=70,
            color='rgba(72, 187, 120, 0.25)',
            line=dict(width=2, color='rgba(72, 187, 120, 0.7)')
        ),
        hoverinfo='skip',
        showlegend=False
    ))

# Add coverage radius circles for sites WITHOUT mobile (red)
if sites_without_mobile:
    fig.add_trace(go.Scattergeo(
        lon=[s["lon"] for s in sites_without_mobile],
        lat=[s["lat"] for s in sites_without_mobile],
        mode='markers',
        marker=dict(
            size=70,
            color='rgba(239, 68, 68, 0.25)',
            line=dict(width=2, color='rgba(239, 68, 68, 0.7)')
        ),
        hoverinfo='skip',
        showlegend=False
    ))

# Add solid markers for sites WITH mobile phlebotomy (green)
if sites_with_mobile:
    fig.add_trace(go.Scattergeo(
        lon=[s["lon"] for s in sites_with_mobile],
        lat=[s["lat"] for s in sites_with_mobile],
        text=[s["name"] for s in sites_with_mobile],
        customdata=[s["hover"] for s in sites_with_mobile],
        mode='markers+text',
        marker=dict(
            size=12,
            color='#22c55e',
            symbol='circle',
            line=dict(width=2, color='white')
        ),
        textposition='top center',
        textfont=dict(size=8, color='#166534', family='Arial Black'),
        name='✅ Mobile Phlebotomy Available',
        hovertemplate='%{customdata}<extra></extra>'
    ))

# Add solid markers for sites WITHOUT mobile phlebotomy (red)
if sites_without_mobile:
    fig.add_trace(go.Scattergeo(
        lon=[s["lon"] for s in sites_without_mobile],
        lat=[s["lat"] for s in sites_without_mobile],
        text=[s["name"] for s in sites_without_mobile],
        customdata=[s["hover"] for s in sites_without_mobile],
        mode='markers+text',
        marker=dict(
            size=12,
            color='#ef4444',
            symbol='circle',
            line=dict(width=2, color='white')
        ),
        textposition='top center',
        textfont=dict(size=8, color='#991b1b', family='Arial Black'),
        name='❌ Quest Walk-in Only',
        hovertemplate='%{customdata}<extra></extra>'
    ))

# Calculate stats
mobile_count = len(sites_with_mobile)
no_mobile_count = len(sites_without_mobile)
total = mobile_count + no_mobile_count

# Update layout
fig.update_layout(
    title=dict(
        text=f'<b>Nectero Site Coverage Map</b><br>' +
             f'<span style="font-size:14px">{total} sites | ' +
             f'<span style="color:#22c55e">● {mobile_count} Mobile Phlebotomy</span> | ' +
             f'<span style="color:#ef4444">● {no_mobile_count} Quest Walk-in Only</span></span>',
        x=0.5,
        font=dict(size=20, color='#1e293b')
    ),
    geo=dict(
        scope='usa',
        projection_type='albers usa',
        showland=True,
        landcolor='#f8fafc',
        showlakes=True,
        lakecolor='#e0f2fe',
        subunitcolor='#cbd5e1',
        subunitwidth=1,
        countrycolor='#94a3b8',
        countrywidth=2,
        bgcolor='white',
        showsubunits=True
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=20, r=20, t=80, b=60),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.08,
        xanchor="center",
        x=0.5,
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#e2e8f0",
        borderwidth=1,
        font=dict(size=12)
    )
)

# Save to HTML
fig.write_html('nectero_sites_map.html')
print("Map saved to: nectero_sites_map.html")

# Summary
print("\n" + "=" * 50)
print("COVERAGE SUMMARY")
print("=" * 50)
print(f"Total sites: {total}")
print(f"Mobile Phlebotomy Available: {mobile_count} ({mobile_count/total*100:.0f}%)")
print(f"Quest Walk-in Only: {no_mobile_count} ({no_mobile_count/total*100:.0f}%)")
print("\nSites WITHOUT mobile phlebotomy:")
for s in sites_without_mobile:
    print(f"  ❌ {s['full_name']} - Quest PSCs: {s['quest_count']}, Nearest: {s['nearest']}")
