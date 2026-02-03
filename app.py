import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- 1. INITIAL STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")
st_autorefresh(interval=1000, key="datarefresh")

# Waktu & Jam
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# Data Tabel Koreksi (Interpolasi)
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
    if suhu_user < suhu_keys[0]: return data_koreksi[suhu_keys[0]]
    if suhu_user > suhu_keys[-1]: return data_koreksi[suhu_keys[-1]]
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

# --- 2. CSS (TAMPILAN MEWAH) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.75), rgba(0, 10, 30, 0.75)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* KOTAK LOGO KIRI ATAS LEBIH PANJANG */
    .partner-box {{ 
        background: white; 
        padding: 12px 50px; 
        border-radius: 15px; 
        display: inline-flex; 
        align-items: center; 
        gap: 40px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .img-partner {{ height: 38px; width: auto; }}

    .hero-container {{
        background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 30px;
        padding: 40px; margin: 10px auto 30px auto; display: flex; 
        justify-content: space-between; align-items: center; max-width: 95%;
    }}

    .title-text {{
        font-family: 'Orbitron'; color: white; font-size: 58px; letter-spacing: 10px; margin: 0; font-weight: 900;
        text-shadow: 0 0 10px #fff, 0 0 20px #26c4b9, 0 0 40px #26c4b9;
    }}

    .logo-cane-large {{
        height: 190px; /* LOGO CANEMETRIX GEDE */
        filter: drop-shadow(0 0 20px #26c4b9);
    }}

    .menu-card-container {{
        position: relative; background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px); border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1); height: 200px;
        transition: 0.3s; margin-bottom: 25px; display: flex;
        flex-direction: column; justify-content: center; align-items: center;
    }}

    .menu-card-container:hover {{
        background: rgba(38, 196, 185, 0.15); border: 1px solid #26c4b9;
        box-shadow: 0 0 25px rgba(38, 196, 185, 0.4); transform: translateY(-5px);
    }}

    /* Overlay Tombol */
    .stButton > button {{
        position: absolute !important; width: 100% !important; height: 200px !important;
        top: 0 !important; left: 0 !important; background: transparent !important;
        color: transparent !important; border: none !important; z-index: 999 !important;
    }}

    .menu-content {{ text-align: center; color: white; pointer-events: none; }}
    .menu-icon {{ font-size: 55px; margin-bottom: 10px; display: block; }}
    .menu-label {{ font-family: 'Poppins'; font-weight: 700; font-size: 14px; text-transform: uppercase; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIKA HALAMAN ---

if st.session_state.page == 'dashboard':
    # HEADER (LOGO PARTNER & WAKTU)
    c_top1, c_top2 = st.columns([2, 1])
    with c_top1:
        st.markdown(f'''
            <div class="partner-box">
                <img src="data:image/png;base64,{logo_ptpn}" class="img-partner">
                <img src="data:image/png;base64,{logo_sgn}" class="img-partner">
                <img src="data:image/png;base64,{logo_lpp}" class="img-partner">
            </div>
        ''', unsafe_allow_html=True)
    with c_top2:
        st.markdown(f'<div style="text-align: right; color: white; font-family: \'Poppins\';"><span>{tgl_skrg}</span><br><b style="color:#26c4b9; font-size:24px;">{jam_skrg} WIB</b></div>', unsafe_allow_html=True)

    # HERO (LOGO CANEMETRIX DI KANAN)
    st.markdown(f'''
        <div class="hero-container">
            <div style="flex: 1.5;">
                <h1 class="title-text">CANE METRIX</h1>
                <p style="color:#26c4b9; font-family:\'Poppins\'; font-weight:700; letter-spacing:5px; margin-top:10px;">ACCELERATING QA PERFORMANCE</p>
            </div>
            <div style="flex: 0.5; text-align: right;">
                <img src="data:image/png;base64,{logo_cane}" class="logo-cane-large">
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # GRID MENU (MANUAL BIAR STABIL)
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1:
        st.markdown('<div class="menu-card-container"><div class="menu-content"><span class="menu-icon">📝</span><span class="menu-label">Input Data</span></div></div>', unsafe_allow_html=True)
        st.button("", key="btn_input")

    with row1_col2:
        st.markdown('<div class="menu-card-container"><div class="menu-content"><span class="menu-icon">🧮</span><span class="menu-label">Hitung Analisa</span></div></div>', unsafe_allow_html=True)
        if st.button("", key="btn_hitung"):
            st.session_state.page = 'analisa_tetes'
            st.rerun()

    with row1_col3:
        st.markdown('<div class="menu-card-container"><div class="menu-content"><span class="menu-icon">📅</span><span class="menu-label">Database Harian</span></div></div>', unsafe_allow_html=True)
        st.button("", key="btn_harian")

    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1:
        st.markdown('<div class="menu-card-container"><div class="menu-content"><span class="menu-icon">📊</span><span class="menu-label">Database Bulanan</span></div></div>', unsafe_allow_html=True)
        st.button("", key="btn_bulanan")
    with row2_col2:
        st.markdown('<div class="menu-card-container"><div class="menu-content"><span class="menu-icon">⚖️</span><span class="menu-label">Rekap Stasiun</span></div></div>', unsafe_allow_html=True)
        st.button("", key="btn_rekap")
    with row2_col3:
        st.markdown('<div class="menu-card-container"><div class="menu-content"><span class="menu-icon">📈</span><span class="menu-label">Trend</span></div></div>', unsafe_allow_html=True)
        st.button("", key="btn_trend")

elif st.session_state.page == 'analisa_tetes':
    # HALAMAN ANALISA TETES
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron; margin-bottom:20px;'>🧪 PERHITUNGAN ANALISA TETES</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<h3 style='color:white;'>📥 INPUT</h3>", unsafe_allow_html=True)
        bx_obs = st.number_input("Brix Teramati", value=8.80, step=0.01, format="%.2f")
        suhu_obs = st.number_input("Suhu Teramati (°C)", value=28.3, step=0.1, format="%.1f")
        koreksi = hitung_interpolasi(suhu_obs)
        st.info(f"Koreksi Tabel: {koreksi:+.3f}")
    
    with c2:
        st.markdown("<h3 style='color:white;'>📤 OUTPUT</h3>", unsafe_allow_html=True)
        bx_akhir = (bx_obs * 10) + koreksi
        st.markdown(f"""
            <div style="background: rgba(38, 196, 185, 0.2); padding: 30px; border-radius: 20px; border: 2px solid #26c4b9; text-align: center;">
                <h4 style="color:white; margin:0;">% BRIX AKHIR</h4>
                <h1 style="color:#26c4b9; font-family:Orbitron; font-size:60px; margin:10px 0;">{bx_akhir:.3f}</h1>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔙 KEMBALI KE BERANDA", key="btn_back"):
        st.session_state.page = 'dashboard'
        st.rerun()
