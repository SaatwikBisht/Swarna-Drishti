# SWARNA DRISHTI – AI Gold Price Forecasting App

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from prophet.plot import plot_plotly

# ----------------------
# Set Page Layout First
# ----------------------
st.set_page_config(page_title="Swarna Drishti", layout="wide")

# ----------------------
# Background Styling (Optional)
# ----------------------
st.markdown("""
    <style>
    .reportview-container {
        background: url('https://your-gold-background-image-link.jpg');
        background-size: cover;
        background-position: center;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------
# Title and Subtitle
# ----------------------
st.markdown("<h1 style='color:gold; text-align:center;'>Swarna Drishti</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:gold; text-align:center;'>AI-Powered Gold Price Oracle</h3>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align:center; color: white;">
        <p style="font-size:16px;">
            Welcome to Swarna Drishti! Get your AI-powered gold price predictions and investment tips.
        </p>
    </div>
""", unsafe_allow_html=True)

# ----------------------
# Load Forecast Data
# ----------------------
@st.cache_data
def load_forecast():
    forecast = pd.read_csv("forecast.csv")
    forecast["ds"] = pd.to_datetime(forecast["ds"])
    return forecast

forecast = load_forecast()

# Debug Info (can remove later)
st.write("Last date in forecast:", forecast['ds'].max())
st.write("Number of forecasted days:", len(forecast))

# ----------------------
# Overview Dashboard
# ----------------------
col1, col2, col3 = st.columns(3)
latest_price = forecast.iloc[-1]["yhat"]
change = latest_price - forecast.iloc[-60]["yhat"]
percent = (change / forecast.iloc[-60]["yhat"]) * 100

col1.metric("Latest Gold Price", f"₹{latest_price:,.2f}")
col2.metric("Price Change in 60 Days", f"₹{change:,.2f}", f"{percent:.2f}%")
col3.metric("Investment Tip", "Consider investing now" if percent > 2 else "Better to wait")

# ----------------------
# Forecast Graph
# ----------------------
st.subheader("📈 Gold Price Prediction (Next 60 Days)")
fig = go.Figure()
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], mode="lines", name="Predicted Price", line=dict(color="gold")))
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_upper"], mode="lines", name="Upper Bound", line=dict(dash='dot', color="lightgreen")))
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_lower"], mode="lines", name="Lower Bound", line=dict(dash='dot', color="salmon")))
fig.update_layout(title="Gold Price Forecast for Next 60 Days", xaxis_title="Date", yaxis_title="Gold Price (INR per 10g)", template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

# ----------------------
# Predict Price for a Specific Date
# ----------------------
st.subheader("🔍 Get Predicted Gold Price for a Specific Date")

st.caption("Note: Forecast available for the next 60 days only.")

target_date = st.date_input("Select a future date", value=pd.to_datetime("2025-04-10"))
target_date = pd.to_datetime(target_date)

result = forecast[forecast["ds"] == target_date]

if not result.empty:
    predicted_price = result["yhat"].values[0]
    lower_bound = result["yhat_lower"].values[0]
    upper_bound = result["yhat_upper"].values[0]

    st.success(f"📅 Predicted Price on {target_date.date()}: ₹{predicted_price:,.2f}")
    st.info(f"🟢 Confidence Range: ₹{lower_bound:,.2f} – ₹{upper_bound:,.2f}")

    if predicted_price > forecast.iloc[-1]["yhat"]:
        st.success("✅ Prices expected to rise — Consider investing.")
    elif predicted_price < forecast.iloc[-1]["yhat"]:
        st.warning("⚠️ Prices expected to dip — Better to wait.")
    else:
        st.info("📊 Price stable — Invest as needed.")
else:
    st.error("❌ Prediction not available for the selected date. Try a date within the next 60 days.")

# ----------------------
# Historical Gold Price Graphs (India and Global Separately)
# ----------------------
st.subheader("📉 Historical Gold Price in India")
try:
    gold_df = pd.read_csv("gold this final.csv")
    gold_df["Date"] = pd.to_datetime(gold_df["Date"], dayfirst=True)
    fig_india = go.Figure()
    fig_india.add_trace(go.Scatter(x=gold_df["Date"], y=gold_df["Price 10g (in INR)"], mode="lines", name="India Gold Price (10g)", line=dict(color="orange")))
    fig_india.update_layout(title="Historical Gold Price in India", xaxis_title="Date", yaxis_title="Price (INR)", template="plotly_white")
    st.plotly_chart(fig_india, use_container_width=True)

    st.subheader("🌍 Historical Global Gold Price (LBMA)")
    fig_global = go.Figure()
    fig_global.add_trace(go.Scatter(x=gold_df["Date"], y=gold_df["GGP (LBMA)"], mode="lines", name="Global Gold Price (LBMA)", line=dict(color="green")))
    fig_global.update_layout(title="Historical Global Gold Price (LBMA)", xaxis_title="Date", yaxis_title="Price (USD)", template="plotly_white")
    st.plotly_chart(fig_global, use_container_width=True)
except Exception as e:
    st.warning("Unable to load historical gold price data. Ensure 'gold this final.csv' has the required columns.")

# ----------------------
# Time Range Filtering
# ----------------------
st.subheader("🗕️ Filter Forecast Data by Date Range")
start_date = pd.to_datetime(st.date_input("Start Date", value=pd.to_datetime("2023-01-01")))
end_date = pd.to_datetime(st.date_input("End Date", value=pd.to_datetime("2025-01-01")))
filtered_data = forecast[(forecast['ds'] >= start_date) & (forecast['ds'] <= end_date)].copy()
filtered_data.set_index("ds", inplace=True)
st.line_chart(filtered_data["yhat"])

# ----------------------
# Forecast Table
# ----------------------
with st.expander("📊 View Raw Forecast Data Table"):
    st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(60))
