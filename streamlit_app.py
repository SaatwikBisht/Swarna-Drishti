#SWARNA DRISHTI

import streamlit as st
import pandas as pd
from prophet.plot import plot_plotly
import plotly.graph_objs as go

st.set_page_config(page_title="Swarna Drishti", layout="wide")
st.title("💰 Swarna Drishti – Predicting the Future of Gold Investment")
st.markdown("Get smart insights into India's gold price trends with AI-powered forecasting.")

@st.cache_data
def load_forecast():
    forecast = pd.read_csv("forecast.csv")
    forecast["ds"] = pd.to_datetime(forecast["ds"])
    return forecast

forecast = load_forecast()

st.subheader("📈 Forecasted Gold Price (Next 30 Days)")

fig = go.Figure()
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], mode="lines", name="Predicted Price", line=dict(color="gold")))
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_upper"], mode="lines", name="Upper Bound", line=dict(dash='dot', color="lightgreen")))
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_lower"], mode="lines", name="Lower Bound", line=dict(dash='dot', color="salmon")))
fig.update_layout(title="Gold Price Prediction for Next 30 Days", xaxis_title="Date", yaxis_title="Gold Price (INR per 10g)", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

st.subheader("💡 Investment Tip")
latest = forecast.iloc[-1]["yhat"]
earlier = forecast.iloc[-31]["yhat"]
change = latest - earlier
percent = (change / earlier) * 100
st.metric("Expected Change", f"₹{change:,.2f}", f"{percent:.2f}%")

if percent > 2:
    st.success("✅ Prices expected to rise — consider investing.")
elif percent < -2:
    st.warning("⏳ Prices expected to fall — better to wait.")
else:
    st.info("⚖️ Stable trend — invest if needed.")

with st.expander("📊 Show Forecast Data Table"):
    st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(30))

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from prophet.plot import plot_plotly
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------
# Set Page Layout and Style
# ----------------------
st.set_page_config(page_title="Swarna Drishti", layout="wide")

# Add Background Image
st.markdown("""
    <style>
    .reportview-container {
        background: url('https://your-gold-background-image-link.jpg');
        background-size: cover;
        background-position: center;
    }
    </style>
""", unsafe_allow_html=True)

# Add a fancy header
st.title("<h1 style='color:gold; text-align:center;'>Swarna Drishti</h1>", unsafe_allow_html=True)
st.subheader("<h3 style='color:gold; text-align:center;'>AI-Powered Gold Price Oracle</h3>", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align:center; color: white;">
        <p style="font-size:16px;">
            Welcome to Swarna Drishti! Get your **AI-powered gold price predictions** and investment tips.
        </p>
    </div>
""", unsafe_allow_html=True)

# ----------------------
# Load Forecast Data
# ----------------------
@st.cache_data
def load_forecast():
    forecast = pd.read_csv("forecast.csv")  # Ensure this is in the repo
    forecast["ds"] = pd.to_datetime(forecast["ds"])
    return forecast

forecast = load_forecast()

# ----------------------
# Layer 1: Overview Dashboard
# ----------------------
col1, col2, col3 = st.columns(3)
latest_price = forecast.iloc[-1]["yhat"]
change = latest_price - forecast.iloc[-31]["yhat"]
percent = (change / forecast.iloc[-31]["yhat"]) * 100

col1.metric("Latest Gold Price", f"₹{latest_price:,.2f}")
col2.metric("Price Change in 30 Days", f"₹{change:,.2f}", f"{percent:.2f}%")
col3.metric("Investment Tip", "Consider investing now" if percent > 2 else "Better to wait")

# ----------------------
# Layer 2: Interactive Forecast Graph
# ----------------------
st.subheader("📈 Gold Price Prediction (Next 30 Days)")

fig = go.Figure()
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], mode="lines", name="Predicted Price", line=dict(color="gold")))
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_upper"], mode="lines", name="Upper Bound", line=dict(dash='dot', color="lightgreen")))
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_lower"], mode="lines", name="Lower Bound", line=dict(dash='dot', color="salmon")))

fig.update_layout(
    title="Gold Price Forecast for Next 30 Days",
    xaxis_title="Date",
    yaxis_title="Gold Price (INR per 10g)",
    template="plotly_dark",  # Dark theme for contrast
    plot_bgcolor="rgba(0,0,0,0)",  # Transparent background for a modern feel
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------
# Layer 3: Correlation Heatmap
# ----------------------
st.subheader("🔍 Correlation Between Economic Factors and Gold Price")

# Assuming you have 'USD_INR', 'Inflation_CPI', 'NIF' in your original data
df = pd.read_csv("forecast.csv")  # Replace with your original data path if needed
corr_data = df[['Gold_Price_10g_INR', 'USD_INR', 'Inflation_CPI', 'NIF']].corr()

fig2, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_data, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
st.pyplot(fig2)

# ----------------------
# Layer 4: Scenario-Based Prediction
# ----------------------
st.subheader("💡 Scenario-Based Price Prediction")
usd_inr_change = st.slider("USD to INR Change (%)", min_value=-5, max_value=5, value=0)
simulated_forecast = forecast.copy()
simulated_forecast['adjusted'] = simulated_forecast['yhat'] * (1 + usd_inr_change / 100)

st.line_chart(simulated_forecast[['ds', 'adjusted']])

# ----------------------
# Layer 5: Historical vs Predicted Price Comparison
# ----------------------
st.subheader("📊 Historical vs Predicted Gold Price")

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df['ds'], y=df['Gold_Price_10g_INR'], mode='lines', name='Historical Price'))
fig3.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Predicted Price', line=dict(color='gold')))
st.plotly_chart(fig3, use_container_width=True)

# ----------------------
# Layer 6: Data Filtering and Time Range Selection
# ----------------------
st.subheader("📅 Filter Forecast Data by Date Range")
start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2025-01-01"))

filtered_data = forecast[(forecast['ds'] >= start_date) & (forecast['ds'] <= end_date)]
st.line_chart(filtered_data[['ds', 'yhat']])

# ----------------------
# Layer 7: Raw Forecast Data Table
# ----------------------
with st.expander("📊 View Raw Forecast Data Table"):
    st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(30))
