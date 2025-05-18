import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from datetime import datetime

st.set_page_config(page_title="Swarna Drishti", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #111111;
        color: #f5f5f5;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .metric-container {
        background-color: #202020;
        padding: 1.2rem;
        border-radius: 0.8rem;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center; color:gold;'>Swarna Drishti</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:white;'>Your AI-Powered 24KT Gold Price Oracle</h4>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid gold;'>", unsafe_allow_html=True)

@st.cache_data
def load_forecast():
    df = pd.read_csv("forecast.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", inplace=True)
    return df

df = load_forecast()

if df.empty:
    st.error("❌ No forecast data available. Please check your forecast.csv file.")
    st.stop()

latest = df.iloc[-1]
if len(df) > 1:
    previous = df.iloc[-2]
    delta = latest["Trident_Forecast"] - previous["Trident_Forecast"]
    percent_change = (delta / previous["Trident_Forecast"]) * 100
else:
    delta = 0
    percent_change = 0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="📅 Latest Forecast Date", value="2025-06-15")

with col2:
    st.metric(label="📈 24KT Gold Price (Predicted)", value=f"₹{latest['Trident_Forecast']:,.2f}")

with col3:
    st.metric(
        label="📊 1-Day Change",
        value=f"₹{delta:,.2f}",
        delta=f"{percent_change:.2f}%"
    )

st.markdown("### 📈 Gold Price Forecast - 24KT Gold (INR per 10g)")

future_df = df.head(7)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=future_df["Date"],
    y=future_df["Trident_Forecast"],
    mode="lines+markers",
    name="Forecast",
    line=dict(color="gold", width=2),
    marker=dict(size=8)
))
fig.update_layout(
    title="24KT Gold Price Forecast",
    xaxis_title="Date",
    yaxis_title="Predicted Price (INR)",
    template="plotly_dark",
    showlegend=True
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 💡 Investment Insight")
if len(future_df) > 1:
    if future_df["Trident_Forecast"].iloc[-1] > future_df["Trident_Forecast"].iloc[0]:
        st.success("📈 The gold price is on a rising trend — a good time to invest.")
    elif future_df["Trident_Forecast"].iloc[-1] < future_df["Trident_Forecast"].iloc[0]:
        st.warning("📉 The gold price is declining — you may wait before investing.")
    else:
        st.info("⏸️ The price seems stable — neutral investment window.")
else:
    st.info("⏸️ Not enough data for trend analysis.")

st.markdown("### 🔍 Predict Gold Price for a Specific Date")
with st.form("predict_form"):
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    default_date = pd.to_datetime("2025-06-15").date()
    
    selected_date = st.date_input(
        "Choose a date to predict", 
        value=default_date,
        min_value=min_date,
        max_value=max_date
    )
    submitted = st.form_submit_button("🔎 Predict Price")

if submitted:
    selected_date = pd.to_datetime(selected_date)
    match = df[df["Date"] == selected_date]
    if not match.empty:
        price = match["Trident_Forecast"].values[0]
        st.success(f"📆 Predicted 24KT Gold Price on {selected_date.date()}: ₹{price:,.2f}")
    else:
        st.error("❌ Forecast not available for this date. Please choose within the forecast range.")

st.markdown("### 📋 24KT Gold Price Predictions")
display_df = df.head(10).copy()
display_df["Date"] = display_df["Date"].dt.strftime('%Y-%m-%d')
st.dataframe(
    display_df.rename(columns={
        "Date": "Date",
        "Trident_Forecast": "Predicted Price (INR)"
    }).set_index("Date"),
    use_container_width=True
)

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>© 2025 Swarna Drishti | Powered by Trident Forecast</p>",
    unsafe_allow_html=True
)