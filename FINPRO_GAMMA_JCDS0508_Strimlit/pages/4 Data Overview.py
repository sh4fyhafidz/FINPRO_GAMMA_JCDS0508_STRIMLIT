import pandas as pd
import streamlit as st
import requests
import io

st.set_page_config(
    page_title="Used Cars SA Data Overview",
    page_icon="📊",
    layout="wide")

st.title("📊 Data Overview")
st.write('With this tool, you can see an overview of the dataset and the average of each column.')
st.markdown('---')

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
        
        required_columns = ['Make', 'Type', 'Year', 'Color', 'Options', 'Engine_Size', 'Fuel_Type', 'Gear_Type', 'Mileage', 'Region', 'Price']
        
        if all(col in data.columns for col in required_columns):
            st.sidebar.success(f"Dataset contains all required columns. Total rows: {data.shape[0]}")
            
            selection = st.selectbox('Choose what you want to see', ['Type', 'Region', 'Make', 'Gear Type', 'Options'])
            
            if selection == 'Type':
                st.subheader('Average Price by Type')
                result = data.groupby('Type')[['Price']].mean().reset_index().sort_values(by='Price', ascending=False)
            elif selection == 'Region':
                st.subheader('Average Price by Region')
                result = data.groupby('Region')[['Price']].mean().reset_index().sort_values(by='Price', ascending=False)
            elif selection == 'Make':
                st.subheader('Average Price by Make')
                result = data.groupby('Make')[['Price']].mean().reset_index().sort_values(by='Price', ascending=False)
            elif selection == 'Gear Type':
                st.subheader('Average Price by Gear Type')
                result = data.groupby('Gear_Type')[['Price']].mean().reset_index().sort_values(by='Price', ascending=False)
            elif selection == 'Options':
                st.subheader('Average Price by Options')
                result = data.groupby('Options')[['Price']].mean().reset_index().sort_values(by='Price', ascending=False)
            
            st.bar_chart(data=result, x=result.columns[0], y='Price', use_container_width=True)
            
            # Add download button for EDA result
            csv = result.to_csv(index=False)
            st.download_button(
                label="Download EDA Result",
                data=csv,
                file_name=f'EDA_{selection}.csv',
                mime='text/csv'
            )
        else:
            missing_cols = [col for col in required_columns if col not in data.columns]
            st.error(f"Your file is missing required columns: {', '.join(missing_cols)}")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
else:
    st.info("👈 Please upload your file first to start.")