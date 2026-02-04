import streamlit as st
import datetime
import pytz
import base64
import os
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'analisa_type' not in st.session_state:
    st.session_state.analisa_type = None

# --- 2. FUNGSI DATABASE EXCEL (FIXED) ---
def kirim_ke_excel(jam, brix=None, pol=None, tsai=None, od=None):
    try:
        # Ambil data dari secrets ke dalam dictionary baru (biar bisa dimodifikasi)
        info_kredensial = dict(st.secrets["gcp_service_account"])
        
        # Perbaikan karakter newline di private_key (Solusi error PEM file)
        info_kredensial["private_key"] = info_kredensial["private_key"].replace("\\n", "\n")
        
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(info_kredensial, scopes=scope)
        client = gspread.authorize(creds)
        
        # ID Spreadsheet dari URL lo
        sheet = client.open_by_key("1yQ2DbMy0ip_du1gqJ16jWwaWK8Psv6AB").worksheet("INPUT")

        # LOGIKA BARIS (Jam 06:00 = Baris 270)
        # Sesuai image_25a14e.png lo beb
        if jam >= 6:
            baris = 270 + (jam - 6)
        else: # Jam 00:00 - 05:00
            baris = 270 + (jam + 18)

        # Update Kolom Tetes: O(Brix), P(Pol), Q(TSAI), R(OD)
        if brix is not None: sheet.update_acell(f"O{baris}", str(round(brix, 2)))
        if pol is not None: sheet.update_acell(f"P{baris}", str(round(pol, 2)))
        if tsai is not None: sheet.update_acell(f"Q{baris}", str(round(tsai, 2)))
        if od is not None: sheet.update_acell(f"R{baris}", str(round(od, 2)))
        
        return True
    except Exception as e:
        st.error(f"❌ Gagal Kirim ke Excel: {e}")
        return False

# --- 3. DATABASE INTERPOLASI (TETAP) ---
data_koreksi = {27:-0.05, 28:0.02, 29:0.09, 30:0.16, 31:0.24, 32:0.315, 33:0.385, 34:0.465, 35:0.54, 36:0.62, 37:0.70, 38:0.78, 39:0.86, 40:0.94}
data_bj = {0.0:0.9964, 5.0:1.01592, 10.0:1.03608, 15.0:1.05691, 20.0:1.07844, 25.0:1.10069, 30.0:1.12368, 35.0:1.14745, 40.0:1.17203, 45.0:1.19746, 49.0:1.21839, 50.0:1.22372, 55.0:1.25083, 60.0:1.27885, 65.0:1.30781, 70.0:1.33775}
data_tsai = {15.0:336.0, 20.0:254.5, 25.0:204.8, 30.0:171.7, 35.0:147.9, 37.7:136.67}

def hitung_interpolasi(nilai_user, dataset):
    keys = sorted(dataset.keys())
    if nilai_user in dataset: return dataset[nilai_user]
    if nilai_user < keys[0]: return dataset[keys[0]]
    if nilai_user > keys[-1]: return dataset[keys[-1]]
    for i in range(len(keys) - 1):
        x0, x1 = keys[i], keys[i+1]
        if x0 < nilai_user < x1:
            y0, y1 = dataset[x0], dataset[x1]
            return y0 + (nilai_user - x0) * (y1 - y0) / (x1 - x0)
    return 1.0

# --- 4. CSS STYLING (FUTURISTIK) ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .card-result { 
        background: rgba(38, 196, 185, 0.1); 
        padding: 20px; border-radius: 15px; 
        border: 2px solid #26c4b9; text-align: center; 
    }
    div.stButton > button {
        background: #26c4b9 !important; color: black !important;
        font-weight: bold !important; border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGIKA HALAMAN ---
if st.session_state.page == 'dashboard':
    st.title("🚀 CANEMETRIX 2.0")
    if st.button("MULAI ANALISA", use_container_width=True):
        st.session_state.page = 'pilih_analisa'
        st.rerun()

elif st.session_state.page == 'pilih_analisa':
    st.header("PILIH ANALISA")
    if st.button("🧪 ANALISA TETES", use_container_width=True):
        st.session_state.analisa_type = 'tetes'
        st.session_state.page = 'analisa_lab'
        st.rerun()
    if st.button("🔙 KEMBALI"):
        st.session_state.page = 'dashboard'
        st.rerun()

elif st.session_state.page == 'analisa_lab':
    st.header(f"ENTRY: {st.session_state.analisa_type.upper()}")
    
    # Input Jam (PENTING!)
    jam_analisa = st.selectbox("🕒 JAM ANALISA", list(range(24)), index=6)
    
    if st.session_state.analisa_type == 'tetes':
        col1, col2 = st.columns(2)
        with col1:
            bx_in = st.number_input("Brix Teramati", value=8.80)
            sh_in = st.number_input("Suhu (°C)", value=28.0)
            pol_baca = st.number_input("Pol Baca", value=11.00)
            
            # Hitung otomatis
            kor = hitung_interpolasi(sh_in, data_koreksi)
            bj = hitung_interpolasi(bx_in, data_bj)
            brix_akhir = (bx_in + kor) * 10
            pol_akhir = (0.286 * pol_baca) / bj * 10
            hk = (pol_akhir / brix_akhir * 100) if brix_akhir != 0 else 0
            
            if st.button("🚀 SIMPAN KE EXCEL"):
                with st.spinner("Mengirim data..."):
                    if kirim_ke_excel(jam_analisa, brix=brix_akhir, pol=pol_akhir):
                        st.success(f"Mantap! Data Jam {jam_analisa}:00 masuk ke baris {270+(jam_analisa-6 if jam_analisa>=6 else jam_analisa+18)}")

        with col2:
            st.markdown(f'<div class="card-result"><h1>{brix_akhir:.2f}</h1><p>% BRIX</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-result" style="border-color:#ffcc00;"><h1>{pol_akhir:.2f}</h1><p>% POL</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-result" style="border-color:#ff4b4b;"><h1>{hk:.2f}</h1><p>HK</p></div>', unsafe_allow_html=True)

    if st.button("🔙 KEMBALI"):
        st.session_state.page = 'pilih_analisa'
        st.rerun()
