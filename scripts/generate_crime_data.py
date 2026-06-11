#!/usr/bin/env python3
import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def generate_crime_dataset(num_records=50000):
    # Get the project root directory (where the script is called from)
    project_root = os.getcwd()
    output_path = os.path.join(project_root, 'data/raw/saps_crime_data_raw.csv')
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Generating {num_records} crime records...")
    print(f"Saving to: {output_path}")
    
    np.random.seed(42)
    random.seed(42)
    
    # Define geographic regions
    provinces = {
        'Gauteng': {'lat_range': (-26.5, -25.5), 'lon_range': (27.5, 28.5), 'weight': 0.35},
        'Western Cape': {'lat_range': (-34.2, -33.7), 'lon_range': (18.2, 18.8), 'weight': 0.20},
        'KwaZulu-Natal': {'lat_range': (-30.0, -29.5), 'lon_range': (30.5, 31.5), 'weight': 0.15},
        'Eastern Cape': {'lat_range': (-33.5, -32.5), 'lon_range': (25.5, 27.5), 'weight': 0.10},
        'Mpumalanga': {'lat_range': (-26.0, -25.0), 'lon_range': (29.0, 31.0), 'weight': 0.07},
        'North West': {'lat_range': (-27.5, -25.5), 'lon_range': (25.0, 27.0), 'weight': 0.05},
        'Free State': {'lat_range': (-29.0, -27.5), 'lon_range': (25.0, 27.5), 'weight': 0.04},
        'Limpopo': {'lat_range': (-24.0, -22.5), 'lon_range': (29.0, 31.0), 'weight': 0.03},
        'Northern Cape': {'lat_range': (-29.0, -27.0), 'lon_range': (20.0, 24.0), 'weight': 0.01}
    }
    
    precincts = {
        'Gauteng': ['Jeppe', 'Hillbrow', 'Soweto', 'Pretoria Central', 'Sandton', 'Roodepoort'],
        'Western Cape': ['Cape Town Central', 'Mitchells Plain', 'Khayelitsha', 'Nyanga', 'Bellville'],
        'KwaZulu-Natal': ['Durban Central', 'Inanda', 'Phoenix', 'Pietermaritzburg', 'Chatsworth'],
        'Eastern Cape': ['Port Elizabeth', 'East London', 'Mdantsane', 'Motherwell', 'Gqeberha'],
        'Mpumalanga': ['Nelspruit', 'Witbank', 'Secunda', 'Middelburg', 'Ermelo'],
        'North West': ['Rustenburg', 'Mahikeng', 'Klerksdorp', 'Brits', 'Potchefstroom'],
        'Free State': ['Bloemfontein', 'Welkom', 'Sasolburg', 'Bethlehem', 'Kroonstad'],
        'Limpopo': ['Polokwane', 'Thohoyandou', 'Modimolle', 'Lebowakgomo', 'Giyani'],
        'Northern Cape': ['Kimberley', 'Upington', 'Springbok', 'De Aar', 'Kuruman']
    }
    
    crime_hierarchy = {
        'Robbery': ['House robbery', 'Business robbery', 'Street robbery', 'Carjacking'],
        'Property Crime': ['Housebreaking', 'Theft out of motor vehicle', 'Theft of motor vehicle'],
        'Violent Crime': ['Murder', 'Attempted murder', 'Assault GBH', 'Kidnapping'],
        'Sexual Offenses': ['Rape', 'Sexual assault'],
        'Contact Crime': ['Common assault', 'Robbery with firearm']
    }
    
    attack_patterns = {
        'Carjacking': ['Hijacking - fake accident', 'Hijacking - driveway', 'Hijacking - traffic light'],
        'House robbery': ['Home invasion - night', 'Home invasion - day', 'Home invasion - banking app'],
        'Kidnapping': ['Kidnapping - extortion', 'Kidnapping - ATM forced', 'Kidnapping - banking transfer'],
        'Murder': ['Domestic violence', 'Gang-related shooting', 'Taxi violence', 'Argument escalation']
    }
    
    weapons = ['Firearm', 'Knife', 'Blunt object', 'No weapon', 'Other']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = (end_date - start_date).days
    
    data = []
    for i in range(num_records):
        if i % 10000 == 0:
            print(f"  Generated {i}/{num_records} records...")
        
        province = random.choices(list(provinces.keys()), 
                                 weights=[p['weight'] for p in provinces.values()])[0]
        bounds = provinces[province]
        lat = np.random.uniform(bounds['lat_range'][0], bounds['lat_range'][1])
        lon = np.random.uniform(bounds['lon_range'][0], bounds['lon_range'][1])
        precinct = random.choice(precincts.get(province, ['General']))
        crime_cat = random.choice(list(crime_hierarchy.keys()))
        crime_sub = random.choice(crime_hierarchy[crime_cat])
        
        if crime_sub in attack_patterns:
            attack_pattern = random.choice(attack_patterns[crime_sub])
        else:
            attack_pattern = f"Standard {crime_sub}"
        
        hour_weights = [1,1,1,1,2,3,4,5,6,7,8,9,10,9,8,10,12,15,18,22,25,20,15,10]
        hour = random.choices(range(24), weights=hour_weights)[0]
        minute = random.randint(0, 59)
        incident_time = f"{hour:02d}:{minute:02d}:00"
        
        random_days = random.randint(0, date_range)
        incident_date = start_date + timedelta(days=random_days)
        
        weapon = random.choice(weapons)
        
        if random.random() < 0.3:
            suspect_count = random.randint(2, 8)
            gang_related = 1
        else:
            suspect_count = random.randint(1, 3)
            gang_related = 0
        
        victim_age = random.randint(18, 70)
        victim_gender = random.choice(['M', 'F'])
        property_lost = round(random.uniform(0, 100000) if random.random() < 0.6 else 0, 2)
        property_recovered = round(property_lost * random.uniform(0, 0.3), 2) if property_lost > 0 else 0
        
        arrest_prob = {'Robbery': 0.35, 'Property Crime': 0.15, 'Violent Crime': 0.40, 
                      'Sexual Offenses': 0.45, 'Contact Crime': 0.38}
        arrest_made = 1 if random.random() < arrest_prob.get(crime_cat, 0.3) else 0
        clearance_rate_days = round(random.uniform(1, 90), 1) if arrest_made else None
        
        repeat_location = 1 if random.random() < 0.2 else 0
        
        data.append({
            'incident_id': f"SAPS-{incident_date.year}-{i:06d}",
            'incident_date': incident_date.strftime('%Y-%m-%d'),
            'incident_time': incident_time,
            'hour': hour,
            'day_of_week': days[incident_date.weekday()],
            'month': incident_date.month,
            'year': incident_date.year,
            'province': province,
            'precinct': precinct,
            'latitude': lat,
            'longitude': lon,
            'crime_category': crime_cat,
            'crime_subcategory': crime_sub,
            'attack_pattern': attack_pattern,
            'weapon_used': weapon,
            'suspect_count': suspect_count,
            'victim_age': victim_age,
            'victim_gender': victim_gender,
            'property_lost': property_lost,
            'property_recovered': property_recovered,
            'arrest_made': arrest_made,
            'clearance_rate_days': clearance_rate_days,
            'gang_related': gang_related,
            'repeat_location': repeat_location
        })
    
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"\n✓ Successfully generated {len(df)} records")
    print(f"✓ Saved to: {output_path}")
    print(f"\nFirst 5 records:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    df = generate_crime_dataset(50000)
