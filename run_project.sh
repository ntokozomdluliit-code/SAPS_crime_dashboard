#!/bin/bash
cd /home/raizel/saps_crime_dashboard
source venv/bin/activate

echo "========================================="
echo "🚔 SAPS Crime Analytics Dashboard"
echo "========================================="

if [ ! -f "data/raw/saps_crime_data_raw.csv" ]; then
    echo "📊 Generating data..."
    python scripts/generate_crime_data.py
fi

if [ ! -f "data/processed/saps_crime_data_cleaned.csv" ]; then
    echo "🧹 Cleaning data..."
    python scripts/clean_transform.py
fi

echo "🎨 Starting dashboard at http://localhost:8050"
cd /home/raizel/saps_crime_dashboard
python dashboard/app.py
