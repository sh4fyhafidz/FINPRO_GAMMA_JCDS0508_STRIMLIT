import pandas as pd
import streamlit as st
import pickle
import requests
import io

st.set_page_config(
    page_title="Used Cars SA Batch Price Prediction",
    page_icon="🚗",
    layout="wide"
)

st.title("🚘 Predict Used Car Price for Batch Data")

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
columns_to_exclude = ['Origin', 'Negotiable']

# **Pastikan file uploader ada sebelum digunakan**
uploaded_file = st.sidebar.file_uploader(
    label="Upload your file",
    type=["csv"],
    help="Upload file format .csv only."
)

if uploaded_file is not None:
    st.sidebar.success(f"File '{uploaded_file.name}' successfully uploaded!")
    st.write("Here is a preview of your data:")

    try:
        data = pd.read_csv(uploaded_file, index_col=None)
        st.dataframe(data, height=125)

        required_columns = ['Make', 'Type', 'Year', 'Color', 'Options', 'Engine_Size', 'Fuel_Type', 'Gear_Type', 'Mileage', 'Region']

        if all(col in data.columns for col in required_columns):
            st.success(f"Dataset contains all required columns. Total rows: {data.shape[0]}")

            # Cek apakah data lebih dari 50 baris
            if data.shape[0] > 50:
                st.warning("⚠️ The uploaded file contains more than 50 rows. Only the first 50 rows will be processed.")
                data = data.iloc[:50]  # Hanya gunakan 50 baris pertama
            
            if st.button("Predict the Price"):
                predictions = model.predict(data[required_columns])
                data['Prediction'] = predictions.round().astype(int)

                st.write("Prediction Result:")
                st.dataframe(data[['Prediction']])

                csv = data.to_csv(index=False)
                st.download_button(
                    label="Download Prediction Result",
                    data=csv,
                    file_name='predictions.csv',
                    mime='text/csv'
                )
        else:
            missing_cols = [col for col in required_columns if col not in data.columns]
            st.error(f"Your file is missing required columns: {', '.join(missing_cols)}")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")

else:
    st.info("👈 Please upload your file first to start.")
