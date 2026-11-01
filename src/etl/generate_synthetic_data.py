"""
UNICEF SR4S - Synthetic Data Generator & Quality Audit
=======================================================
Simulates offline iRAP audit logging, satellite traffic metrics, 
and generates high-fidelity data for Ahmedabad schools.
Run: python src/etl/generate_synthetic_data.py
"""
import pandas as pd
import numpy as np
from pathlib import Path
import random

np.random.seed(42)
RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

# 1. Schools Dimension (Ahmedabad Focus)
zones = ['Maninagar', 'Satellite', 'Chandkheda', 'Bopal', 'Naranpura', 'Vastrapur']
schools = pd.DataFrame({
    'school_id': range(1, 51),
    'school_name': [f"Govt. Primary School {zone} {i}" for i, zone in enumerate(zones * 8 + zones[:2])],
    'city': 'Ahmedabad',
    'zone': zones * 8 + zones[:2],
    'student_population': np.random.randint(150, 800, 50),
    'latitude': np.random.uniform(229.5, 231.5, 50) / 10, # Approx Ahmedabad coords
    'longitude': np.random.uniform(724.5, 726.5, 50) / 10
})

# 2. iRAP Offline Audit Logs (Simulating mobile app sync delays)
audit_data = []
for sid in schools['school_id']:
    # Simulate offline logging: 30% of audits have a sync delay
    audit_date = pd.to_datetime('2025-12-15') + pd.Timedelta(days=random.randint(0, 30))
    sync_delay_days = random.choice([0, 0, 0, 2, 5]) if random.random() < 0.3 else 0
    sync_date = audit_date + pd.Timedelta(days=sync_delay_days)
    
    # iRAP Star Ratings (1 to 5) and infrastructure scores (0 to 100)
    star_rating = random.choices([1, 2, 3, 4, 5], weights=[0.15, 0.25, 0.30, 0.20, 0.10])[0]
    
    audit_data.append({
        'audit_id': f"AUD-{sid:03d}",
        'school_id': sid,
        'audit_date': audit_date,
        'sync_date': sync_date,
        'sync_status': 'Offline-Delayed' if sync_delay_days > 0 else 'Real-time',
        'auditor_id': f"IRAP-{random.randint(10, 15)}",
        'star_rating': star_rating,
        'sidewalk_score': random.randint(20, 100),
        'crossing_score': random.randint(10, 100),
        'speed_management_score': random.randint(15, 100),
        'student_visibility_score': random.randint(30, 100)
    })

audits = pd.DataFrame(audit_data)

# 3. "Sky Usage" Satellite/Traffic Metrics 
# (Simulating satellite imagery API data used to estimate road risk where ground truth is sparse)
sky_metrics = pd.DataFrame({
    'school_id': schools['school_id'],
    'estimated_avg_daily_traffic': np.random.randint(500, 15000, 50),
    'road_width_meters': np.random.uniform(5.0, 18.0, 50).round(1),
    'distance_to_major_highway_km': np.random.uniform(0.2, 5.0, 50).round(2),
    'satellite_confidence_score': np.random.uniform(0.85, 0.99, 50).round(2)
})

# 4. Countermeasure Cost Table (iRAP Standard Estimates in INR)
countermeasures = pd.DataFrame({
    'countermeasure_id': range(1, 6),
    'measure_name': ['Raised Zebra Crossing', 'Pedestrian Refuge Island', 'School Speed Limit Signage', 'Sidewalk Construction (100m)', 'High-Visibility School Paint'],
    'estimated_cost_inr': [45000, 120000, 15000, 85000, 25000],
    'projected_star_rating_increase': [1.0, 1.5, 0.5, 1.5, 0.5]
})

# Save to CSV
schools.to_csv(RAW / "schools_dim.csv", index=False)
audits.to_csv(RAW / "irap_audit_logs.csv", index=False)
sky_metrics.to_csv(RAW / "sky_satellite_metrics.csv", index=False)
countermeasures.to_csv(RAW / "countermeasure_costs.csv", index=False)

print("✅ Synthetic data generated successfully in data/raw/")
print(f"   - Schools: {len(schools)} records")
print(f"   - Offline/Real-time Audits: {len(audits)} records")
print(f"   - Sky Satellite Metrics: {len(sky_metrics)} records")