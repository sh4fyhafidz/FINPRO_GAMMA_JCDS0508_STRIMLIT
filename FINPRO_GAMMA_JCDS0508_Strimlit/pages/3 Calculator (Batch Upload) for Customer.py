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

model_url = "https://raw.githubusercontent.com/sh4fyhafidz/SHAFYHAFIDZ_ANALYSIS-SaaS-AWS_JCDS0508/main/Model_Saudi_Arabia_Used_Cars.sav"

try:
    response = requests.get(model_url)
    response.raise_for_status()
    model = pickle.load(io.BytesIO(response.content))
    st.success("✅ Model successfully loaded!")
except Exception as e:
    st.error(f"❌ Failed to load model: {str(e)}")

required_columns = ['Make', 'Type', 'Year', 'Color', 'Options', 'Engine_Size', 'Fuel_Type', 'Gear_Type', 'Mileage', 'Region']

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
        
        data = data[required_columns] if all(col in data.columns for col in required_columns) else data.filter(items=required_columns)
        
        st.dataframe(data, height=125)
        st.success(f"Dataset processed with required columns. Total rows: {data.shape[0]}")
        
        if data.shape[0] > 50:
            st.warning("⚠️ The uploaded file contains more than 50 rows. Only the first 50 rows will be processed.")
            data = data.iloc[:50]
        
        if st.button("Predict the Price"):
            predictions = model.predict(data)
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
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("👈 Please upload your file first to start.")
