# Home.py
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Used Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #F0F8FF;
    }
    .main-header {
        font-size: 3rem;
        color: #4CAF50;
        text-align: center;
        margin: 2rem 0;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 2rem;
    }
    .description {
        font-size: 1.2rem;
        line-height: 1.6;
        color: #FFFFFF;
        text-align: justify;
        margin: 1rem auto;
        width: 80%;
    }
    .feature-box {
        background-color: #000000;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem auto;
        width: 80%;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .cta-button {
        display: block;
        width: fit-content;
        margin: 2rem auto;
        padding: 1rem 2rem;
        background-color: #4CAF50;
        color: white;
        text-align: center;
        font-size: 1.2rem;
        border-radius: 25px;
        text-decoration: none;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease;
    }
    .cta-button:hover {
        background-color: #45A049;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<h1 class="main-header">🚗 Welcome to the Used Car Price Predictor 🚗</h1>', unsafe_allow_html=True)

# Sub Header
st.markdown('<h2 class="sub-header">Predict the Selling Price of Used Cars on Syarah.com Using Machine Learning</h2>', unsafe_allow_html=True)

# Description
st.markdown("""
    <div class="description">
        The Used Car Price Predictor is a machine learning-based application designed to predict
        the selling price of used cars listed on Syarah.com. Using advanced data analysis and
        the CatBoost model, this tool helps users estimate the fair market price based on historical
        data and key vehicle attributes.
    </div>
""", unsafe_allow_html=True)

# Updated "How It Works" section with better contrast
st.markdown("""
    <div class="feature-box" style="background-color: #FFFFFF; color: black; border: 1px solid #B0BEC5;">
        <h3>🔍 How It Works:</h3>
        <ol style="line-height: 1.8;">
            <li><strong>Input Vehicle Data:</strong> Provide details such as make, model, year, mileage, and features.</li>
            <li><strong>Predict the Price:</strong> Use our pre-trained CatBoost machine learning model to estimate the selling price.</li>
            <li><strong>Analyze Results:</strong> Get an accurate price range and insights to make informed decisions.</li>
                    <li><strong>CatBoost Model:</strong> This machine learning model uses gradient boosting to handle categorical data efficiently and make accurate predictions.</li>
        </ol>
    </div>
""", unsafe_allow_html=True)

# Call to Action Button


# Footer
st.markdown("""
    <footer style="text-align:center; margin-top:3rem; font-size:0.9rem;">
        Machine Learning V.1, contact the operator if you encounter any issues ☎
    </footer>
""", unsafe_allow_html=True)
