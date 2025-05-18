import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# -------------------- Page Config --------------------
st.set_page_config(page_title="Swarna Drishti", layout="wide")

# -------------------- App Title --------------------
st.markdown("<h1 style='text-align:center; color:gold;'>Swarna Drishti</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:white;'>Your AI-Powered 24KT Gold Price Oracle</h4>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid gold;'>", unsafe_allow_html=True)

# -------------------- Load Forecast --------------------
@st.cache_data
def load_forecast():
    df = pd.read_csv("forecast.csv")
    df = df[["ds", "yhat", "yhat_lower", "yhat_upper"]]  # Only necessary columns
    df.rename(columns={
        "ds": "Date",
        "yhat": "Predicted",
        "yhat_lower": "Lower_Bound",
        "yhat_upper": "Upper_Bound"
    }, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", inplace=True)
    return df

df = load_forecast()

if df.empty:
    st.error("❌ Forecast data not found or empty. Please check forecast.csv.")
    st.stop()

# -------------------- Latest Forecast Metrics --------------------
latest = df.iloc[-1]
previous = df.iloc[-2] if len(df) > 1 else latest
delta = latest["Predicted"] - previous["Predicted"]
percent_change = (delta / previous["Predicted"]) * 100 if previous["Predicted"] != 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📅 Latest Forecast Date", latest["Date"].date())
with col2:
    st.metric("📈 24KT Gold Price (Predicted)", f"₹{latest['Predicted']:,.2f}")
with col3:
    st.metric("📊 1-Day Change", f"₹{delta:,.2f}", f"{percent_change:.2f}%")

# -------------------- Line Chart (Next 7 Days) --------------------
st.markdown("### 📈 Gold Price Forecast – Next 7 Days (24KT)")
future_df = df.head(7)

fig = go.Figure()
fig.add_trace(go.Scatter(x=future_df["Date"], y=future_df["Predicted"], mode="lines+markers", name="Predicted Price", line=dict(color="gold")))
fig.add_trace(go.Scatter(x=future_df["Date"], y=future_df["Upper_Bound"], mode="lines", name="Upper Bound", line=dict(dash="dot", color="lightgreen")))
fig.add_trace(go.Scatter(x=future_df["Date"], y=future_df["Lower_Bound"], mode="lines", name="Lower Bound", line=dict(dash="dot", color="salmon")))
fig.update_layout(
    title="24KT Gold Price Forecast",
    xaxis_title="Date",
    yaxis_title="INR per 10g",
    template="plotly_dark",
    showlegend=True
)
st.plotly_chart(fig, use_container_width=True)

# -------------------- Investment Insight --------------------
st.markdown("### 💡 Investment Insight")
if future_df["Predicted"].iloc[-1] > future_df["Predicted"].iloc[0]:
    st.success("📈 Price is rising – Good time to invest.")
elif future_df["Predicted"].iloc[-1] < future_df["Predicted"].iloc[0]:
    st.warning("📉 Price is declining – You may wait.")
else:
    st.info("⏸️ Price stable – Neutral window.")

# -------------------- Predict for Selected Date --------------------
st.markdown("### 🔍 Predict Gold Price for a Specific Date")
with st.form("predict_form"):
    selected_date = st.date_input("Select a date to predict", value=df["Date"].iloc[0].date(), min_value=df["Date"].min().date(), max_value=df["Date"].max().date())
    submitted = st.form_submit_button("🔎 Predict")

if submitted:
    match = df[df["Date"] == pd.to_datetime(selected_date)]
    if not match.empty:
        row = match.iloc[0]
        st.success(f"📆 Predicted 24KT Gold Price on {selected_date}: ₹{row['Predicted']:,.2f}")
        st.info(f"📊 Confidence Interval: ₹{row['Lower_Bound']:,.2f} – ₹{row['Upper_Bound']:,.2f}")
    else:
        st.error("❌ No forecast available for this date.")

# -------------------- Show Last 7 Days Forecast Table --------------------
st.markdown("### 📋 Last 7 Days – 24KT Gold Price Forecast")
last_7 = df.tail(7).copy()
last_7["Date"] = last_7["Date"].dt.strftime("%Y-%m-%d")
last_7.set_index("Date", inplace=True)

st.dataframe(last_7[["Predicted", "Lower_Bound", "Upper_Bound"]].rename(columns={
    "Predicted": "Predicted Price (INR)",
    "Lower_Bound": "Lower Bound",
    "Upper_Bound": "Upper Bound"
}), use_container_width=True)

# -------------------- Footer --------------------
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>© 2025 Swarna Drishti | Powered by Prophet Forecast</p>", unsafe_allow_html=True)
