import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Swarna Drishti", layout="wide")

st.markdown("<h1 style='text-align:center; color:gold;'>Swarna Drishti</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:white;'>Your AI-Powered 24KT Gold Price Oracle</h4>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid gold;'>", unsafe_allow_html=True)

# Debug section - let's see what's in your CSV
st.write("🔍 **Debug Information:**")

try:
    # Try to load the CSV and show its structure
    df_raw = pd.read_csv("forecast.csv")
    st.write(f"✅ CSV loaded successfully!")
    st.write(f"📊 **Shape:** {df_raw.shape}")
    st.write(f"📋 **Columns:** {list(df_raw.columns)}")
    st.write(f"🔤 **Data types:**")
    st.write(df_raw.dtypes)
    st.write(f"📄 **First 5 rows:**")
    st.write(df_raw.head())
    
    # Try to convert Date column
    if 'Date' in df_raw.columns:
        st.write("🔄 Converting Date column...")
        df_raw["Date"] = pd.to_datetime(df_raw["Date"])
        st.write("✅ Date conversion successful!")
    else:
        st.error("❌ No 'Date' column found! Available columns are: " + str(list(df_raw.columns)))
        st.stop()
    
    # Check for Predicted_Price column
    if 'Predicted_Price' not in df_raw.columns:
        st.error("❌ No 'Predicted_Price' column found! Available columns are: " + str(list(df_raw.columns)))
        st.stop()
    
except FileNotFoundError:
    st.error("❌ forecast.csv file not found in the current directory!")
    st.write("Please make sure the CSV file is in the same folder as your streamlit app.")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading CSV: {str(e)}")
    st.write(f"Error type: {type(e).__name__}")
    st.stop()

# Define the load_forecast function with better error handling
@st.cache_data
def load_forecast():
    try:
        df = pd.read_csv("forecast.csv")
        
        # Check if required columns exist
        required_columns = ['Date', 'Predicted_Price']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Convert Date column to datetime
        df["Date"] = pd.to_datetime(df["Date"])
        
        # Sort by date and reset index
        df = df.sort_values("Date").reset_index(drop=True)
        
        return df
        
    except Exception as e:
        st.error(f"Error in load_forecast: {str(e)}")
        return pd.DataFrame()

# Load the forecast data
df = load_forecast()

if df.empty:
    st.error("❌ Could not load forecast data. Please check the debug information above.")
    st.stop()

st.success("✅ Forecast data loaded successfully!")

# Get latest data with error handling
try:
    latest_row = df.iloc[-1]
    latest_date = latest_row["Date"]
    latest_price = latest_row["Predicted_Price"]
    
    # Debug: Show the types of these variables
    st.write("🔍 **Variable types:**")
    st.write(f"latest_date type: {type(latest_date)}")
    st.write(f"latest_price type: {type(latest_price)}")
    st.write(f"latest_date value: {latest_date}")
    st.write(f"latest_price value: {latest_price}")
    
except Exception as e:
    st.error(f"❌ Error accessing latest data: {str(e)}")
    st.stop()

# Calculate daily change
try:
    if len(df) > 1:
        previous_row = df.iloc[-2]
        previous_price = previous_row["Predicted_Price"]
        daily_change = latest_price - previous_price
        percent_change = (daily_change / previous_price) * 100 if previous_price != 0 else 0
    else:
        daily_change = 0
        percent_change = 0
except Exception as e:
    st.error(f"❌ Error calculating daily change: {str(e)}")
    daily_change = 0
    percent_change = 0

# Display metrics with better error handling
st.markdown("### 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    try:
        # Convert datetime to string more carefully
        if hasattr(latest_date, 'strftime'):
            date_str = latest_date.strftime("%Y-%m-%d")
        else:
            date_str = str(latest_date)
        st.metric("📅 Latest Forecast Date", date_str)
    except Exception as e:
        st.error(f"Error displaying date: {str(e)}")
        st.metric("📅 Latest Forecast Date", "Error")

with col2:
    try:
        price_str = f"₹{latest_price:,.2f}"
        st.metric("📈 24KT Gold Price (Predicted)", price_str)
    except Exception as e:
        st.error(f"Error displaying price: {str(e)}")
        st.metric("📈 24KT Gold Price (Predicted)", "Error")

with col3:
    try:
        change_str = f"₹{daily_change:,.2f}"
        percent_str = f"{percent_change:.2f}%"
        st.metric("📊 1-Day Change", change_str, percent_str)
    except Exception as e:
        st.error(f"Error displaying change: {str(e)}")
        st.metric("📊 1-Day Change", "Error")

# Simple chart for now
st.markdown("### 📈 Gold Price Forecast – Next 7 Days")

try:
    next_7_days = df.head(7).copy()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=next_7_days["Date"], 
        y=next_7_days["Predicted_Price"], 
        mode="lines+markers", 
        name="Predicted Price", 
        line=dict(color="gold", width=4),
        marker=dict(size=10, color="gold")
    ))
    
    fig.update_layout(
        title="24KT Gold Price Forecast - Next 7 Days",
        xaxis_title="Date",
        yaxis_title="Price (INR per 10g)",
        template="plotly_dark",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
except Exception as e:
    st.error(f"❌ Error creating chart: {str(e)}")

# Show raw data for verification
st.markdown("### 📄 Raw Data (First 10 rows)")
st.dataframe(df.head(10))

st.markdown("---")
st.markdown("### ⚠️ If you're still seeing errors, please:")
st.write("1. Copy the debug information shown above")
st.write("2. Check that your CSV has 'Date' and 'Predicted_Price' columns")
st.write("3. Make sure the CSV file is in the same directory as your .py file")
st.write("4. Share the error message with the debug info")