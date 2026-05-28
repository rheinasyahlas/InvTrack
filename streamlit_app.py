import streamlit as st
import pandas as pd
import numpy as np

# --- Konfigurasi ---
SHERATON_PURPLE = '#5a189a'
hod_options = ['Administrative and General', 'Engineering', 'FB', 'Finance', 'Front Office', 'Housekeeping', 'Human Resources', 'Loss Prevention', 'Sales and Marketing']

def get_risk_level(aging):
    if aging <= 3: return 'Safe'
    elif aging <= 7: return 'Warning'
    return 'Critical'

# --- Inisialisasi Data ---
if 'master_df' not in st.session_state:
    np.random.seed(42)
    st.session_state.master_df = pd.DataFrame({
        'No. Invoice': [f'INV-000{i}' for i in range(1, 6)],
        'Supplier': ['PT Sentosa', 'CV Makmur', 'Sumber Rejeki', 'Karya Bersama', 'UD Jaya'],
        'Description': ['Bahan Baku Resto', 'Alat Kebersihan', 'Sparepart AC', 'ATK Kantor', 'Seragam Staff'],
        'Nilai': [5000000, 12000000, 800000, 25000000, 1500000],
        'Pemegang Dokumen (HOD)': ['Finance', 'Housekeeping', 'Engineering', 'FB', 'Sales and Marketing'],
        'Aging': [2, 8, 4, 10, 1]
    })
    st.session_state.master_df['Risk Level'] = st.session_state.master_df['Aging'].apply(get_risk_level)

# --- Tampilan ---
st.set_page_config(page_title='Sheraton Invoice Monitor')
st.markdown(f"<h1 style='color:{SHERATON_PURPLE};'>Sheraton Bandung Invoice Monitor</h1>", unsafe_allow_html=True)
st.dataframe(st.session_state.master_df)
st.write('File berhasil dibuat! Silakan download file ini dan requirements.txt untuk diunggah ke GitHub.')
