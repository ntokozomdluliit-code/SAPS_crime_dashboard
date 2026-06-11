import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import os

project_root = "/home/raizel/saps_crime_dashboard"
df_path = os.path.join(project_root, 'data/processed/saps_crime_data_cleaned.csv')

print("Loading data...")
df = pd.read_csv(df_path)
df['incident_date'] = pd.to_datetime(df['incident_date'])
print(f"Loaded {len(df)} records")

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "SAPS Crime Analytics Dashboard"

app.layout = dbc.Container([
    dbc.Row([dbc.Col(html.H1("SAPS Attack Pattern Analytics Dashboard", className="text-center text-danger mb-4"), width=12)]),
    dbc.Row([
        dbc.Col([html.Label("Province:"), dcc.Dropdown(id='province_filter', options=[{'label': 'All', 'value': 'All'}] + [{'label': p, 'value': p} for p in sorted(df['province'].unique())], value='All')], width=3),
        dbc.Col([html.Label("Crime Category:"), dcc.Dropdown(id='crime_filter', options=[{'label': 'All', 'value': 'All'}] + [{'label': c, 'value': c} for c in sorted(df['crime_category'].unique())], value='All')], width=3),
        dbc.Col([html.Label("Year:"), dcc.RangeSlider(id='year_slider', min=df['year'].min(), max=df['year'].max(), value=[df['year'].min(), df['year'].max()], marks={y: str(y) for y in range(df['year'].min(), df['year'].max()+1)})], width=6)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Total Incidents"), html.H2(id='total_incidents', className="text-danger")])), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Clearance Rate"), html.H2(id='clearance_rate', className="text-success")])), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Gang Related"), html.H2(id='gang_percent', className="text-warning")])), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Peak Hour"), html.H2(id='peak_hour', className="text-info")])), width=3)
    ], className="mb-4"),
    dbc.Row([dbc.Col(dcc.Graph(id='crime_clock'), width=6), dbc.Col(dcc.Graph(id='attack_patterns'), width=6)]),
    dbc.Row([dbc.Col(dcc.Graph(id='hotspot_map'), width=12)], className="mt-4"),
], fluid=True)

@app.callback(
    [Output('total_incidents', 'children'), Output('clearance_rate', 'children'), 
     Output('gang_percent', 'children'), Output('peak_hour', 'children'),
     Output('crime_clock', 'figure'), Output('attack_patterns', 'figure'), Output('hotspot_map', 'figure')],
    [Input('province_filter', 'value'), Input('crime_filter', 'value'), Input('year_slider', 'value')]
)
def update(province, crime_category, year_range):
    filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    if province != 'All': filtered = filtered[filtered['province'] == province]
    if crime_category != 'All': filtered = filtered[filtered['crime_category'] == crime_category]
    
    total = len(filtered)
    clearance = (filtered['arrest_made'].sum() / total * 100) if total > 0 else 0
    gang = (filtered['gang_related'].sum() / total * 100) if total > 0 else 0
    peak = filtered.groupby('hour').size().idxmax() if total > 0 else 0
    
    hourly = filtered.groupby('hour').size()
    clock = go.Figure(data=go.Bar(x=hourly.index, y=hourly.values, marker_color='darkred'))
    clock.update_layout(title='Crime by Hour', template='plotly_dark', height=400)
    
    patterns = filtered['attack_pattern'].value_counts().head(10)
    pat_fig = go.Figure(data=go.Bar(y=patterns.index, x=patterns.values, orientation='h', marker_color='crimson'))
    pat_fig.update_layout(title='Top Attack Patterns', template='plotly_dark', height=400)
    
    sample = filtered.sample(min(2000, len(filtered)))
    map_fig = px.scatter_mapbox(sample, lat='latitude', lon='longitude', color='crime_category', zoom=5, center={'lat': -29, 'lon': 24})
    map_fig.update_layout(mapbox_style='carto-darkmatter', height=500)
    
    return f"{total:,}", f"{clearance:.1f}%", f"{gang:.1f}%", f"{peak}:00", clock, pat_fig, map_fig

if __name__ == '__main__':
    print("\nStarting dashboard at http://localhost:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)
