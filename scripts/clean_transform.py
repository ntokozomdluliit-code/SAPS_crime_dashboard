#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os

def clean_crime_data():
    project_root = os.getcwd()
    input_path = os.path.join(project_root, 'data/raw/saps_crime_data_raw.csv')
    output_path = os.path.join(project_root, 'data/processed/saps_crime_data_cleaned.csv')
    
    print(f"Loading raw data from: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found!")
        print("Please run generate_crime_data.py first")
        return None
    
    df = pd.read_csv(input_path)
    df['incident_date'] = pd.to_datetime(df['incident_date'])
    
    print(f"Initial shape: {df.shape}")
    
    df['clearance_rate_days'] = df['clearance_rate_days'].fillna(-1)
    df = df.drop_duplicates(subset=['incident_id'])
    
    df['month_name'] = df['incident_date'].dt.strftime('%B')
    df['quarter'] = df['incident_date'].dt.quarter
    df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)
    
    severity_weights = {
        'Murder': 10, 'Rape': 9, 'Kidnapping': 8, 'Carjacking': 7,
        'House robbery': 6, 'Assault GBH': 5
    }
    
    def get_severity(crime):
        for key, weight in severity_weights.items():
            if key in str(crime):
                return weight
        return 3
    
    df['severity_score'] = df['crime_subcategory'].apply(get_severity)
    df['response_priority'] = df['severity_score'] + df['repeat_location'] * 3 + df['gang_related'] * 2
    
    def get_season(month):
        if month in [12, 1, 2]: return 'Summer'
        elif month in [3, 4, 5]: return 'Autumn'
        elif month in [6, 7, 8]: return 'Winter'
        else: return 'Spring'
    
    df['season'] = df['month'].apply(get_season)
    
    # Hot spot detection
    df['lat_rounded'] = df['latitude'].round(3)
    df['lon_rounded'] = df['longitude'].round(3)
    df['grid_cell'] = df['lat_rounded'].astype(str) + ',' + df['lon_rounded'].astype(str)
    cell_counts = df.groupby('grid_cell').size().reset_index(name='incident_count')
    df = df.merge(cell_counts, on='grid_cell', how='left')
    df['hot_spot'] = (df['incident_count'] > df['incident_count'].quantile(0.90)).astype(int)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"✓ Cleaned data saved to: {output_path}")
    print(f"Final shape: {df.shape}")
    print(f"\n📊 Summary:")
    print(f"  Total incidents: {len(df):,}")
    print(f"  Clearance rate: {(df['arrest_made'].sum() / len(df)) * 100:.1f}%")
    print(f"  Gang related: {(df['gang_related'].sum() / len(df)) * 100:.1f}%")
    
    return df

if __name__ == "__main__":
    df = clean_crime_data()
    print("\n✓ Cleaning complete!")
