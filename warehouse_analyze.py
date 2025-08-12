import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

# Generate synthetic warehouse usage data
def generate_synthetic_data(minutes=1440):
    timestamps = [datetime.now() - timedelta(minutes=i) for i in range(minutes)][::-1]
    cpu_usage = np.random.normal(loc=50, scale=20, size=minutes).clip(0, 100)
    memory_usage = np.random.normal(loc=60, scale=25, size=minutes).clip(0, 100)
    auto_scaling_events = [random.choice([0, 1]) if random.random() < 0.01 else 0 for _ in range(minutes)]
    data = pd.DataFrame({
        'Timestamp': timestamps,
        'CPU_Usage': cpu_usage,
        'Memory_Usage': memory_usage,
        'AutoScalingEvent': auto_scaling_events
    })
    return data

# Analyze warehouse efficiency
def analyze_efficiency(data):
    idle_time = data[data['CPU_Usage'] < 10].shape[0]
    over_provisioned_time = data[data['Memory_Usage'] < 30].shape[0]
    auto_scaling_events = data['AutoScalingEvent'].sum()
    recommendations = []
    if idle_time > 60:
        recommendations.append("Consider reducing active hours or consolidating workloads to minimize idle time.")
    if over_provisioned_time > 60:
        recommendations.append("Review memory allocation and consider right-sizing resources.")
    if auto_scaling_events > 20:
        recommendations.append("Optimize auto-scaling policies to reduce unnecessary scaling events.")
    summary = {
        'Idle Time (minutes)': idle_time,
        'Over-Provisioned Time (minutes)': over_provisioned_time,
        'Auto-Scaling Events': auto_scaling_events,
        'Recommendations': recommendations
    }
    return summary

# Generate data and summary
data = generate_synthetic_data()
summary = analyze_efficiency(data)

# Create dashboard app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Warehouse Efficiency Analyzer"

# Layout
app.layout = dbc.Container([
    html.H1("Warehouse Efficiency Analyzer Dashboard", className="my-4"),
    dbc.Row([
        dbc.Col([
            html.H5("Summary Metrics"),
            html.Ul([
                html.Li(f"Idle Time (minutes): {summary['Idle Time (minutes)']}"),
                html.Li(f"Over-Provisioned Time (minutes): {summary['Over-Provisioned Time (minutes)']}"),
                html.Li(f"Auto-Scaling Events: {summary['Auto-Scaling Events']}")
            ])
        ], width=6),
        dbc.Col([
            html.H5("Recommendations"),
            html.Ul([html.Li(rec) for rec in summary['Recommendations']])
        ], width=6)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=px.line(data, x='Timestamp', y='CPU_Usage', title='CPU Usage Over Time'))
        ], width=6),
        dbc.Col([
            dcc.Graph(figure=px.line(data, x='Timestamp', y='Memory_Usage', title='Memory Usage Over Time'))
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=px.bar(data[data['AutoScalingEvent'] == 1], x='Timestamp', y='AutoScalingEvent',
                                    title='Auto-Scaling Events'))
        ])
    ])
], fluid=True)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)
