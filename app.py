import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Seoul Bike Demand Prediction",
    page_icon="🚲",
    layout="wide"
)

@st.cache_resource
def load_model():
    model = joblib.load("bike_demand_model.pkl")
    return model

model = load_model()

st.title("Seoul Bike Demand Prediction")

st.write("""
Predict the expected number of rented bikes based on weather,
season, holiday, and time details.
""")

st.sidebar.header("Enter Input Details")

hour = st.sidebar.slider("Hour", 0, 23, 18)
temperature = st.sidebar.slider("Temperature", -20.0, 45.0, 25.0)
humidity = st.sidebar.slider("Humidity", 0, 100, 60)
wind_speed = st.sidebar.slider("Wind Speed", 0.0, 10.0, 2.5)
visibility = st.sidebar.slider("Visibility", 0, 2500, 1500)
dew_point_temperature = st.sidebar.slider("Dew Point Temperature", -30.0, 30.0, 15.0)
solar_radiation = st.sidebar.slider("Solar Radiation", 0.0, 5.0, 0.8)
rainfall = st.sidebar.slider("Rainfall", 0.0, 50.0, 0.0)
snowfall = st.sidebar.slider("Snowfall", 0.0, 10.0, 0.0)

season = st.sidebar.selectbox(
    "Season",
    ["Spring", "Summer", "Autumn", "Winter"]
)

holiday = st.sidebar.selectbox(
    "Holiday",
    ["No Holiday", "Holiday"]
)

day = st.sidebar.slider("Day", 1, 31, 15)
month = st.sidebar.slider("Month", 1, 12, 7)
year = st.sidebar.selectbox("Year", [2017, 2018])

day_of_week = st.sidebar.selectbox(
    "Day of Week",
    [0, 1, 2, 3, 4, 5, 6],
    format_func=lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][x]
)

is_weekend = 1 if day_of_week >= 5 else 0

input_data = pd.DataFrame({
    "hour": [hour],
    "temperature": [temperature],
    "humidity": [humidity],
    "wind_speed": [wind_speed],
    "visibility": [visibility],
    "dew_point_temperature": [dew_point_temperature],
    "solar_radiation": [solar_radiation],
    "rainfall": [rainfall],
    "snowfall": [snowfall],
    "season": [season],
    "holiday": [holiday],
    "day": [day],
    "month": [month],
    "year": [year],
    "day_of_week": [day_of_week],
    "is_weekend": [is_weekend]
})

st.subheader("Input Data")
st.dataframe(input_data)

if st.button("Predict Bike Demand"):
    prediction = model.predict(input_data)
    predicted_count = int(prediction[0])

    st.success(f"Predicted Rented Bike Count: {predicted_count}")

    if predicted_count < 300:
        st.info("Demand Level: Low")
    elif predicted_count < 1000:
        st.warning("Demand Level: Medium")
    else:
        st.error("Demand Level: High")