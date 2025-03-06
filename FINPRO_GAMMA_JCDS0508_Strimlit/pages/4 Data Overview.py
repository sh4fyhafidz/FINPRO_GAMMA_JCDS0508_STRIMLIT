import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Used Cars SA Data Overview",
    page_icon="📊",
    layout="wide")

st.title("📊 Data Overview")
st.write("Below is an interactive dashboard for further insights:")

tableau_url = "https://public.tableau.com/views/UsedCarDashboard_17410944222040/Dashboard2?:showVizHome=no&:embed=true"

components.html(
    f'<iframe src="{tableau_url}" width="100%" height="600"></iframe>',
    height=600
)
