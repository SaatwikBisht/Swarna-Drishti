import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.set_page_config(page_title="Swarna Drishti", layout="wide")

st.markdown("<h1 style='text-align:center; color:gold;'>Swarna Drishti</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:white;'>Your AI-Powered 24KT Gold Price Oracle</h4>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid gold;'>", unsafe_allow_html=True)

@st.cache_data
def load_forecast():
    try:
        df = pd.read_csv("forecast.csv")
        required_cols = ["ds", "yhat", "yhat_lower", "yhat_upper"]
        df = df[required_cols].copy()
        df.columns = ["Date", "Predicted", "Lower_Bound", "Upper_Bound"]
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date").reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"Error loading forecast data: {e}")
        return pd.DataFrame()

df = load_forecast()

if df.empty:
    st.error("❌ Forecast data not found or empty. Please check forecast.csv.")
    st.stop()

latest_row = df.iloc[-1]
latest_date = latest_row["Date"]
latest_price = latest_row["Predicted"]

if len(df) > 1:
    previous_row = df.iloc[-2]
    previous_price = previous_row["Predicted"]
    delta = latest_price - previous_price
    percent_change = (delta / previous_price) * 100 if previous_price != 0 else 0
else:
    delta = 0
    percent_change = 0

col1, col2, col3 = st.columns(3)

with col1:
    date_string = pd.to_datetime(latest_date).strftime("%Y-%m-%d")
    st.metric("📅 Latest Forecast Date", date_string)

with col2:
    price_string = f"₹{latest_price:,.2f}"
    st.metric("📈 24KT Gold Price (Predicted)", price_string)

with col3:
    delta_string = f"₹{delta:,.2f}"
    percent_string = f"{percent_change:.2f}%"
    st.metric("📊 1-Day Change", delta_string, percent_string)

st.markdown("### 📈 Gold Price Forecast – Next 7 Days (24KT)")
next_7_days = df.head(7).copy()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=next_7_days["Date"], 
    y=next_7_days["Predicted"], 
    mode="lines+markers", 
    name="Predicted Price", 
    line=dict(color="gold", width=3),
    marker=dict(size=8)
))

fig.add_trace(go.Scatter(
    x=next_7_days["Date"], 
    y=next_7_days["Upper_Bound"], 
    mode="lines", 
    name="Upper Bound", 
    line=dict(dash="dot", color="lightgreen", width=2)
))

fig.add_trace(go.Scatter(
    x=next_7_days["Date"], 
    y=next_7_days["Lower_Bound"], 
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
if len(next_7_days) >= 2:
    start_price = next_7_days["Predicted"].iloc[0]
    end_price = next_7_days["Predicted"].iloc[-1]
    price_trend = ((end_price - start_price) / start_price) * 100
    
    if price_trend > 2:
        st.success(f"📈 Price expected to rise by {price_trend:.2f}% – Excellent time to invest!")
    elif price_trend > 0:
        st.success(f"📈 Price expected to rise by {price_trend:.2f}% – Good time to invest.")
    elif price_trend < -2:
        st.warning(f"📉 Price expected to decline by {abs(price_trend):.2f}% – Consider waiting.")
    elif price_trend < 0:
        st.warning(f"📉 Price expected to decline by {abs(price_trend):.2f}% – You may wait.")
    else:
        st.info("⏸️ Price expected to remain stable – Neutral investment window.")
else:
    st.info("⏸️ Insufficient data for insight.")

st.markdown("### 🔍 Predict Gold Price for a Specific Date")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()
default_date = df["Date"].iloc[0].date()

selected_date = st.date_input(
    "Select a date to predict:",
    value=default_date,
    min_value=min_date,
    max_value=max_date
)

if st.button("🔎 Get Prediction"):
    matching_rows = df[df["Date"].dt.date == selected_date]
    
    if not matching_rows.empty:
        prediction_row = matching_rows.iloc[0]
        predicted_price = prediction_row["Predicted"]
        lower_bound = prediction_row["Lower_Bound"]
        upper_bound = prediction_row["Upper_Bound"]
        
        col_pred, col_conf = st.columns(2)
        
        with col_pred:
            st.success(f"📆 Predicted Price on {selected_date}: ₹{predicted_price:,.2f}")
        
        with col_conf:
            st.info(f"📊 Range: ₹{lower_bound:,.2f} – ₹{upper_bound:,.2f}")
        
        volatility = upper_bound - lower_bound
        st.info(f"📈 Market Volatility: ₹{volatility:.2f}")
    else:
        st.error("❌ No forecast available for this date.")

st.markdown("### 📋 Extended Forecast – Next 30 Days")
extended_forecast = df.head(30).copy()
extended_forecast["Date"] = extended_forecast["Date"].dt.strftime("%Y-%m-%d")
extended_forecast["Predicted"] = extended_forecast["Predicted"].apply(lambda x: f"₹{x:,.2f}")
extended_forecast["Lower_Bound"] = extended_forecast["Lower_Bound"].apply(lambda x: f"₹{x:,.2f}")
extended_forecast["Upper_Bound"] = extended_forecast["Upper_Bound"].apply(lambda x: f"₹{x:,.2f}")

extended_forecast.columns = ["Date", "Predicted Price", "Lower Bound", "Upper Bound"]
st.dataframe(extended_forecast, use_container_width=True, height=400)

st.markdown("### 📊 Price Statistics")
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    avg_price = df["Predicted"].mean()
    st.metric("📈 Average Price", f"₹{avg_price:,.2f}")

with col_stat2:
    max_price = df["Predicted"].max()
    max_idx = df["Predicted"].idxmax()
    max_date = df.iloc[max_idx]["Date"].strftime("%Y-%m-%d")
    st.metric("🔺 Highest Price", f"₹{max_price:,.2f}")
    st.caption(f"Expected on {max_date}")

with col_stat3:
    min_price = df["Predicted"].min()
    min_idx = df["Predicted"].idxmin()
    min_date = df.iloc[min_idx]["Date"].strftime("%Y-%m-%d")
    st.metric("🔻 Lowest Price", f"₹{min_price:,.2f}")
    st.caption(f"Expected on {min_date}")

with col_stat4:
    price_range = max_price - min_price
    st.metric("📏 Price Range", f"₹{price_range:,.2f}")

st.markdown("### 🎯 Investment Recommendations")
current_price = latest_price
avg_price_7_days = next_7_days["Predicted"].mean()

if avg_price_7_days > current_price:
    st.success("🐂 **Bullish Trend**: Market sentiment positive. Consider investment.")
    st.info("💡 **Strategy**: Dollar-cost averaging recommended.")
else:
    st.warning("🐻 **Bearish Trend**: Market sentiment cautious. Wait for better entry.")
    st.info("💡 **Strategy**: Monitor closely for stabilization.")

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>© 2025 Swarna Drishti | Powered by Prophet Forecast</p>", unsafe_allow_html=True)