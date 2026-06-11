# 🚔 SAPS Attack Pattern Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-2.9+-green.svg)](https://plotly.com/dash/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An **interactive analytics dashboard** for the South African Police Service to identify crime attack patterns, optimize resource deployment, and track clearance rates.

## 🎯 Problem Statement

SAPS faces critical challenges:
- **Manual docket review** taking 3-5 days to identify patterns
- **Delayed response** to emerging Modus Operandi
- **Inefficient resource allocation** across 1,100+ precincts

## 💡 Solution

| Feature | Impact |
|---------|--------|
| **Crime Clock** | Identifies peak crime hours per precinct |
| **Attack Pattern Matrix** | Tracks emerging Modus Operandi in real-time |
| **Hotspot Mapping** | Geographic crime clustering with 500m precision |
| **Performance Metrics** | Clearance rates and response priority scoring |

## ✨ Key Features

- 🔄 **Real-time filtering** by province, crime category, and year
- 📈 **Interactive visualizations** with Plotly
- 🗺️ **Geographic heatmaps** with 90th percentile hotspot detection
- 📊 **Attack pattern tracking** with severity scoring (1-10 scale)
- 🎯 **Response priority scoring** combining severity + repeat offenses + gang involvement

## 🚀 Quick Start

```bash
# Clone and run
git clone https://github.com/yourusername/saps-crime-dashboard.git
cd saps-crime-dashboard
chmod +x run_project.sh
./run_project.sh
