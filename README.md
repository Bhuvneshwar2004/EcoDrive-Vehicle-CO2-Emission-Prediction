```markdown
# 🚗 Vehicle CO2 Emission Prediction System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Machine Learning](https://img.shields.io/badge/ML-Random%20Forest-green)

## 📝 Project Overview

The **Vehicle CO2 Emission Prediction System** is a Machine Learning-based web application designed to estimate the carbon footprint of cars based on their engine specifications.

With rising environmental concerns and stricter regulations like **BS-VI norms in India**, this tool helps users understand the environmental impact of their vehicles. It uses the **Random Forest Regressor** algorithm to provide accurate emission predictions.

### 🎯 Key Objectives
- **Analyze:** Visualize the relationship between Engine Size, Cylinders, and CO2 emissions.
- **Predict:** Estimate CO2 output (g/km) for any vehicle using technical data.
- **Awareness:** Help users differentiate between Eco-friendly and High-Emission vehicles.

---

## ✨ Key Features

- **🇮🇳 Indian Context Logic:**
  - Includes a **Mileage Converter** that automatically converts **km/L** (Indian standard) to **L/100km** (International standard) for the model.
  - References **BS-VI** compliance in the project context.
- **📊 Interactive Dashboard:**
  - Data visualizations using Bar Charts and Scatter Plots.
  - User-friendly Sidebar navigation.
- **📄 Downloadable Reports:**
  - Generates a text file report containing the car's identity, technical specs, and prediction result for documentation.
- **🤖 Machine Learning:**
  - Uses a trained **Random Forest** model saved as `co2_model.pkl` for fast predictions without retraining.

---

## 🛠️ Tech Stack

- **Language:** Python
- **Frontend Framework:** Streamlit
- **Machine Learning:** Scikit-Learn (Random Forest Regressor)
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Model Persistence:** Joblib

---

## 🚀 How to Run the Project

### Prerequisites
Make sure you have **Python** installed on your system.

### Step 1: Install Dependencies
Open your terminal (Command Prompt) in the project folder and run:
```bash
pip install -r requirements.txt

```

### Step 2: Run the Application

Execute the following command to start the web app:

```bash
streamlit run app.py

```

### Step 3: Access the App

The application will automatically open in your default web browser at:
`http://localhost:8501`

---

## 🔮 Future Scope

* **Cloud Deployment:** Deploying the app on Streamlit Cloud for public access.
* **Real-time Database:** Integrating a database to store user prediction history.
* **Mobile App:** Converting the web logic into a mobile application.

---

## 👨‍🎓 Developer Info

**Developed By:** Bhuvneshwar Sahu

**Batch:** 2022-2026

**Department:** Computer Science & Engineering

**Institute:** Government Engineering College, Raipur (C.G.)

---

> *This project was developed as part of the Vocational Training (VT) program.*
