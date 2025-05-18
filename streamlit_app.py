import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from datetime import datetime

# ------------------------
# PAGE CONFIGURATION
# ------------------------
st.set_page_config(page_title="Swarna Drishti", layout="wide")
st.markdown("""
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
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:gold;'>Swarna Drishti</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:white;'>Your AI-Powered 24KT Gold Price Oracle</h4>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid gold;'>", unsafe_allow_html=True)

# ------------------------
# LOAD FORECAST DATA
# ------------------------
@st.cache_data
def load_forecast():
    df = pd.read_csv("forecast.csv")  # Should have 'ds', 'yhat', 'yhat_lower', 'yhat_upper'
    df.rename(columns={"ds": "Date", "yhat": "Predicted", "yhat_lower": "Lower_Bound", "yhat_upper": "Upper_Bound"}, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", inplace=True)
    return df

df = load_forecast()

if df.empty:
    st.error("❌ No forecast data available. Please check your forecast.csv file.")
    st.stop()

# ------------------------
# METRICS
# ------------------------
latest = df.iloc[-1]
if len(df) > 1:
    previous = df.iloc[-2]
    delta = latest["Predicted"] - previous["Predicted"]
    percent_change = (delta / previous["Predicted"]) * 100
else:
    delta = 0
    percent_change = 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="📅 Latest Forecast Date", value=latest["Date"].date())
with col2:
    st.metric(label="📈 24KT Gold Price (Predicted)", value=f"₹{latest['Predicted']:,.2f}")
with col3:
    st.metric(label="📊 1-Day Change", value=f"₹{delta:,.2f}", delta=f"{percent_change:.2f}%")

# ------------------------
# FORECAST GRAPH
# ------------------------
st.markdown("### 📈 Gold Price Forecast - 24KT Gold (INR per 10g)")

future_df = df.head(7)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=future_df["Date"],
    y=future_df["Predicted"],
    mode="lines+markers",
    name="Forecast",
    line=dict(color="gold", width=2),
    marker=dict(size=8)
))
fig.add_trace(go.Scatter(
    x=future_df["Date"],
    y=future_df["Upper_Bound"],
    mode="lines",
    name="Upper Bound",
    line=dict(dash='dot', color="lightgreen")
))
fig.add_trace(go.Scatter(
    x=future_df["Date"],
    y=future_df["Lower_Bound"],
    mode="lines",
    name="Lower Bound",
    line=dict(dash='dot', color="red")
))
fig.update_layout(
    title="Next 7 Days Gold Price Forecast (24KT)",
    xaxis_title="Date",
    yaxis_title="Predicted Price (INR)",
    template="plotly_dark",
    showlegend=True
)
st.plotly_chart(fig, use_container_width=True)

# ------------------------
# INVESTMENT SUGGESTION
# ------------------------
st.markdown("### 💡 Investment Insight")
if len(future_df) > 1:
    if future_df["Predicted"].iloc[-1] > future_df["Predicted"].iloc[0]:
        st.success("📈 The gold price is rising — a good time to invest.")
    elif future_df["Predicted"].iloc[-1] < future_df["Predicted"].iloc[0]:
        st.warning("📉 The gold price is falling — you may wait before investing.")
    else:
        st.info("⏸️ The price seems stable — neutral investment window.")
else:
    st.info("⏸️ Not enough data for trend analysis.")

# ------------------------
# PREDICTION FORM
# ------------------------
st.markdown("### 🔍 Predict Gold Price for a Specific Date")
with st.form("predict_form"):
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    default_date = df["Date"].iloc[0].date()
    
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
        price = match["Predicted"].values[0]
        lb = match["Lower_Bound"].values[0]
        ub = match["Upper_Bound"].values[0]
        st.success(f"📆 Predicted 24KT Gold Price on {selected_date.date()}: ₹{price:,.2f}")
        st.info(f"🔺 Confidence Interval: ₹{lb:,.2f} – ₹{ub:,.2f}")
    else:
        st.error("❌ Forecast not available for this date. Please choose within the forecast range.")

# ------------------------
# FORECAST TABLE
# ------------------------
st.markdown("### 📋 24KT Gold Price Forecast Table")
display_df = df.head(10).copy()
display_df["Date"] = display_df["Date"].dt.strftime('%Y-%m-%d')
st.dataframe(
    display_df.rename(columns={
        "Date": "Date",
        "Predicted": "Predicted Price (INR)",
        "Lower_Bound": "Lower Bound",
        "Upper_Bound": "Upper Bound"
    }).set_index("Date"),
    use_container_width=True
)

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>© 2025 Swarna Drishti | Powered by Prophet</p>",
    unsafe_allow_html=True
)
