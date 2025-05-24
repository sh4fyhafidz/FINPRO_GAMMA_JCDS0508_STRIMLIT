import pandas as pd
import streamlit as st
import pickle
import requests
import os
import io

st.set_page_config(
    page_title="Used Cars SA Price Prediction",
    page_icon="🚗",
    layout="wide")

st.title("🚙 Predict Used Car Price")

# Load Model
model_url = "https://raw.githubusercontent.com/sh4fyhafidz/SHAFYHAFIDZ_ANALYSIS-SaaS-AWS_JCDS0508/main/Model_Saudi_Arabia_Used_Cars.sav"

try:
    response = requests.get(model_url)
    response.raise_for_status()
    model = pickle.load(io.BytesIO(response.content))
    st.success("✅ Model successfully loaded!")
except Exception as e:
    st.error(f"❌ Failed to load model: {str(e)}")

# Load dataset
data_url = "https://raw.githubusercontent.com/sh4fyhafidz/SHAFYHAFIDZ_ANALYSIS-SaaS-AWS_JCDS0508/main/Data_Clean.csv"

try:
    response = requests.get(data_url)
    response.raise_for_status()
    df = pd.read_csv(io.BytesIO(response.content))
    st.success("✅ Data successfully loaded!")
except Exception as e:
    st.error(f"❌ Failed to load data: {str(e)}")

columns_to_exclude = ['Origin', 'Negotiable']
df_filtered = df.drop(columns=columns_to_exclude, errors='ignore')

# Get unique values
unique_values = {col: df_filtered[col].dropna().unique().tolist() for col in df_filtered.columns}

def user_input_features():
    Make = st.selectbox("Select Make (Brand of Car)", options=unique_values['Make'])
    Type = st.selectbox("Select Type", options=unique_values['Type'])
    Color = st.selectbox("Select Car Color", options=unique_values['Color'])
    Fuel_Type = st.selectbox("Select Fuel Type", options=unique_values['Fuel_Type'])
    Gear_Type = st.radio('Choose Gear Type:', unique_values['Gear_Type'], horizontal=True)
    Options = st.radio('Choose Options:', unique_values['Options'], horizontal=True)
    Engine_Size = st.number_input('Fill Engine Size', min_value=min(unique_values['Engine_Size']), 
                                  max_value=max(unique_values['Engine_Size']), step=0.1, 
                                  value=min(unique_values['Engine_Size']))
    Year = st.selectbox("Select Year", options=unique_values['Year'])
    Mileage = st.number_input('Fill Mileage (KM)', min_value=0, max_value=max(unique_values['Mileage']), 
                              step=100, value=0)
    Region = st.selectbox("Select Region", options=unique_values['Region'])
    
    df_new = pd.DataFrame({
        'Make': [Make], 'Type': [Type], 'Year': [Year],
        'Color': [Color], 'Options': [Options], 'Engine_Size': [Engine_Size],
        'Fuel_Type': [Fuel_Type], 'Gear_Type': [Gear_Type], 'Mileage': [Mileage],
        'Region': [Region]
    })
    return df_new

# Get user input
df_customer = user_input_features()
if not df_customer.empty:
    price = model.predict(df_customer)

    # Display prediction
    st.markdown("<h3 style='text-align: center;'>Final Prediction</h3>", unsafe_allow_html=True)
    range_error = 18
    price_formatted = "{:,}".format(int(price[0]))
    price_down = "{:,}".format(int(price[0]) - int(price[0]) * range_error // 100)
    price_up = "{:,}".format(int(price[0]) + int(price[0]) * range_error // 100)
    price_commission = "{:,}".format(int(price[0]) * 5 // 100)
    monthly_installment = "{:,}".format(int(price[0]) // 47)

    st.markdown(f"<h1 style='text-align: center;'>SAR {price_formatted}</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"<p style='text-align: center;'>Estimation (±{range_error}%)</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>SAR {price_down} - {price_up}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Commission (5%): SAR {price_commission}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Monthly Installment (47 months): SAR {monthly_installment}</p>", unsafe_allow_html=True)
    st.markdown("---")

st.write("### Fill the Detail")
