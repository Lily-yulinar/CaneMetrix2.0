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

# --- 2. CSS (UPDATE FONT & LAYOUT) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Rajdhani:wght@700&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.75), rgba(0, 10, 30, 0.75)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* KOTAK LOGO KIRI ATAS */
    .partner-box {{ 
        background: white; 
        padding: 12px 60px; /* Lebih lebar sesuai request */
        border-radius: 15px; 
        display: inline-flex; 
        align-items: center; 
        gap: 50px; /* Jarak antar logo lebih plong */
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .img-partner {{ height: 35px; width: auto; }}

    .hero-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 40px;
        padding: 50px; margin: 10px auto 30px auto; display: flex; 
        justify-content: space-between; align-items: center; max-width: 95%;
    }}

    /* FONT JUDUL BARU - LEBIH KOTAK */
    .title-text {{
        font-family: 'Michroma', sans-serif; 
        color: white; 
        font-size: 62px; 
        letter-spacing: 8px; 
        margin: 0; 
        font-weight: 400;
        text-shadow: 0 0 15px rgba(255,255,255,0.5), 0 0 30px #26c4b9;
        text-transform: uppercase;
    }}

    .sub-title {{
        color:#26c4b9; 
        font-family: 'Poppins'; 
        font-weight: 700; 
        letter-spacing: 6px; 
        margin-top: 15px;
        opacity: 0.9;
    }}

    .logo-cane-large {{
        height: 200px; /* Logo CaneMetrix Gede di Kanan */
        filter: drop-shadow(0 0 25px #26c4b9);
    }}

    .menu-card-container {{
        position: relative; background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px); border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1); height: 180px;
        transition: 0.3s; margin-bottom: 25px; display: flex;
        flex-direction: column; justify-content: center; align-items: center;
    }}

    .menu-card-container:hover {{
        background: rgba(38, 196, 185, 0.15); border: 1px solid #26c4b9;
        box-shadow: 0 0 30px rgba(38, 196, 185, 0.4); transform: translateY(-8px);
    }}

    /* Overlay Tombol Anti-Macet */
    .stButton > button {{
        position: absolute !important; width: 100% !important; height: 180px !important;
        top: 0 !important; left: 0 !important; background: transparent !important;
        color: transparent !important; border: none !important; z-index: 999 !important;
    }}

    .menu-icon {{ font-size: 50px; margin-bottom: 10px; }}
    .menu-label {{ font-family: 'Poppins'; font-weight: 700; font-size: 14px; color: white; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIKA HALAMAN ---

if st.session_state.page == 'dashboard':
    # HEADER
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

    # HERO (FONT KOTAK & LOGO KANAN)
    st.markdown(f'''
        <div class="hero-container">
            <div style="flex: 1.5;">
                <h1 class="title-text">CANE METRIX</h1>
                <p class="sub-title">ACCELERATING QA PERFORMANCE</p>
            </div>
            <div style="flex: 0.5; text-align: right;">
                <img src="data:image/png;base64,{logo_cane}" class="logo-cane-large">
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # MENU GRID
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="menu-card-container"><div class="menu-icon">📝</div><div class="menu-label">INPUT DATA</div></div>', unsafe_allow_html=True)
        st.button("", key="btn_input")
    with col2:
        st.markdown('<div class="menu-card-container"><div class="menu-icon">🧮</div><div class="menu-label">HITUNG ANALISA</div></div>', unsafe_allow_html=True)
        if st.button("", key="btn_hitung"):
            st.session_state.page = 'analisa_tetes'
            st.rerun()
    with col3:
        st.markdown('<div class="menu-card-container"><div class="menu-icon">📅</div><div class="menu-label">DATABASE HARIAN</div></div>', unsafe_allow_html=True)
        st.button("", key="btn_harian")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown('<div class="menu-card-container"><div class="menu-icon">📊</div><div class="menu-label">DATABASE BULANAN</div></div>', unsafe_allow_html=True)
        st.button("", key="btn_bulanan")
    with col5:
        st.markdown('<div class="menu-card-container"><div class="menu-icon">⚖️</div><div class="menu-label">REKAP STASIUN</div></div>', unsafe_allow_html=True)
        st.button("", key="btn_rekap")
    with col6:
        st.markdown('<div class="menu-card-container"><div class="menu-icon">📈</div><div class="menu-label">TREND</div></div>', unsafe_allow_html=True)
        st.button("", key="btn_trend")

elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Michroma;'>🧪 PERHITUNGAN ANALISA TETES</h2>", unsafe_allow_html=True)
    st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        bx_obs = st.number_input("Brix Teramati", value=8.80, step=0.01, format="%.2f")
        suhu_obs = st.number_input("Suhu Teramati (°C)", value=28.3, step=0.1, format="%.1f")
        koreksi = hitung_interpolasi(suhu_obs)
        st.write(f"Koreksi: {koreksi:+.3f}")
    with c2:
        bx_akhir = (bx_obs * 10) + koreksi
        st.markdown(f"""
            <div style="background: rgba(38, 196, 185, 0.2); padding: 30px; border-radius: 20px; border: 2px solid #26c4b9; text-align: center;">
                <h4 style="color:white; margin:0;">% BRIX AKHIR</h4>
                <h1 style="color:#26c4b9; font-family:Michroma; font-size:55px; margin:10px 0;">{bx_akhir:.3f}</h1>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("🔙 KEMBALI"):
        st.session_state.page = 'dashboard'
        st.rerun()
