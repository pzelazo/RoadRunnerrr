# graph.py

import pandas as pd
import plotly.express as px

def generate_graph():
    df = pd.read_csv('results.csv')
    df['StartTime'] = pd.to_datetime(df['StartTime'], format='%Y-%m-%d-%H:%M:%S.%f')
    fig = px.line(df, x='StartTime', y='VusersNumber', title='Number of Users Over Time')
    fig.show()
