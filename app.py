import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- 1. INITIAL STATE & CONFIG ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")
st_autorefresh(interval=1000, key="datarefresh")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# Waktu & Jam
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# Tabel Koreksi
data_koreksi = {
    25: -0.19, 26: -0.12, 27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16,
    31: 0.24, 32: 0.31, 33: 0.38, 34: 0.46, 35: 0.54, 36: 0.62,
    37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94, 41: 1.02, 42: 1.10,
    43: 1.18, 44: 1.26, 45: 1.34, 46: 1.42, 47: 1.50, 48: 1.58,
    49: 1.66, 50: 1.72
}

def hitung_interpolasi(suhu_user):
    suhu_keys = sorted(data_koreksi.keys())
    if suhu_user in data_koreksi: return data_koreksi[suhu_user]
    for i in range(len(suhu_keys) - 1):
        x0, x1 = suhu_keys[i], suhu_keys[i+1]
        if x0 < suhu_user < x1:
            y0, y1 = data_koreksi[x0], data_koreksi[x1]
            return y0 + (suhu_user - x0) * (y1 - y0) / (x1 - x0)
    return 0.0

def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 2. CSS (FIX KLIK & JAM GEDE) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.8), rgba(0, 10, 30, 0.8)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
    }}

    /* HEADER LOGO BOX */
    .partner-box {{ 
        background: white; padding: 12px 60px; border-radius: 12px; 
        display: inline-flex; align-items: center; gap: 50px;
        min-width: 450px;
    }}

    /* JAM SUPER GEDE */
    .jam-container {{ text-align: right; color: white; font-family: 'Poppins'; }}
    .jam-digital {{
        color: #26c4b9; font-size: 55px; font-weight: 900; 
        line-height: 1; text-shadow: 0 0 20px rgba(38, 196, 185, 0.8);
    }}

    /* DASHBOARD HERO */
    .hero-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 40px;
        padding: 50px; margin: 20px 0; display: flex; justify-content: space-between; align-items: center;
    }}

    /* STYLE TOMBOL BIAR JADI CARD (BIAR BISA DIKLIK!) */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        height: 180px !important;
        width: 100% !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        transition: 0.3s !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    div.stButton > button:hover {{
        border: 1px solid #26c4b9 !important;
        background: rgba(38, 196, 185, 0.15) !important;
        box-shadow: 0 0 25px rgba(38, 196, 185, 0.4) !important;
        transform: translateY(-5px) !important;
    }}

    /* Tombol Khusus Kembali */
    .back-btn button {{
        height: auto !important; width: auto !important;
        background: #26c4b9 !important; padding: 10px 30px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
c_h1, c_h2 = st.columns([3, 1])
with c_h1:
    st.markdown(f'''<div class="partner-box">
        <img src="data:image/png;base64,{logo_ptpn}" height="35">
        <img src="data:image/png;base64,{logo_sgn}" height="35">
        <img src="data:image/png;base64,{logo_lpp}" height="35">
    </div>''', unsafe_allow_html=True)
with c_h2:
    st.markdown(f'''<div class="jam-container">
        <div style="font-size: 20px; opacity: 0.8;">{tgl_skrg}</div>
        <div class="jam-digital">{jam_skrg}</div>
    </div>''', unsafe_allow_html=True)

# --- 4. MAIN NAVIGATION ---
if st.session_state.page == 'dashboard':
    st.markdown(f'''
    <div class="hero-container">
        <div>
            <h1 style="font-family:'Michroma'; color:white; font-size:55px; margin:0; letter-spacing:10px;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:'Poppins'; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{logo_cane}" height="180">
    </div>
    ''', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("📝\n\nINPUT DATA", key="btn_input")
    with col2:
        # TOMBOL INI SEKARANG PASTI BISA DIKLIK
        if st.button("🧮\n\nHITUNG ANALISA", key="btn_hitung"):
            st.session_state.page = 'analisa_tetes'
            st.rerun()
    with col3:
        st.button("📅\n\nDATABASE HARIAN", key="btn_harian")

    col4, col5, col6 = st.
