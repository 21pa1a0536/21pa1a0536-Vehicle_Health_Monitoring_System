import streamlit as st
import plotly.graph_objects as go

# Helper to create a gauge chart
def create_gauge(title, value, min_val, max_val, safe_range, warn_range, reverse=False):
    if reverse:
        color = (
            "green" if value >= safe_range[0]
            else "orange" if value >= warn_range[0]
            else "red"
        )
    else:
        color = (
            "green" if value <= safe_range[1]
            else "orange" if value <= warn_range[1]
            else "red"
        )
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': color},
            'steps': [
                {'range': safe_range, 'color': "lightgreen"},
                {'range': warn_range, 'color': "yellow"},
                {'range': [min_val, warn_range[0]] if reverse else [warn_range[1], max_val], 'color': "tomato"}
            ]
        }
    ))
    return fig

# Function to generate health alerts
def check_health(data):
    alerts = []

    if data["engine_temp"] > 100:
        alerts.append(f"High Engine Temperature: {data['engine_temp']}°C")
    if data["battery_voltage"] < 12:
        alerts.append(f"Low Battery Voltage: {data['battery_voltage']}V")
    if data["rpm"] > 5000:
        alerts.append(f"High Engine RPM: {data['rpm']}")
    if data["brake_fluid"] < 50:
        alerts.append(f"Low Brake Fluid Level: {data['brake_fluid']}%")

    return alerts

# Streamlit UI
st.set_page_config(page_title="Vehicle Health Dashboard", layout="wide")
st.title("Vehicle Health Monitoring Dashboard")

# Sidebar Inputs
st.sidebar.header("Input Vehicle Sensor Values")
engine_temp = st.sidebar.number_input("Engine Temperature (°C)", min_value=0, max_value=200, value=90)
battery_voltage = st.sidebar.number_input("Battery Voltage (V)", min_value=0.0, max_value=20.0, value=12.5, step=0.1)
rpm = st.sidebar.number_input("Engine RPM", min_value=0, max_value=8000, value=2000)
brake_fluid = st.sidebar.slider("Brake Fluid Level (%)", min_value=0, max_value=100, value=75)

# Data collection
sensor_data = {
    "engine_temp": engine_temp,
    "battery_voltage": battery_voltage,
    "rpm": rpm,
    "brake_fluid": brake_fluid
}

alerts = check_health(sensor_data)

# Gauges
st.subheader("System Health Gauges")
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(create_gauge("Engine Temp (°C)", engine_temp, 0, 150, (0, 90), (90, 100)), use_container_width=True)
    st.plotly_chart(create_gauge("Engine RPM", rpm, 0, 8000, (0, 4000), (4000, 5000)), use_container_width=True)

with col2:
    st.plotly_chart(create_gauge("Battery Voltage (V)", battery_voltage, 0, 20, (12, 14), (11.5, 12), reverse=True), use_container_width=True)
    st.plotly_chart(create_gauge("Brake Fluid (%)", brake_fluid, 0, 100, (60, 100), (50, 60), reverse=True), use_container_width=True)

# Alerts section
st.subheader("Status Report")
if alerts:
    st.error("Issues Detected:")
    for alert in alerts:
        st.markdown(f"- {alert}")
else:
    st.success("All systems are functioning within safe ranges.")
