# 🌫️ Durgapur Air Quality Analytics & Alerting System

> An end-to-end data analytics project analyzing and forecasting air quality 
> in Durgapur, West Bengal — one of India's most industrially polluted cities.

## 🔴 Live Dashboard
👉 [Click here to open the Streamlit App] (coming soon..)

## 🎯 Project Objectives
- Analyze historical AQI trends (2020–2023) for Durgapur
- Identify seasonal patterns and year-on-year deterioration
- Deliver insights via an interactive web dashboard

## 📊 Key Findings
- Durgapur AQI exceeds 300 (Very Poor) on average X% of winter days
- PM10 is the dominant pollutant (r = 0.93 with AQI)
- January–February consistently record the worst air quality
- Monsoon season shows AQI improvement of ~40% vs winter

## 🛠 Tech Stack
`Python` `pandas` `Streamlit` `Plotly` `Open-Meteo API`

## 📁 Project Structure

```text
durgapur-aqi-analytics/
│
├── data/
│   ├── raw/                        # Original downloaded files (never modify)
│   │   ├── city_day.csv
│   │   └── weather_durgapur_raw.csv
│   ├── processed/                  # Cleaned and feature-engineered data
│   │   ├── aqi_cleaned.csv
│   │   └── aqi_features.csv
│   └── external/                   # Supplementary reference data
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   └── 04_feature_engineering.ipynb
│
├── src/
│   └── data_ingestion.py           # API fetch scripts
│
├── dashboard/
│   ├── app.py                      # Main Streamlit app
│   ├── pages/
│   └── assets/
│       └── weather.png
│
├── models/
│
├── reports/
│   └── durgapur_aqi_insights.pdf   # Final summary report
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 How to Run Locally
\`\`\`bash
git clone https://github.com/rahulnag-io/durgapur-aqi-analytics
cd durgapur-aqi-analytics
pip install -r requirements.txt
streamlit run dashboard/app.py
\`\`\`

## 🗃 Data Sources
- [CPCB Daily AQI](https://cpcb.nic.in/) via Kaggle
- [OpenAQ API](https://openaq.org/)
- [Open-Meteo](https://open-meteo.com/) — Historical weather