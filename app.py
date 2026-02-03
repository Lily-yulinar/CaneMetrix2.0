import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os
import numpy as np

# --- 1. SETTING PAGE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# Inisialisasi session state agar tidak hilang saat refresh
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

def pindah_halaman(nama_halaman):
    st.session_state.page = nama_halaman
    st.rerun()

# --- 2. DATA TABEL KOREKSI SUHU BRIX (Interpolasi) ---
data_koreksi = {
    25: -0.19, 26: -0.12, 27: -0.05, 28: 0.02, 29: 0.09,
    30: 0.16, 31: 0.24, 32: 0.31, 33: 0.38, 34: 0.46,
    35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86,
    40: 0.94, 41: 1.02, 42: 1.10, 43: 1.18, 44: 1.26,
    45: 1.34, 46: 1.42, 47: 1.50, 48: 1.58, 49: 1.66, 50: 1.72
}

def hitung_koreksi_suhu(suhu_input):
    suhu_list = sorted(data_koreksi.keys())
    koreksi_list = [data_koreksi[s] for s in suhu_list]
    return np.interp(suhu_input, suhu_list, koreksi_list)

# --- 3. FUNGSI LOAD LOGO ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

l_kb = get_base64_logo("kb.png")
l_sgn = get_base64_logo("sgn.png")
l_ptpn = get_base64_logo("ptpn.png")
l_lpp = get_base64_logo("lpp.png")
l_cane = get_base64_logo("canemetrix.png")
url_bumn_backup = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Logo_BUMN.svg/512px-Logo_BUMN.svg.png"

# --- 4. CSS CUSTOM (UI & Partner Box) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
    }}

    .fixed-partner-box {{ 
        background: white; padding: 10px 40px; border-radius: 12px; 
        display: flex; align-items: center; gap: 35px; 
        width: 650px !important; box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }}
    
    .fixed-partner-box img {{ height: 35px; width: auto; }}

    .jam-digital {{
        color: #26c4b9; font-size: 40px; font-weight: 900; 
        font-family: 'Poppins'; text-shadow: 0 0 15px rgba(38, 196, 185, 0.6);
    }}

    .glass-card {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); 
        padding: 30px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }}

    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important; height: 160px !important; width: 100% !important;
        font-size: 18px !important; font-weight: 700 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. HEADER ---
@st.fragment
def render_header():
    h1, h2 = st.columns([10, 3])
    with h1:
        src_kb = f"data:image/png;base64,{l_kb}" if l_kb else url_bumn_backup
        st.markdown(f'''
        <div class="fixed-partner-box">
            <img src="{src_kb}">
            <img src="data:image/png;base64,{l_sgn if l_sgn else ''}">
            <img src="data:image/png;base64,{l_ptpn if l_ptpn else ''}">
            <img src="data:image/png;base64,{l_lpp if l_lpp else ''}">
        </div>''', unsafe_allow_html=True)
    with h2:
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.datetime.now(tz)
        st.markdown(f'''
            <div style="text-align:right;">
                <div style="color:white; opacity:0.8; font-family:Poppins; font-size:14px;">{now.strftime("%d %B %Y")}</div>
                <div class="jam-digital">{now.strftime("%H:%M:%S")}</div>
            </div>''', unsafe_allow_html=True)
    st_autorefresh(interval=1000, key="global_clock")

render_header()

# --- 6. LOGIKA NAVIGASI HALAMAN ---

# HALAMAN DASHBOARD
if st.session_state.page == 'dashboard':
    st.markdown(f'''
    <div class="glass-card" style="display:flex; justify-content:space-between; align-items:center; margin-top:20px;">
        <div>
            <h1 style="font-family:'Michroma'; color:white; font-size:clamp(30px, 5vw, 55px); margin:0; letter-spacing:8px;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:'Poppins'; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{l_cane if l_cane else ''}" height="150">
    </div>''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("📝\nINPUT DATA"): pindah_halaman('input_data')
    with c2: 
        if st.button("🧮\nHITUNG ANALISA"): pindah_halaman('analisa_tetes')
    with c3: 
        if st.button("📅\nDATABASE HARIAN"): pindah_halaman('db_harian')

# HALAMAN HITUNG ANALISA (Ini yang lo cari, Beb!)
elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4 style='color:white;'>Input Data Lab</h4>", unsafe_allow_html=True)
        brix_obs = st.number_input("Brix Teramati", min_value=0.0, value=8.50, step=0.01, format="%.2f")
        
        # Hitung Otomatis Pengenceran (x10)
        brix_pengenceran = brix_obs * 10
        st.info(f"Brix Pengenceran (x10): **{brix_pengenceran:.2f}**")
        
        suhu = st.number_input("Suhu (°C)", min_value=25.0, max_value=50.0, value=28.0, step=0.1)

    with col2:
        st.markdown("<h4 style='color:white;'>Hasil Analisa</h4>", unsafe_allow_html=True)
        # Logika Interpolasi
        koreksi = hitung_koreksi_suhu(suhu)
        brix_akhir = brix_pengenceran + koreksi
        
        st.markdown(f"""
            <div style="background: rgba(38, 196, 185, 0.1); padding: 25px; border-radius: 20px; border: 1px solid #26c4b9; text-align: center;">
                <p style="color: white; margin: 0; opacity: 0.8;">Nilai Koreksi Suhu</p>
                <h3 style="color: #26c4b9; margin: 0;">{koreksi:+.2f}</h3>
                <div style="margin: 15px 0; border-top: 1px solid rgba(255,255,255,0.1);"></div>
                <p style="color: white; margin: 0; opacity: 0.8; font-weight: bold;">% BRIX AKHIR</p>
                <h1 style="color: white; font-size: 60px; margin: 0;">{brix_akhir:.2f}</h1>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')

# HALAMAN LAIN (Placeholder)
elif st.session_state.page == 'input_data':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>📝 INPUT DATA</h2>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')

elif st.session_state.page == 'db_harian':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>📅 DATABASE HARIAN</h2>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')
