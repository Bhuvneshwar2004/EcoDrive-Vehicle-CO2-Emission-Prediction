# ==========================================
# CO2 Emission Prediction - College Project
# ==========================================

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
import joblib
import datetime

# Page Configuration
st.set_page_config(page_title="Vehicle CO2 Predictor", layout="wide")

# --- 1. DATA LOADING & PROCESSING (Cached) ---
@st.cache_data
def load_data():
    df = pd.read_csv('co2 Emissions.csv')
    
    # Renaming for Indian Context (Gasoline -> Petrol)
    fuel_mapping = {
        "Z": "Petrol (Premium)", 
        "X": "Petrol (Regular)", 
        "D": "Diesel", 
        "E": "Ethanol (E85)", 
        "N": "Natural Gas"
    }
    df["Fuel Type"] = df["Fuel Type"].map(fuel_mapping)
    
    # Dropping Natural Gas
    df = df[~df["Fuel Type"].str.contains("Natural Gas")].reset_index(drop=True)
    
    # Removing Outliers
    df_clean = df[['Engine Size(L)', 'Cylinders', 'Fuel Consumption Comb (L/100 km)', 'CO2 Emissions(g/km)']]
    df_model_data = df_clean[(np.abs(stats.zscore(df_clean)) < 1.9).all(axis=1)]
    
    return df, df_model_data

# --- 2. MODEL TRAINING & SAVING (Cached) ---
@st.cache_resource
def train_model(df):
    X = df[['Engine Size(L)', 'Cylinders', 'Fuel Consumption Comb (L/100 km)']]
    y = df['CO2 Emissions(g/km)']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # SAVE THE MODEL FILE (Silently saves to folder)
    joblib.dump(model, 'co2_model.pkl')
    
    return model

# Load Data and Model
df, df_model_data = load_data()
model = train_model(df_model_data)

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🚗 Project Menu")
menu = st.sidebar.radio(
    "Select an option:",
    ["Home", "Data Analysis (Graphs)", "Prediction System", "About Project"],
    index=0
)

# --- PAGE: HOME ---
if menu == "Home":
    st.title("🌱 CO2 Emission Prediction System")
    
    # Professional Introduction
    st.markdown("""
    ### 📝 Project Overview
    Welcome to the **Vehicle Emission Analysis** project. 
    
    This system uses **Machine Learning (Random Forest)** to predict the Carbon Dioxide (CO2) emissions of cars based on their engine parameters. 
    
    With rising concerns about Global Warming and stricter norms like **BS-VI**, understanding vehicle emissions is crucial for a sustainable future.
    """)

    # Objectives
    st.markdown("""
    ### 🎯 Objectives
    * **Analyze:** Study how Engine Size, Cylinders, and Mileage affect pollution.
    * **Predict:** Estimate CO2 output (g/km) for any car.
    * **Awareness:** Differentiate between Eco-friendly and High-Emission vehicles.
    """)

    st.image("home_image.png", caption="Sustainable Transport", use_container_width=True)

    # Student Details
    st.info("""
    **👨‍🎓 Project Developed By:** **Name:** Bhuvneshwar Sahu  
    **Batch:** 2022-26  
    **Department:** Computer Science & Engineering  
    **Institute:** Government Engineering College, Raipur
    """)

# --- PAGE: DATA ANALYSIS ---
elif menu == "Data Analysis (Graphs)":
    st.title("📊 Data Analysis & Visualization")
    
    if st.checkbox("Show Raw Dataset"):
        st.write(df.head(10))
        st.write(f"**Total Records:** {df.shape[0]}")

    st.markdown("---")
    
    # Graph 1
    st.subheader("1. Which Fuel Type is most common?")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.countplot(x='Fuel Type', data=df, palette="viridis", ax=ax1)
    plt.xticks(rotation=45)
    st.pyplot(fig1)
    
    # Graph 2
    st.subheader("2. Engine Size vs. CO2 Emission")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x='Engine Size(L)', y='CO2 Emissions(g/km)', hue='Fuel Type', data=df, ax=ax2)
    st.pyplot(fig2)

