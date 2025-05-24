import pandas as pd
import streamlit as st
import pickle
import requests
import io

st.set_page_config(
    page_title="Telco Customer Churn Prediction",
    page_icon="📱",
    layout="wide"
)

st.title("📱 Telco Customer Churn Prediction (Batch)")

# Load Model
model_url = "https://raw.githubusercontent.com/sh4fyhafidz/SHAFYHAFIDZ_ANALYSIS-SaaS-AWS_JCDS0508/main/Model_Saudi_Arabia_Used_Cars.sav"

try:
    response = requests.get(model_url)
    response.raise_for_status()
    model = pickle.load(io.BytesIO(response.content))
    st.success("✅ Model successfully loaded!")
except Exception as e:
    st.error(f"❌ Failed to load model: {str(e)}")

# Upload file
uploaded_file = st.sidebar.file_uploader("📤 Upload file CSV", type=["csv"])
min_tenure = st.sidebar.number_input("🔢 Minimal Tenure (bulan):", min_value=0, value=10)

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)

        # Simpan Churn asli jika ada
        true_churn = data['Churn'] if 'Churn' in data.columns else None

        # Tampilkan preview awal
        st.write("📊 Data Upload Preview:")
        st.dataframe(data.head())

        # Filter berdasarkan tenure
        filtered_data = data[data['tenure'] >= min_tenure].copy()
        st.write(f"📋 {filtered_data.shape[0]} data dengan tenure ≥ {min_tenure} ditemukan.")

        # Simpan Churn asli untuk data terfilter (jika ada)
        if true_churn is not None:
            churn_actual = true_churn.loc[filtered_data.index].values
        else:
            churn_actual = None

        # Hapus kolom target sebelum prediksi
        if 'Churn' in filtered_data.columns:
            filtered_data = filtered_data.drop(columns=['Churn'])

        if st.button("🔮 Prediksi Churn"):
            if model:
                pred = model.predict(filtered_data)
                proba = model.predict_proba(filtered_data)[:, 1]

                # Tambahkan hasil prediksi
                filtered_data['Churn_Predicted'] = pred
                filtered_data['Proba_Churn'] = (proba * 100).round(2).astype(str) + '%'
                filtered_data['Proba_Numeric'] = proba  # untuk pengurutan

                # Urutkan berdasarkan probabilitas tertinggi
                filtered_data = filtered_data.sort_values(by='Proba_Numeric', ascending=False)

                # Tambahkan kolom actual jika tersedia
                if churn_actual is not None:
                    filtered_data['Churn_Actual'] = churn_actual

                # Kolom yang ingin ditampilkan
                display_cols = ['customerID', 'tenure', 'Churn_Predicted', 'Proba_Churn']
                if churn_actual is not None:
                    display_cols.append('Churn_Actual')

                st.success("✅ Prediksi berhasil dilakukan!")
                st.dataframe(filtered_data[display_cols])

                # Download CSV (tanpa kolom numeric)
                csv = filtered_data.drop(columns=['Proba_Numeric']).to_csv(index=False)
                st.download_button(
                    label="📥 Download Hasil Prediksi",
                    data=csv,
                    file_name="hasil_prediksi_churn.csv",
                    mime="text/csv"
                )
            else:
                st.warning("⚠️ Model belum dimuat.")
    except Exception as e:
        st.error(f"❌ Error saat membaca atau memproses data: {e}")
else:
    st.info("👈 Upload file CSV kamu untuk memulai prediksi.")
