# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from datetime import datetime

# ----------------------------
# 💠 Basic Page Setup
# ----------------------------
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

# ----------------------------
# 🌟 Title & Hero Section
# ----------------------------
st.markdown("<h1 style='text-align:center; color:gold;'>Swarna Drishti</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:white;'>Your AI-Powered 24KT Gold Price Oracle</h4>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid gold;'>", unsafe_allow_html=True)

# ----------------------------
# 📦 Load Data
# ----------------------------
@st.cache_data
def load_forecast():
    df = pd.read_csv("forecast.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", inplace=True)
    return df

df = load_forecast()

# ----------------------------
# 📈 Latest Metrics
# ----------------------------
latest = df.iloc[-1]
previous = df.iloc[-2]
delta = latest["Trident_Forecast"] - previous["Trident_Forecast"]
percent_change = (delta / previous["Trident_Forecast"]) * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="📅 Latest Forecast Date", value=str(latest["Date"].date()))


with col2:
    st.metric(label="📈 24KT Gold Price (Predicted)", value=f"₹{latest['Trident_Forecast']:,.2f}")

with col3:
    st.metric(
        label="📊 1-Day Change",
        value=f"₹{delta:,.2f}",
        delta=f"{percent_change:.2f}%"
    )

# ----------------------------
# 📈 Forecast Chart (Next 7 Days)
# ----------------------------
st.markdown("### 📈 Next 7 Days Forecast - 24KT Gold (INR per 10g)")
future_df = df[df["Date"] > df["Date"].max() - pd.Timedelta(days=7)]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=future_df["Date"],
    y=future_df["Trident_Forecast"],
    mode="lines+markers",
    name="Forecast",
    line=dict(color="gold", width=2)
))
fig.update_layout(
    title="24KT Gold Price Forecast (Next 7 Days)",
    xaxis_title="Date",
    yaxis_title="Predicted Price (INR)",
    template="plotly_dark"
)
st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# 💡 Investment Suggestion
# ----------------------------
st.markdown("### 💡 Investment Insight")
if future_df["Trident_Forecast"].iloc[-1] > future_df["Trident_Forecast"].iloc[0]:
    st.success("📈 The gold price is on a rising trend — a good time to invest.")
elif future_df["Trident_Forecast"].iloc[-1] < future_df["Trident_Forecast"].iloc[0]:
    st.warning("📉 The gold price is declining — you may wait before investing.")
else:
    st.info("⏸️ The price seems stable — neutral investment window.")

# ----------------------------
# 🔍 Predict Price on Selected Date
# ----------------------------
st.markdown("### 🔍 Predict Gold Price for a Specific Date")
with st.form("predict_form"):
    selected_date = st.date_input("Choose a date to predict", value=df["Date"].max())
    submitted = st.form_submit_button("🔎 Predict Price")

if submitted:
    selected_date = pd.to_datetime(selected_date)
    match = df[df["Date"] == selected_date]
    if not match.empty:
        price = match["Trident_Forecast"].values[0]
        st.success(f"📆 Predicted 24KT Gold Price on {selected_date.date()}: ₹{price:,.2f}")
    else:
        st.error("❌ Forecast not available for this date. Please choose within the forecast range.")

# ----------------------------
# 📋 Table of Last 7 Days Predicted Prices
# ----------------------------
st.markdown("### 📋 Last 7 Days of 24KT Gold Price Predictions")
last_7_days = df.tail(7).copy()
last_7_days["Date"] = last_7_days["Date"].dt.strftime('%Y-%m-%d')
st.dataframe(
    last_7_days.rename(columns={
        "Date": "Date",
        "Trident_Forecast": "Predicted Price (INR)"
    }).set_index("Date"),
    use_container_width=True
)

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>© 2025 Swarna Drishti | Powered by Trident Forecast</p>",
    unsafe_allow_html=True
)
