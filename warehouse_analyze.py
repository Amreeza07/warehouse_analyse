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
    recommendations
