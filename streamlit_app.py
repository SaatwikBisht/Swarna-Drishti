#SWARNA DRISHTI

import streamlit as st
import pandas as pd
from prophet.plot import plot_plotly
import plotly.graph_objs as go

st.set_page_config(page_title="Swarna Drishti", layout="wide")
st.title("💰 Swarna Drishti – AI Gold Price Forecast")
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
