# dashboard/app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import numpy as np
from datetime import datetime, timedelta

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Durgapur Air Quality Dashboard",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Load data ─────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("C:/Users/Rahul Nag/projects/self/durgapur-aqi-analytics/data/processed/aqi_features.csv", parse_dates=['Date'])
    return df.sort_values('Date').reset_index(drop=True)

# ml model --
df = load_data()
#ml model --

# ── AQI color helper ──────────────────────────────────────────────
def aqi_color(aqi):
    if aqi <= 50: return "#2ecc71"
    elif aqi <= 100: return "#f1c40f"
    elif aqi <= 200: return "#e67e22"
    elif aqi <= 300: return "#e74c3c"
    elif aqi <= 400: return "#8e44ad"
    else: return "#2c3e50"

def aqi_label(aqi):
    if aqi <= 50: return "Good"
    elif aqi <= 100: return "Satisfactory"
    elif aqi <= 200: return "Moderate"
    elif aqi <= 300: return "Poor"
    elif aqi <= 400: return "Very Poor"
    else: return "Severe"

# ── Sidebar ───────────────────────────────────────────────────────
st.sidebar.image("C:/Users/Rahul Nag/projects/self/durgapur-aqi-analytics/dashboard/assets/weather.png",
                 width=120,
                 caption="Durgapur, West Bengal")
st.sidebar.title("🌫️ Durgapur AQI")
st.sidebar.markdown("---")

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df['Date'].dt.year.min()),
    max_value=int(df['Date'].dt.year.max()),
    value=(2018, 2023)
)

show_pm25 = st.sidebar.checkbox("Show PM2.5 overlay", value=True)
show_rolling = st.sidebar.checkbox("Show 30-day rolling avg", value=True)

# Filter data
mask = (df['Date'].dt.year >= year_range[0]) & (df['Date'].dt.year <= year_range[1])
filtered = df[mask].copy()

# ── Header ────────────────────────────────────────────────────────
st.title("🌫️ Durgapur Air Quality Analytics")
st.markdown("Real-time insights into Durgapur's air pollution — driven by CPCB data")
st.markdown("---")

# ── KPI Metrics Row ───────────────────────────────────────────────
latest = df.iloc[-1]
latest_aqi = int(latest['aqi'])
latest_cat = aqi_label(latest_aqi)
avg_aqi = int(filtered['aqi'].mean())
severe_days = int((filtered['aqi'] > 300).sum())
pct_severe = round(severe_days / len(filtered) * 100, 1)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Latest AQI", f"{latest_aqi}", delta=latest_cat)
with col2:
    st.metric(f"Avg AQI ({year_range[0]}–{year_range[1]})", avg_aqi)
with col3:
    st.metric("Severe Days (AQI>300)", severe_days, delta=f"{pct_severe}% of period")
with col4:
    dominant_pollutant = latest.get('AQI_Bucket', 'PM2.5/PM10')
    st.metric("Primary Driver", str(dominant_pollutant))

# ── Main Chart: AQI Time Series ───────────────────────────────────
st.subheader("📈 AQI Trend Over Time")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=filtered['Date'], y=filtered['aqi'],
    name='Daily AQI', line=dict(color='steelblue', width=1),
    opacity=0.5, fill='tozeroy', fillcolor='rgba(70,130,180,0.1)'
))

if show_rolling:
    rolling = filtered['aqi'].rolling(30, center=True).mean()
    fig.add_trace(go.Scatter(
        x=filtered['Date'], y=rolling,
        name='30-day Avg', line=dict(color='crimson', width=2.5)
    ))

# Add AQI threshold bands
fig.add_hrect(y0=0, y1=100, fillcolor="green", opacity=0.05, line_width=0)
fig.add_hrect(y0=200, y1=300, fillcolor="orange", opacity=0.05, line_width=0)
fig.add_hrect(y0=300, y1=500, fillcolor="red", opacity=0.08, line_width=0)
fig.add_hline(y=300, line_dash="dash", line_color="orange",
              annotation_text="Very Poor Threshold")

fig.update_layout(
    height=400, hovermode='x unified',
    yaxis_title="AQI", xaxis_title="Date",
    legend=dict(orientation="h", yanchor="bottom", y=1.02)
)
st.plotly_chart(fig, use_container_width=True)

# ── Seasonal Pattern ──────────────────────────────────────────────
st.subheader("📅 Seasonal Patterns")

col1, col2 = st.columns(2)

with col1:
    monthly_avg = filtered.groupby(filtered['Date'].dt.month)['aqi'].mean().reset_index()
    monthly_avg['MonthName'] = pd.to_datetime(monthly_avg['Date'], format='%m').dt.strftime('%b')
    
    fig2 = px.bar(monthly_avg, x='MonthName', y='aqi',
                  title="Average AQI by Month",
                  color='aqi', color_continuous_scale='RdYlGn_r')
    fig2.update_layout(height=350)
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    season_avg = filtered.groupby('Season_Code')['aqi'].mean().reset_index()
    season_labels = {0: 'Winter', 1: 'Spring', 2: 'Monsoon', 3: 'Post-Monsoon'}
    season_avg['Season'] = season_avg['Season_Code'].map(season_labels)
    
    fig3 = px.bar(season_avg, x='Season', y='aqi',
                  title="Average AQI by Season",
                  color='aqi', color_continuous_scale='RdYlGn_r')
    fig3.update_layout(height=350)
    st.plotly_chart(fig3, use_container_width=True)

# ── 24-Hour AQI Forecast ──────────────────────────────────────────
st.subheader("🔮 24-Hour AQI Forecast")
st.info("Forecast model coming soon...")

FEATURES = ['AQI_lag1', 'AQI_lag2', 'AQI_lag7',
            'AQI_roll3_mean', 'AQI_roll7_mean', 'AQI_roll7_std',
            'Month', 'DayOfWeek', 'Season_Code', 'IsWeekend']

# try--

# try--

# ── Footer ────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Data sources: CPCB via Kaggle · Open-Meteo · OpenAQ | Built with ❤️ in Durgapur")