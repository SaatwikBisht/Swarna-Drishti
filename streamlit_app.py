import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Swarna Drishti", layout="wide")

st.markdown("<h1 style='text-align:center; color:gold;'>Swarna Drishti</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:white;'>Your AI-Powered 24KT Gold Price Oracle</h4>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid gold;'>", unsafe_allow_html=True)

@st.cache_data
def load_forecast():
    try:
        df = pd.read_csv("forecast.csv")
        df = df[["ds", "yhat", "yhat_lower", "yhat_upper"]]
        df.rename(columns={
            "ds": "Date",
            "yhat": "Predicted",
            "yhat_lower": "Lower_Bound",
            "yhat_upper": "Upper_Bound"
        }, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values("Date", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading forecast data: {str(e)}")
        return pd.DataFrame()

df = load_forecast()

if df.empty:
    st.error("❌ Forecast data not found or empty. Please check forecast.csv.")
    st.stop()

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
    date_str = latest["Date"].strftime("%Y-%m-%d")
    st.metric("📅 Latest Forecast Date", date_str)

with col2:
    price_str = f"₹{latest['Predicted']:,.2f}"
    st.metric("📈 24KT Gold Price (Predicted)", price_str)

with col3:
    delta_str = f"₹{delta:,.2f}"
    percent_str = f"{percent_change:.2f}%"
    st.metric("📊 1-Day Change", delta_str, percent_str)

st.markdown("### 📈 Gold Price Forecast – Next 7 Days (24KT)")
future_df = df.head(7)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=future_df["Date"], 
    y=future_df["Predicted"], 
    mode="lines+markers", 
    name="Predicted Price", 
    line=dict(color="gold", width=3),
    marker=dict(size=8)
))
fig.add_trace(go.Scatter(
    x=future_df["Date"], 
    y=future_df["Upper_Bound"], 
    mode="lines", 
    name="Upper Bound", 
    line=dict(dash="dot", color="lightgreen", width=2)
))
fig.add_trace(go.Scatter(
    x=future_df["Date"], 
    y=future_df["Lower_Bound"], 
    mode="lines", 
    name="Lower Bound", 
    line=dict(dash="dot", color="salmon", width=2)
))
fig.update_layout(
    title="24KT Gold Price Forecast",
    xaxis_title="Date",
    yaxis_title="INR per 10g",
    template="plotly_dark",
    showlegend=True,
    height=500
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 💡 Investment Insight")
if len(future_df) >= 2:
    price_start = future_df["Predicted"].iloc[0]
    price_end = future_df["Predicted"].iloc[-1]
    price_change = ((price_end - price_start) / price_start) * 100
    
    if price_change > 2:
        st.success(f"📈 Price is expected to rise by {price_change:.2f}% in the next 7 days – Excellent time to invest!")
    elif price_change > 0:
        st.success(f"📈 Price is expected to rise by {price_change:.2f}% in the next 7 days – Good time to invest.")
    elif price_change < -2:
        st.warning(f"📉 Price is expected to decline by {abs(price_change):.2f}% in the next 7 days – Consider waiting.")
    elif price_change < 0:
        st.warning(f"📉 Price is expected to decline by {abs(price_change):.2f}% in the next 7 days – You may wait.")
    else:
        st.info("⏸️ Price is expected to remain stable – Neutral investment window.")
else:
    st.info("⏸️ Insufficient data for investment insight.")

st.markdown("### 🔍 Predict Gold Price for a Specific Date")
with st.form("predict_form"):
    col_date, col_button = st.columns([3, 1])
    with col_date:
        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()
        default_date = df["Date"].iloc[0].date()
        selected_date = st.date_input(
            "Select a date to predict",
            value=default_date,
            min_value=min_date,
            max_value=max_date
        )
    with col_button:
        st.write("")
        submitted = st.form_submit_button("🔎 Predict", use_container_width=True)

if submitted:
    selected_datetime = pd.to_datetime(selected_date)
    match = df[df["Date"].dt.date == selected_date]
    
    if not match.empty:
        row = match.iloc[0]
        col_pred, col_conf = st.columns(2)
        with col_pred:
            price_str = f"₹{row['Predicted']:,.2f}"
            st.success(f"📆 Predicted 24KT Gold Price on {selected_date}: {price_str}")
        with col_conf:
            lower_str = f"₹{row['Lower_Bound']:,.2f}"
            upper_str = f"₹{row['Upper_Bound']:,.2f}"
            st.info(f"📊 Confidence Interval: {lower_str} – {upper_str}")
        
        volatility = row['Upper_Bound'] - row['Lower_Bound']
        confidence_percent = ((row['Predicted'] - row['Lower_Bound']) / (row['Upper_Bound'] - row['Lower_Bound'])) * 100
        vol_str = f"₹{volatility:.2f}"
        st.info(f"📈 Prediction Confidence: {confidence_percent:.1f}% | Market Volatility: {vol_str}")
    else:
        st.error("❌ No forecast available for this date.")

st.markdown("### 📋 Extended Forecast – Next 30 Days")
extended_df = df.head(30).copy()
extended_df["Date_Formatted"] = extended_df["Date"].dt.strftime("%Y-%m-%d")
extended_df["Predicted_Formatted"] = extended_df["Predicted"].apply(lambda x: f"₹{x:,.2f}")
extended_df["Lower_Bound_Formatted"] = extended_df["Lower_Bound"].apply(lambda x: f"₹{x:,.2f}")
extended_df["Upper_Bound_Formatted"] = extended_df["Upper_Bound"].apply(lambda x: f"₹{x:,.2f}")

display_df = extended_df[["Date_Formatted", "Predicted_Formatted", "Lower_Bound_Formatted", "Upper_Bound_Formatted"]]
display_df.columns = ["Date", "Predicted Price", "Lower Bound", "Upper Bound"]

st.dataframe(display_df, use_container_width=True, height=400)

st.markdown("### 📊 Price Statistics")
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    avg_price = df["Predicted"].mean()
    avg_str = f"₹{avg_price:,.2f}"
    st.metric("📈 Average Price", avg_str)

with col_stat2:
    max_price = df["Predicted"].max()
    max_date = df[df["Predicted"] == max_price]["Date"].iloc[0]
    max_str = f"₹{max_price:,.2f}"
    st.metric("🔺 Highest Price", max_str)
    st.caption(f"Expected on {max_date.strftime('%Y-%m-%d')}")

with col_stat3:
    min_price = df["Predicted"].min()
    min_date = df[df["Predicted"] == min_price]["Date"].iloc[0]
    min_str = f"₹{min_price:,.2f}"
    st.metric("🔻 Lowest Price", min_str)
    st.caption(f"Expected on {min_date.strftime('%Y-%m-%d')}")

with col_stat4:
    price_range = max_price - min_price
    range_str = f"₹{price_range:,.2f}"
    st.metric("📏 Price Range", range_str)

st.markdown("### 🎯 Investment Recommendations")
current_price = latest["Predicted"]
avg_price_7_days = future_df["Predicted"].mean()
trend_direction = "bullish" if avg_price_7_days > current_price else "bearish"

if trend_direction == "bullish":
    st.success("🐂 **Bullish Trend Detected**: Market sentiment is positive. Consider gradual investment.")
    st.info("💡 **Strategy**: Dollar-cost averaging recommended. Invest in small amounts regularly.")
else:
    st.warning("🐻 **Bearish Trend Detected**: Market sentiment is cautious. Wait for better entry points.")
    st.info("💡 **Strategy**: Monitor closely and consider investing when prices stabilize.")

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>© 2025 Swarna Drishti | Powered by Prophet Forecast</p>", unsafe_allow_html=True)