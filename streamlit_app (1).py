import streamlit as st
import pandas as pd
import numpy as np

# --- Aesthetic Configuration ---
BRAND_COLOR = '#5a189a'
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

# --- Data Initialization ---
if 'master_df' not in st.session_state:
    np.random.seed(42)
    st.session_state.master_df = pd.DataFrame({
        'No. Invoice': [f'INV-000{i}' for i in range(1, 6)],
        'Supplier': ['PT Sentosa', 'CV Makmur', 'Sumber Rejeki', 'Karya Bersama', 'UD Jaya'],
        'Description': ['Resto Raw Materials', 'Cleaning Tools', 'AC Spareparts', 'Office Stationery', 'Staff Uniforms'],
        'Nilai': [5000000, 12000000, 800000, 25000000, 1500000],
        'Pemegang Dokumen (HOD)': ['Finance', 'Housekeeping', 'Engineering', 'FB', 'Sales and Marketing'],
        'Aging': [2, 8, 4, 10, 1]
    })
    st.session_state.master_df['Risk Level'] = st.session_state.master_df['Aging'].apply(get_risk_level)

# --- Web UI ---
st.set_page_config(page_title="InvMon - Invoice Monitor", layout="wide")
st.markdown(f"<h1 style='text-align: center; color: {BRAND_COLOR};'>📊 InvMon - Integrated Invoice Monitor</h1>", unsafe_allow_html=True)

# --- 1. DASHBOARD SUMMARY ---
st.divider()
col1, col2, col3 = st.columns(3)
total_pending = len(st.session_state.master_df)
crit_count = st.session_state.master_df[st.session_state.master_df['Risk Level'] == 'Critical'].shape[0]

with col1:
    st.metric("Active Invoices", f"{total_pending} Documents")
with col2:
    st.metric("Critical Invoices (>7 days)", f"{crit_count} Documents", delta_color="inverse")
with col3:
    if not st.session_state.master_df.empty:
        top_hod = st.session_state.master_df.groupby('Pemegang Dokumen (HOD)')['Aging'].mean().idxmax()
        st.metric("Follow-up Priority", top_hod)

# --- 2. INVOICE ENTRY ---
with st.expander("➕ Add New Invoice"):
    with st.form("entry_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            new_inv = st.text_input("Invoice Number")
            new_supp = st.text_input("Supplier Name")
        with c2:
            new_val = st.number_input("Value (IDR)", min_value=0, step=1000)
            new_hod = st.selectbox("Department", hod_options)
        new_desc = st.text_area("Description")
        if st.form_submit_button("Save to System"):
            if new_inv and new_supp:
                new_row = pd.DataFrame([{'No. Invoice': new_inv, 'Supplier': new_supp, 'Description': new_desc, 'Nilai': new_val, 'Pemegang Dokumen (HOD)': new_hod, 'Aging': 1, 'Risk Level': 'Safe'}])
                st.session_state.master_df = pd.concat([st.session_state.master_df, new_row], ignore_index=True)
                st.success(f"Invoice {new_inv} successfully added!")
                st.rerun()

# --- 3. SEARCH & FILTER ---
st.divider()
st.subheader("🔍 Search & Filter")
f1, f2 = st.columns(2)
search_term = f1.text_input("Search Supplier...")
dept_filter = f2.selectbox("Filter Department", ["All"] + hod_options)

# --- 4. MONITORING TABLE ---
st.subheader("📊 Active Invoice Monitor")
display_df = st.session_state.master_df.copy()
if search_term:
    display_df = display_df[display_df['Supplier'].str.contains(search_term, case=False)]
if dept_filter != "All":
    display_df = display_df[display_df['Pemegang Dokumen (HOD)'] == dept_filter]

if not display_df.empty:
    for i, row in display_df.iterrows():
        with st.container():
            col_a, col_b, col_c = st.columns([4, 2, 1])
            color = '#d90429' if row['Risk Level'] == 'Critical' else ('#ffb703' if row['Risk Level'] == 'Warning' else '#2a9d8f')
            col_a.markdown(f"**{row['No. Invoice']}** - {row['Supplier']}<br/><small>{row['Description']} | <b>Department: {row['Pemegang Dokumen (HOD)']} | Value: IDR {row['Nilai']:,.0f}</b></small>", unsafe_allow_html=True)
            col_b.markdown(f"Status: <span style='color:{color}; font-weight:bold;'>{row['Risk Level']}</span> ({row['Aging']} Days)", unsafe_allow_html=True)
            if col_c.button("Mark Done", key=f"done_{i}"):
                st.session_state.master_df = st.session_state.master_df.drop(i).reset_index(drop=True)
                st.rerun()
            st.divider()
else:
    st.info("No data found or all tasks completed.")

# --- 5. AUTO DISPATCHER ---
st.subheader("📧 Auto Dispatcher (Follow-up)")
if not st.session_state.master_df.empty:
    selected_invoices = st.multiselect("Select Invoices for Follow-up", st.session_state.master_df['No. Invoice'].tolist())
    if selected_invoices:
        sel_rows = st.session_state.master_df[st.session_state.master_df['No. Invoice'].isin(selected_invoices)]
        items_list = ""
        target_names = set()
        for _, r in sel_rows.iterrows():
            items_list += f"- {r['No. Invoice']} ({r['Supplier']}) | Aging: {r['Aging']} Days\n"
            recipient = hod_contacts.get(r['Pemegang Dokumen (HOD)'], r['Pemegang Dokumen (HOD)'])
            target_names.add(recipient)

        recipients_str = " / ".join(target_names)
        draft = f"Subject: Pending Document Follow-up\n\nDear {recipients_str},\n\nGreetings from the Finance Team! I hope you are having a wonderful day.\n\nAs we strive for operational excellence, could you kindly assist us in reviewing the following pending invoices currently held by your department? Your support in ensuring these documents are validated will help us maintain our smooth financial workflow:\n\n{items_list}\nThank you very much for your time and kind cooperation. We truly appreciate everything you do.\n\nBest regards,\nAccount Payable"
        st.text_area("Message Draft:", draft, height=350)
