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
latest_price = latest_row["Predicted_Price"]

if len(df) > 1:
    previous_row = df.iloc[-2]
    previous_price = previous_row["Predicted_Price"]
    daily_change = latest_price - previous_price
    percent_change = (daily_change / previous_price) * 100 if previous_price != 0 else 0
else:
    daily_change = 0
    percent_change = 0

col1, col2, col3 = st.columns(3)

with col1:
    date_str = latest_date.strftime("%Y-%m-%d")
    st.metric("📅 Latest Forecast Date", date_str)

with col2:
    price_str = f"₹{latest_price:,.2f}"
    st.metric("📈 24KT Gold Price (Predicted)", price_str)

with col3:
    change_str = f"₹{daily_change:,.2f}"
    percent_str = f"{percent_change:.2f}%"
    st.metric("📊 1-Day Change", change_str, percent_str)

st.markdown("### 📈 Gold Price Forecast – Next 7 Days (24KT)")
next_7_days = df.head(7).copy()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=next_7_days["Date"], 
    y=next_7_days["Predicted_Price"], 
    mode="lines+markers", 
    name="Predicted Price", 
    line=dict(color="gold", width=4),
    marker=dict(size=10, color="gold"),
    fill=None
))

fig.update_layout(
    title="24KT Gold Price Forecast - Next 7 Days",
    xaxis_title="Date",
    yaxis_title="INR per 10g",
    template="plotly_dark",
    showlegend=True,
    height=500,
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 💡 Investment Insight")
if len(next_7_days) >= 2:
    start_price = next_7_days["Predicted_Price"].iloc[0]
    end_price = next_7_days["Predicted_Price"].iloc[-1]
    weekly_trend = ((end_price - start_price) / start_price) * 100
    
    if weekly_trend > 3:
        st.success(f"📈 **Strong Bullish Signal**: Price expected to rise by {weekly_trend:.2f}% over next 7 days – Excellent time to invest!")
        st.info("💰 **Recommendation**: Consider buying gold now as significant gains are expected.")
    elif weekly_trend > 1:
        st.success(f"📈 **Bullish Signal**: Price expected to rise by {weekly_trend:.2f}% over next 7 days – Good time to invest.")
        st.info("💰 **Recommendation**: Favorable conditions for gold investment.")
    elif weekly_trend > -1:
        st.info(f"⏸️ **Stable Market**: Price expected to change by {weekly_trend:.2f}% over next 7 days – Neutral investment window.")
        st.info("💰 **Recommendation**: Market is stable, suitable for steady investment.")
    elif weekly_trend > -3:
        st.warning(f"📉 **Bearish Signal**: Price expected to decline by {abs(weekly_trend):.2f}% over next 7 days – Consider waiting.")
        st.info("💰 **Recommendation**: Wait for better entry points or invest with caution.")
    else:
        st.error(f"📉 **Strong Bearish Signal**: Price expected to decline by {abs(weekly_trend):.2f}% over next 7 days – Not recommended to invest now.")
        st.info("💰 **Recommendation**: Avoid buying gold currently, prices may fall further.")
else:
    st.info("⏸️ Insufficient data for weekly trend analysis.")

st.markdown("### 🔍 Predict Gold Price for a Specific Date")

col_date, col_button = st.columns([3, 1])

with col_date:
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    default_date = df["Date"].iloc[0].date()
    
    selected_date = st.date_input(
        "Select a date to predict:",
        value=default_date,
        min_value=min_date,
        max_value=max_date
    )

with col_button:
    st.write("")
    predict_button = st.button("🔎 Get Prediction", use_container_width=True)

if predict_button:
    matching_rows = df[df["Date"].dt.date == selected_date]
    
    if not matching_rows.empty:
        prediction_row = matching_rows.iloc[0]
        predicted_price = prediction_row["Predicted_Price"]
        
        st.success(f"📆 **Predicted 24KT Gold Price on {selected_date}**: ₹{predicted_price:,.2f}")
        
        current_price = latest_price
        price_diff = predicted_price - current_price
        price_change_percent = (price_diff / current_price) * 100
        
        if price_diff > 0:
            st.info(f"📈 Price is expected to be ₹{price_diff:,.2f} ({price_change_percent:.2f}%) higher than current prediction")
        elif price_diff < 0:
            st.info(f"📉 Price is expected to be ₹{abs(price_diff):,.2f} ({abs(price_change_percent):.2f}%) lower than current prediction")
        else:
            st.info("⏸️ Price is expected to remain same as current prediction")
    else:
        st.error("❌ No forecast available for the selected date.")

st.markdown("### 📋 Extended Forecast Table")

tab1, tab2 = st.tabs(["📅 Next 7 Days", "📅 Next 30 Days"])

with tab1:
    display_7_days = next_7_days.copy()
    display_7_days["Date"] = display_7_days["Date"].dt.strftime("%Y-%m-%d")
    display_7_days["Predicted_Price"] = display_7_days["Predicted_Price"].apply(lambda x: f"₹{x:,.2f}")
    display_7_days.columns = ["Date", "Predicted Price (INR)"]
    st.dataframe(display_7_days, use_container_width=True, height=300)

with tab2:
    next_30_days = df.head(30).copy()
    display_30_days = next_30_days.copy()
    display_30_days["Date"] = display_30_days["Date"].dt.strftime("%Y-%m-%d")
    display_30_days["Predicted_Price"] = display_30_days["Predicted_Price"].apply(lambda x: f"₹{x:,.2f}")
    display_30_days.columns = ["Date", "Predicted Price (INR)"]
    st.dataframe(display_30_days, use_container_width=True, height=400)

st.markdown("### 📊 Price Analysis & Statistics")

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    avg_price = df["Predicted_Price"].mean()
    st.metric("📊 Average Price", f"₹{avg_price:,.2f}")

with col_stat2:
    max_price = df["Predicted_Price"].max()
    max_idx = df["Predicted_Price"].idxmax()
    max_date_str = df.iloc[max_idx]["Date"].strftime("%Y-%m-%d")
    st.metric("🔺 Highest Price", f"₹{max_price:,.2f}")
    st.caption(f"Expected on {max_date_str}")

with col_stat3:
    min_price = df["Predicted_Price"].min()
    min_idx = df["Predicted_Price"].idxmin()
    min_date_str = df.iloc[min_idx]["Date"].strftime("%Y-%m-%d")
    st.metric("🔻 Lowest Price", f"₹{min_price:,.2f}")
    st.caption(f"Expected on {min_date_str}")

with col_stat4:
    price_volatility = max_price - min_price
    volatility_percent = (price_volatility / avg_price) * 100
    st.metric("📏 Price Volatility", f"₹{price_volatility:,.2f}")
    st.caption(f"{volatility_percent:.1f}% of avg price")

st.markdown("### 🎯 Investment Strategy Recommendations")

current_price = latest_price
avg_next_7_days = next_7_days["Predicted_Price"].mean()
avg_next_30_days = df.head(30)["Predicted_Price"].mean()

col_strategy1, col_strategy2 = st.columns(2)

with col_strategy1:
    st.markdown("#### 🗓️ Short-term (7 Days)")
    if avg_next_7_days > current_price * 1.02:
        st.success("🟢 **BUY SIGNAL**: Strong upward trend expected")
        st.write("• Consider buying within next 1-2 days")
        st.write("• Expected short-term gains")
    elif avg_next_7_days < current_price * 0.98:
        st.error("🔴 **SELL/WAIT SIGNAL**: Downward trend expected")
        st.write("• Avoid buying for next week")
        st.write("• Consider selling if you own gold")
    else:
        st.info("🟡 **HOLD SIGNAL**: Stable prices expected")
        st.write("• Market consolidation phase")
        st.write("• Suitable for steady investors")

with col_strategy2:
    st.markdown("#### 📅 Long-term (30 Days)")
    if avg_next_30_days > current_price * 1.05:
        st.success("🟢 **STRONG BUY**: Excellent long-term prospects")
        st.write("• Dollar-cost averaging recommended")
        st.write("• Suitable for retirement planning")
    elif avg_next_30_days < current_price * 0.95:
        st.warning("🟠 **WAIT**: Better entry points ahead")
        st.write("• Monitor for 2-3 weeks")
        st.write("• Set price alerts for better entry")
    else:
        st.info("🟡 **NEUTRAL**: Steady long-term outlook")
        st.write("• Good for regular SIP investments")
        st.write("• Low risk, moderate returns")

st.markdown("### 📈 Price Trend Visualization - Extended View")
fig_extended = go.Figure()
fig_extended.add_trace(go.Scatter(
    x=df["Date"], 
    y=df["Predicted_Price"], 
    mode="lines", 
    name="Predicted Price Trend", 
    line=dict(color="gold", width=3),
    fill=None
))

fig_extended.update_layout(
    title="Gold Price Forecast - Complete Timeline",
    xaxis_title="Date",
    yaxis_title="INR per 10g",
    template="plotly_dark",
    height=400,
    hovermode='x unified'
)

st.plotly_chart(fig_extended, use_container_width=True)

st.markdown("---")
st.markdown("### ⚠️ Disclaimer")
st.warning("""
**Important Notice**: 
- These predictions are based on historical data and AI modeling
- Gold prices are subject to market volatility and external factors
- Always consult with financial advisors before making investment decisions
- Past performance does not guarantee future results
""")

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>© 2025 Swarna Drishti | Powered by Prophet Forecast | Made with ❤️ for Smart Investors</p>", unsafe_allow_html=True)