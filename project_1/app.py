import streamlit as st
import requests
import pandas as pd
import time
import plotly.express as px
import logging

# ----------------- Logging Setup ----------------- #
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('app.log')
console_handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ----------------- Streamlit UI ----------------- #
st.set_page_config(page_title="Smart Vehicle Detection System", layout="wide", page_icon="🚗")

# Custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .title {
            color: #2c3e50;
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
        .description {
            color: #34495e;
            font-size: 18px;
            text-align: center;
            margin-bottom: 30px;
        }
        .footer {
            background-color: #2c3e50;
            color: white;
            padding: 10px;
            text-align: center;
        }
        .notification {
            background-color: #e8f8f5;
            border-left: 6px solid #1abc9c;
            padding: 10px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🚦 Navigation")
option = st.sidebar.radio("Choose an option:", ["Home", "Upload Image", "Upload CSV", "Statistics"])

# Notification log
notification_log = []

# ----------------- Page Logic ----------------- #

# Home
if option == "Home":
    st.image(r"C:\Users\TARANI\OneDrive\Desktop\app\dash.png", use_container_width=True)
    st.markdown("""
    ### Key Features:
    - Upload vehicle images for detection.
    - Process CSV files with bulk data.
    - Get real-time notifications for authorities.
    """)
    st.markdown("🔧 **Built with FastAPI and Streamlit.**")
    logger.info('Home page loaded')

# Upload Image
elif option == "Upload Image":
    st.header("📸 Upload Vehicle Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        st.markdown("Processing...")
        with st.spinner("Analyzing the image..."):
            try:
                files = {"file": uploaded_file.getvalue()}
                response = requests.post("http://localhost:8000/recognize", files=files)
                if response.status_code == 200:
                    result = response.json()
                    vehicle_info = f"Vehicle Detected: {result['license_plate']}"
                    notification_log.append(vehicle_info)
                    st.success(vehicle_info)
                    time.sleep(1)
                    st.balloons()
                    st.markdown(
                        f'<div class="notification">Notification sent to traffic police about {vehicle_info}.</div>',
                        unsafe_allow_html=True
                    )
                    logger.info(f'Image processed successfully: {vehicle_info}')
                else:
                    st.error("Error: Unable to process the image.")
                    logger.error('Error processing image')
            except Exception as e:
                st.error("Exception occurred while processing.")
                logger.exception("Exception in Upload Image section")

# Upload CSV
elif option == "Upload CSV":
    st.header("📄 Upload Vehicle Data (CSV)")
    uploaded_file = st.file_uploader("Choose a CSV file...", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("### Uploaded Data")
            st.dataframe(df)

            st.write("### Data Summary")
            st.write(df.describe())

            if "Speed" in df.columns:
                fig = px.histogram(df, x="Speed", nbins=20, title="Speed Distribution of Vehicles")
                st.plotly_chart(fig)
            logger.info('CSV data processed successfully')
        except Exception as e:
            st.error("Failed to process CSV file.")
            logger.exception("Exception in Upload CSV section")

# Statistics
elif option == "Statistics":
    st.header("📊 Real-Time Statistics")
    st.write("🚘 Vehicles Processed: ", 55)
    st.write("📤 Notifications Sent: ", 16)

    speed_data = [50, 60, 70, 55, 80, 75, 65, 90]
    fig = px.line(y=speed_data, x=range(len(speed_data)), title="Vehicle Speed Over Time")
    st.plotly_chart(fig)
    logger.info('Statistics page loaded')

# Footer
st.markdown("""
<div class="footer">
    <p>© 2024 Smart Vehicle Detection System and Enforcement System</p>
    <p>Contact: <a href="mailto:support@smartdetection.com" style="color:white;">support@smartdetection.com</a></p>
</div>
""", unsafe_allow_html=True)
