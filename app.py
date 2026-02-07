import streamlit as st
import datetime
import pytz
import base64
import os
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIG & KONEKSI ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

def init_connection():
    try:
        # Mengambil data dari Streamlit Secrets (Format TOML)
        s = st.secrets["gcp_service_account"]
        info = {
            "type": s["type"],
            "project_id": s["project_id"],
            "private_key_id": s["private_key_id"],
            "private_key": s["private_key"],
            "client_email": s["client_email"],
            "client_id": s["client_id"],
            "auth_uri": s["auth_uri"],
            "token_uri": s["token_uri"],
            "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
            "client_x509_cert_url": s["client_x509_cert_url"]
        }
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Gagal Inisialisasi Koneksi: {e}")
        return None

def simpan_ke_gsheets(data_list):
    client = init_connection()
    if client:
        try:
            # PASTIKAN: Nama file di Drive sudah "KKKB_250711" (Bukan .xlsx)
            sh = client.open("KKKB_250711") 
            # PASTIKAN: Ada sheet bernama "INPUT"
            worksheet = sh.worksheet("INPUT")
            worksheet.append_row(data_list)
            return True, "Data Berhasil Disimpan! ✅"
        except Exception as e:
            return False, f"Gagal Simpan: {e}"
    return False, "Koneksi Gagal"

# --- 2. SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'analisa_type' not in st.session_state:
    st.session_state.analisa_type = None

# --- 3. DATABASE TABEL (INTERPOLASI) ---
data_koreksi = {27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94}
data_bj = {0.0: 0.99640, 5.0: 1.01592, 10.0: 1.03608, 15.0: 1.05691, 20.0: 1.07844, 25.0: 1.10069, 30.0: 1.12368, 35.0: 1.14745, 40.0: 1.17203, 45.0: 1.19746, 50.0: 1.22372, 60.0: 1.27885, 70.0: 1.33775}

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

# --- 4. CSS CUSTOM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .hero-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 40px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    div.stButton > button {
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: white !important;
        height: 150px !important;
        font-family: 'Orbitron', sans-serif !important;
        transition: 0.3s !important;
    }
    
    div.stButton > button:hover {
        border-color: #26c4b9 !important;
        box-shadow: 0 0 25px rgba(38, 196, 185, 0.4) !important;
        transform: translateY(-5px) !important;
    }

    .card-result {
        background: rgba(38, 196, 185, 0.1);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #26c4b9;
        text-align: center;
        margin-bottom: 15px;
    }
    
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: white; }
    p { font-family: 'Poppins', sans-serif; color: #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGIKA HALAMAN ---

# --- DASHBOARD ---
if st.session_state.page == 'dashboard':
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown("<h1 style='font-size:60px; margin:0;'>CANE METRIX</h1>", unsafe_allow_html=True)
    st.markdown("<p style='letter-spacing:5px; color:#26c4b9;'>ACCELERATING QA PERFORMANCE</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📝\n\nINPUT DATA", use_container_width=True): st.toast("Fitur Database Segera Hadir")
    with c2:
        if st.button("🧮\n\nHITUNG ANALISA", use_container_width=True):
            st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        if st.button("📅\n\nDATABASE HARIAN", use_container_width=True): st.toast("Fitur View Data Segera Hadir")

# --- PILIH JENIS ANALISA ---
elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        if st.button("🧪 ANALISA TETES", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
    with m2:
        if st.button("🔬 OD TETES", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'od'; st.rerun()
    
    if st.button("🔙 KEMBALI KE DASHBOARD", use_container_width=True):
        st.session_state.page = 'dashboard'; st.rerun()

# --- HALAMAN HITUNG (LAB) ---
elif st.session_state.page == 'analisa_lab':
    list_jam = [f"{(i % 24):02d}:00" for i in range(6, 30)] # Jam 06:00 sampai 05:00 besoknya

    if st.session_state.analisa_type == 'tetes':
        st.markdown("<h2 style='color:#26c4b9;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        col_in, col_res = st.columns(2)
        
        with col_in:
            jam_sel = st.selectbox("Analisa Jam", options=list_jam)
            bx_obs = st.number_input("Brix Teramati", value=8.80, format="%.2f")
            temp = st.number_input("Suhu (°C)", value=28.0, format="%.1f")
            pol_rd = st.number_input("Pol Baca", value=11.00, format="%.2f")
            
            # Perhitungan
            kor = hitung_interpolasi(temp, data_koreksi)
            bj = hitung_interpolasi(bx_obs, data_bj)
            brix_final = (bx_obs + kor) * 10
            pol_final = (0.286 * pol_rd) / bj * 10
            hk = (pol_final / brix_final * 100) if brix_final != 0 else 0
            
            if st.button("🚀 SIMPAN KE EXCEL", use_container_width=True):
                tgl = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d")
                # Format Baris: Tanggal, Jam, Jenis, Brix, Pol, HK
                row = [tgl, jam_sel, "Tetes", brix_final, pol_final, hk]
                sukses, msg = simpan_ke_gsheets(row)
                if sukses: st.success(msg)
                else: st.error(msg)

        with col_res:
            st.markdown(f'<div class="card-result"><h3>% BRIX</h3><h1 style="color:#26c4b9;">{brix_final:.3f}</h1></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-result"><h3>% POL</h3><h1 style="color:#ffcc00;">{pol_final:.3f}</h1></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-result"><h3>HK</h3><h1 style="color:#ff4b4b;">{hk:.2f}</h1></div>', unsafe_allow_html=True)

    elif st.session_state.analisa_type == 'od':
        st.markdown("<h2 style='color:#ff4b4b;'>🔬 OD TETES</h2>", unsafe_allow_html=True)
        jam_sel = st.selectbox("Analisa Jam", options=list_jam)
        bx_od = st.number_input("Brix Teramati", value=8.80)
        abs_val = st.number_input("Absorbansi (λ)", value=0.418, format="%.3f")
        
        bj_od = hitung_interpolasi(bx_od, data_bj)
        od_res = (abs_val * bj_od * 500) / 1
        
        st.markdown(f'<div class="card-result"><h3>HASIL OD</h3><h1>{od_res:.3f}</h1></div>', unsafe_allow_html=True)
        
        if st.button("🚀 SIMPAN KE EXCEL", use_container_width=True):
            tgl = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d")
            row = [tgl, jam_sel, "OD Tetes", bx_od, abs_val, od_res]
            sukses, msg = simpan_ke_gsheets(row)
            if sukses: st.success(msg)
            else: st.error(msg)

    if st.button("🔙 KEMBALI"):
        st.session_state.page = 'pilih_analisa'; st.rerun()
