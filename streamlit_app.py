import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

# ----------------------
# Set Page Config
# ----------------------
st.set_page_config(page_title="Swarna Drishti - AI Gold Forecast", layout="wide")

# ----------------------
# Title and Subtitle
# ----------------------
st.markdown("""
    <h1 style='text-align:center; color:gold;'>Swarna Drishti</h1>
    <h4 style='text-align:center; color:white;'>AI-Powered Forecast for 24KT Gold Price (INR / 10g)</h4>
""", unsafe_allow_html=True)

# ----------------------
# Load Forecast Data
# ----------------------
@st.cache_data
def load_forecast():
    forecast = pd.read_csv("forecast.csv")
    forecast["Date"] = pd.to_datetime(forecast["Date"])
    return forecast

forecast = load_forecast()

# ----------------------
# Display Today's Forecast
# ----------------------
latest_price = forecast.iloc[0]["Trident_Forecast"]
st.metric("Predicted Price Today (24KT)", f"\u20B9{latest_price:,.2f}")

# ----------------------
# 7-Day Forecast Graph
# ----------------------
st.subheader("📈 Next 7 Days 24KT Gold Price Forecast")
forecast_7 = forecast.head(7)
fig = go.Figure()
fig.add_trace(go.Scatter(x=forecast_7["Date"], y=forecast_7["Trident_Forecast"], mode="lines+markers", name="Forecast", line=dict(color="gold")))
fig.update_layout(title="Forecast for Next 7 Days (24KT Gold, INR per 10g)", xaxis_title="Date", yaxis_title="Price (INR)", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# ----------------------
# Investment Suggestion
# ----------------------
price_today = forecast.iloc[0]["Trident_Forecast"]
price_week = forecast.iloc[6]["Trident_Forecast"]
price_diff = price_week - price_today
percent_diff = (price_diff / price_today) * 100

if percent_diff > 1:
    st.success("\U0001F4B5 Gold price expected to rise. Consider investing.")
elif percent_diff < -1:
    st.warning("\u26A0\ufe0f Gold price expected to fall. Consider waiting.")
else:
    st.info("\u2139\ufe0f Gold price expected to remain stable. Invest as needed.")

# ----------------------
# Predict for a Selected Date
# ----------------------
st.subheader("🔮 Predict 24KT Gold Price for a Specific Date")
target_date = st.date_input("Select a date (within forecast range)", value=forecast["Date"].min(), min_value=forecast["Date"].min(), max_value=forecast["Date"].max())
if st.button("Predict Price"):
    result = forecast[forecast["Date"] == pd.to_datetime(target_date)]
    if not result.empty:
        predicted = result.iloc[0]["Trident_Forecast"]
        st.success(f"\U0001F4C5 Predicted Price on {target_date.strftime('%d %b %Y')}: \u20B9{predicted:,.2f} (24KT)")
    else:
        st.error("❌ Prediction not available for the selected date.")

# ----------------------
# Historical Table (Last 7 Days)
# ----------------------
st.subheader("📅 Last 7 Days Forecasted Gold Prices (24KT)")
st.dataframe(forecast.head(7).rename(columns={"Date": "Date", "Trident_Forecast": "Forecasted Price (INR)"}), use_container_width=True)
