import streamlit as st
import pandas as pd
import numpy as np

# --- Konfigurasi Estetika ---
SHERATON_PURPLE = '#5a189a'
hod_options = [
    'Administrative and General',
    'Engineering',
    'FB',
    'Finance',
    'Front Office',
    'Housekeeping',
    'Human Resources',
    'Loss Prevention',
    'Sales and Marketing'
]

hod_contacts = {
    'Administrative and General': 'Ms. Imelda Mangundap / Mr. Ahmad Samsul Arifin',
    'Engineering': 'Mr. Rojak Suryaman',
    'FB': 'Mr. Tri Julianto',
    'Finance': 'Mr. Nasrudin',
    'Front Office': 'Manager on Duty',
    'Housekeeping': 'Mr. Alamsyah Ramadhan',
    'Human Resources': 'Mr. Jaya Atmaja',
    'Loss Prevention': 'Mr. Dwiyanto',
    'Sales and Marketing': 'Ms. Virna Kiranjani'
}

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

# --- Tampilan Web ---
st.set_page_config(page_title="Sheraton Bandung - Invoice Monitor", layout="wide")
st.markdown(f"<h1 style='text-align: center; color: {SHERATON_PURPLE};'>🏨 Sheraton Bandung - Integrated Invoice Monitor</h1>", unsafe_allow_html=True)

# --- 1. DASHBOARD RINGKASAN ---
st.divider()
col1, col2, col3 = st.columns(3)
total_pending = len(st.session_state.master_df)
crit_count = st.session_state.master_df[st.session_state.master_df['Risk Level'] == 'Critical'].shape[0]

with col1:
    st.metric("Total Invoice Aktif", f"{total_pending} Dokumen")
with col2:
    st.metric("Invoice Kritis (>7 hari)", f"{crit_count} Dokumen", delta_color="inverse")
with col3:
    if not st.session_state.master_df.empty:
        top_hod = st.session_state.master_df.groupby('Pemegang Dokumen (HOD)')['Aging'].mean().idxmax()
        st.metric("Prioritas Follow-up", top_hod)

# --- 2. INPUT INVOICE ---
with st.expander("➕ Tambah Invoice Baru"):
    with st.form("entry_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            new_inv = st.text_input("Nomor Invoice")
            new_supp = st.text_input("Nama Supplier")
        with c2:
            new_val = st.number_input("Nilai (IDR)", min_value=0, step=1000)
            new_hod = st.selectbox("Departemen (HOD)", hod_options)
        new_desc = st.text_area("Keterangan/Description")
        if st.form_submit_button("Simpan ke Sistem"):
            if new_inv and new_supp:
                new_row = pd.DataFrame([{'No. Invoice': new_inv, 'Supplier': new_supp, 'Description': new_desc, 'Nilai': new_val, 'Pemegang Dokumen (HOD)': new_hod, 'Aging': 1, 'Risk Level': 'Safe'}])
                st.session_state.master_df = pd.concat([st.session_state.master_df, new_row], ignore_index=True)
                st.success(f"Invoice {new_inv} berhasil ditambahkan!")
                st.rerun()

# --- 3. SEARCH & FILTER ---
st.divider()
st.subheader("🔍 Pencarian & Filter")
f1, f2 = st.columns(2)
search_term = f1.text_input("Cari Supplier...")
dept_filter = f2.selectbox("Filter Departemen", ["Semua"] + hod_options)

# --- 4. MONITORING TABEL ---
st.subheader("📊 Daftar Monitor Invoice Aktif")
display_df = st.session_state.master_df.copy()
if search_term:
    display_df = display_df[display_df['Supplier'].str.contains(search_term, case=False)]
if dept_filter != "Semua":
    display_df = display_df[display_df['Pemegang Dokumen (HOD)'] == dept_filter]

if not display_df.empty:
    for i, row in display_df.iterrows():
        with st.container():
            col_a, col_b, col_c = st.columns([4, 2, 1])
            color = '#d90429' if row['Risk Level'] == 'Critical' else ('#ffb703' if row['Risk Level'] == 'Warning' else '#2a9d8f')
            col_a.markdown(f"**{row['No. Invoice']}** - {row['Supplier']}<br/><small>{row['Description']} | <b>Value: IDR {row['Nilai']:,.0f}</b></small>", unsafe_allow_html=True)
            col_b.markdown(f"Status: <span style='color:{color}; font-weight:bold;'>{row['Risk Level']}</span> ({row['Aging']} Hari)", unsafe_allow_html=True)
            if col_c.button("Selesai", key=f"done_{i}"):
                st.session_state.master_df = st.session_state.master_df.drop(i).reset_index(drop=True)
                st.rerun()
            st.divider()
else:
    st.info("Data tidak ditemukan atau semua tugas selesai.")

# --- 5. AUTO DISPATCHER ---
st.subheader("📧 Auto Dispatcher (Follow-up)")
if not st.session_state.master_df.empty:
    selected_invoices = st.multiselect("Pilih Invoice untuk Follow-up", st.session_state.master_df['No. Invoice'].tolist())
    if selected_invoices:
        sel_rows = st.session_state.master_df[st.session_state.master_df['No. Invoice'].isin(selected_invoices)]
        items_list = ""
        target_names = set()
        for _, r in sel_rows.iterrows():
            items_list += f"- {r['No. Invoice']} ({r['Supplier']}) | Aging: {r['Aging']} Hari\n"
            recipient = hod_contacts.get(r['Pemegang Dokumen (HOD)'], r['Pemegang Dokumen (HOD)'])
            target_names.add(recipient)
        
        recipients_str = " / ".join(target_names)
        draft = f"Subjek: [Follow-up] Dokumen Pending - Sheraton Bandung Apex\n\nDear {recipients_str},\n\nSemoga Bapak/Ibu dalam keadaan baik.\n\nMohon bantuannya untuk melakukan pengecekan pada invoice berikut yang masih pending di departemen Anda agar siklus finansial tetap berjalan lancar:\n\n{items_list}\nTerima kasih atas kerja samanya.\n\nSalam,\nFinance Operations"
        st.text_area("Draf Pesan:", draft, height=300)
