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

# Waktu
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# Data Tabel Koreksi
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

# --- 2. CSS (TAMPILAN ACC LO) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.75), rgba(0, 10, 30, 0.75)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    .hero-container {{
        background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 30px;
        padding: 40px; margin: 10px auto 30px auto; display: flex; justify-content: space-between; align-items: center;
    }}

    .logo-cane-large {{ height: 180px; filter: drop-shadow(0 0 20px #26c4b9); }}

    .menu-card-container {{
        position: relative; background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px); border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1); height: 180px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        transition: 0.3s;
    }}

    .menu-card-container:hover {{
        background: rgba(38, 196, 185, 0.15); border: 1px solid #26c4b9;
        box-shadow: 0 0 25px rgba(38, 196, 185, 0.4); transform: translateY(-5px);
    }}

    /* CSS Fix Tombol: Pastikan menutupi seluruh area card */
    .stButton > button {{
        position: absolute !important; width: 100% !important; height: 180px !important;
        top: 0 !important; left: 0 !important; background: transparent !important;
        color: transparent !important; border: none !important; z-index: 999 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIKA HALAMAN ---
if st.session_state.page == 'dashboard':
    # Header partner & Jam
    c_top1, c_top2 = st.columns([2, 1])
    with c_top1:
        st.markdown(f'<div style="background:white; padding:8px; border-radius:12px; display:inline-flex; gap:15px;"><img src="data:image/png;base64,{logo_ptpn}" height="35"><img src="data:image/png;base64,{logo_sgn}" height="35"><img src="data:image/png;base64,{logo_lpp}" height="35"></div>', unsafe_allow_html=True)
    with c_top2:
        st.markdown(f'<div style="text-align: right; color: white;">{tgl_skrg}<br><b style="color:#26c4b9; font-size:20px;">{jam_skrg} WIB</b></div>', unsafe_allow_html=True)

    # Hero
    st.markdown(f'''
        <div class="hero-container">
            <div>
                <h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0;">CANE METRIX</h1>
                <p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p>
            </div>
            <img src="data:image/png;base64,{logo_cane}" class="logo-cane-large">
        </div>
    ''', unsafe_allow_html=True)

    # GRID MENU (DIBUAT MANUAL BIAR SENSOR KLIK GAK ERROR)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="menu-card-container"><div style="font-size:50px;">📝</div><div style="color:white; font-weight:700;">INPUT DATA</div></div>', unsafe_allow_html=True)
        st.button("", key="btn_input")
        
    with col2:
        st.markdown('<div class="menu-card-container"><div style="font-size:50px;">🧮</div><div style="color:white; font-weight:700;">HITUNG ANALISA</div></div>', unsafe_allow_html=True)
        # INI TOMBOLNYA BEB!
        if st.button("", key="btn_hitung"):
            st.session_state.page = 'analisa_tetes'
            st.rerun()

    with col3:
        st.markdown('<div class="menu-card-container"><div style="font-size:50px;">📅</div><div style="color:white; font-weight:700;">DATABASE HARIAN</div></div>', unsafe_allow_html=True)
        st.button("", key="btn_harian")

    # Baris 2
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown('<div class="menu-card-container"><div style="font-size:50px;">📊</div><div style="color:white; font-weight:700;">DATABASE BULANAN</div></div>', unsafe_allow_html=True)
        st.button("", key="btn_bulanan")
    with col5:
        st.markdown('<div class="menu-card-container"><div style="font-size:50px;">⚖️</div><div style="color:white; font-weight:700;">REKAP STASIUN</div></div>', unsafe_allow_html=True)
        st.button("", key="btn_rekap")
    with col6:
        st.markdown('<div class="menu-card-container"><div style="font-size:50px;">📈</div><div style="color:white; font-weight:700;">TREND</div></div>', unsafe_allow_html=True)
        st.button("", key="btn_trend")

elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 PERHITUNGAN ANALISA TETES</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="hero-container" style="display:block; text-align:center;">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            bx_obs = st.number_input("Brix Teramati", value=8.80, format="%.2f")
            suhu_obs = st.number_input("Suhu Teramati (°C)", value=28.3, format="%.1f")
            koreksi = hitung_interpolasi(suhu_obs)
            st.success(f"Koreksi: {koreksi:+.3f}")
        with c2:
            bx_akhir = (bx_obs * 10) + koreksi
            st.markdown(f"""
                <div style="background: rgba(38, 196, 185, 0.2); padding: 20px; border-radius: 20px; border: 2px solid #26c4b9;">
                    <h4 style="color:white;">% BRIX AKHIR</h4>
                    <h1 style="color:#26c4b9; font-size:60px; font-family:Orbitron;">{bx_akhir:.3f}</h1>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔙 KEMBALI"):
        st.session_state.page = 'dashboard'
        st.rerun()


NAH KETIKA GW KLIK SUB MENU HITUNG, MUNCUL KALKULATOR ANALISA TETES YA.