# --- PAGE: PREDICTION SYSTEM ---
elif menu == "Prediction System":
    st.title("🚀 Predict Emission")
    st.markdown("Enter the vehicle details below to estimate the CO2 output.")

    # Car Identity
    st.subheader("1. Car Identity (Optional)")
    col_id1, col_id2 = st.columns(2)
    with col_id1:
        car_brand = st.text_input("Car Brand", placeholder="e.g. Maruti, Tata")
    with col_id2:
        car_model = st.text_input("Car Model Name", placeholder="e.g. Swift, Nexon")

    st.markdown("---")
    
    # Technical Specs
    st.subheader("2. Technical Specifications")
    col1, col2 = st.columns(2)

    with col1:
        engine_size = st.number_input("Engine Size (Litres)", min_value=0.5, max_value=10.0, value=2.0, step=0.1)
        cylinders = st.slider("Number of Cylinders", min_value=2, max_value=16, value=4)

    with col2:
        # INDIAN CONTEXT: Mileage
        mileage_kml = st.number_input("Mileage (km per Litre)", min_value=1.0, max_value=50.0, value=15.0, step=0.5)
        # Convert to L/100km
        fuel_consumption_l100 = 100 / mileage_kml
        st.caption(f"Calculated Fuel Consumption: {fuel_consumption_l100:.2f} L/100km")

    # Predict Button
    if st.button("Predict CO2 Emission", type="primary"):
        input_data = [[engine_size, cylinders, fuel_consumption_l100]]
        prediction = model.predict(input_data)[0]
        
        # Determine Status
        status = "Low/Moderate Emission" if prediction < 200 else "High Emission"
        status_icon = "✅" if prediction < 200 else "⚠️"
        
        st.markdown("### 📝 Prediction Report")
        
        car_name_display = f"{car_brand} {car_model}" if car_brand or car_model else "Vehicle"
        
        st.success(f"**{car_name_display}** Estimated Emission: **{prediction:.2f} g/km**")
        
        if prediction < 200:
            st.info(f"{status_icon} This is a {status} Vehicle.")
        else:
            st.warning(f"{status_icon} This is a {status} Vehicle.")

        # --- GENERATE REPORT TEXT ---
        report_text = f"""
==================================================
        VEHICLE CO2 EMISSION REPORT
==================================================
Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

--- CAR IDENTITY ---
Brand: {car_brand if car_brand else "N/A"}
Model: {car_model if car_model else "N/A"}

--- TECHNICAL SPECIFICATIONS ---
Engine Size: {engine_size} L
Cylinders: {cylinders}
Mileage: {mileage_kml} km/L
Calculated Fuel Cons.: {fuel_consumption_l100:.2f} L/100km

--- PREDICTION RESULT ---
Estimated CO2 Emission: {prediction:.2f} g/km
Emission Status: {status}

==================================================
Generated by CO2 Prediction System
==================================================
        """
        
        # --- DOWNLOAD BUTTON FOR REPORT ---
        st.download_button(
            label="📄 Download Prediction Report",
            data=report_text,
            file_name=f"CO2_Report_{car_brand}_{car_model}.txt",
            mime="text/plain"
        )

# --- PAGE: ABOUT ---
elif menu == "About Project":
    st.title("ℹ️ About")
    st.markdown("""
    ### College Project Details
    **Project Title:** CO2 Emission Prediction by Vehicle  
    **Developed By:** Bhuvneshwar Sahu  
    **Batch:** 2022-26  
    **Department:** Computer Science & Engineering  
    
    **Dataset Source:** Government of Canada - Open Data Portal.
    
    **Description:**
    This tool helps users understand the environmental impact of vehicles based on technical specifications.
    """)