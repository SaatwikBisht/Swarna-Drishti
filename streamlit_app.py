import streamlit as st
import pandas as pd

st.title("Gold Price App - Debug Version")

# Step 1: Load and check the CSV
st.write("Loading CSV...")
try:
    df = pd.read_csv("forecast.csv")
    st.success("✅ CSV loaded successfully!")
    st.write("CSV shape:", df.shape)
    st.write("CSV columns:", df.columns.tolist())
    st.write("First 3 rows:")
    st.write(df.head(3))
except Exception as e:
    st.error(f"❌ Error loading CSV: {e}")
    st.stop()

# Step 2: Convert dates
st.write("Converting dates...")
try:
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
    st.success("✅ Date conversion successful!")
except Exception as e:
    st.error(f"❌ Error converting dates: {e}")
    st.stop()

# Step 3: Get latest data
st.write("Getting latest data...")
try:
    latest_row = df.iloc[-1]
    latest_date = latest_row["Date"]
    latest_price = latest_row["Predicted_Price"]
    st.success("✅ Latest data retrieved!")
    st.write(f"Latest date: {latest_date}")
    st.write(f"Latest price: {latest_price}")
except Exception as e:
    st.error(f"❌ Error getting latest data: {e}")
    st.stop()

# Step 4: Display metrics (the part that was failing)
st.write("Displaying metrics...")
try:
    date_string = latest_date.strftime("%d-%m-%Y")
    price_string = f"₹{latest_price:,.2f}"
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📅 Date", date_string)
    with col2:
        st.metric("💰 Price", price_string)
    
    st.success("✅ Metrics displayed successfully!")
except Exception as e:
    st.error(f"❌ Error displaying metrics: {e}")
    st.write(f"Error details: {type(e).__name__}: {str(e)}")

st.write("---")
st.write("If you see this message, the basic functionality is working!")
st.write("Next step: Replace with full app code.")