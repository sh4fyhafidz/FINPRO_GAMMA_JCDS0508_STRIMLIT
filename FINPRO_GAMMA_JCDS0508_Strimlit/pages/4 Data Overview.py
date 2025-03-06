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

# Embed Tableau Dashboard
st.markdown("## 📈 Interactive Dashboard")
st.write("Below is an interactive dashboard for further insights:")
st.markdown(
    """
    <iframe src="https://public.tableau.com/views/UsedCarDashboard_17410944222040/Dashboard2?:showVizHome=no&:embed=true"
    width="100%" height="600" style="border: none;"></iframe>
    """,
    unsafe_allow_html=True
)
