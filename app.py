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

# Waktu & Jam (Update Realtime)
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

# --- 2. CSS CUSTOM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0, 10, 30, 0.75), rgba(0, 10, 30, 0.75)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }

    .partner-box { 
        background: white; 
        padding: 12px 60px; 
        border-radius: 12px; 
        display: inline-flex; 
        align-items: center; 
        gap: 50px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        min-width: 450px;
    }

    .hero-container {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 40px;
        padding: 50px; margin: 10px auto 30px auto; display: flex; 
        justify-content: space-between; align-items: center; max-width: 95%;
    }

    .title-text {
        font-family: 'Michroma', sans-serif; 
        color: white; font-size: 58px; letter-spacing: 12px; 
        margin: 0; text-transform: uppercase;
        text-shadow: 0 0 15px #26c4b9;
    }

    /* JAM GEDE & BOLD */
    .time-container { text-align: right; color: white; font-family: 'Poppins'; }
    .clock-text {
        color: #26c4b9; font-size: 32px; font-weight: 900; 
        letter-spacing: 2px; text-shadow: 0 0 10px rgba(38, 196, 185, 0.5);
    }

    .menu-card-container {
        position: relative; background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px); border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1); height: 180px;
        transition: 0.3s; margin-bottom: 25px; display: flex;
        flex-direction: column; justify-content: center; align-items: center;
    }

    .menu-card-container:hover {
        background: rgba(38, 196, 185, 0.15); border: 1px solid #26c4b9;
        transform: translateY(-5px);
    }

    /* Tombol Transparan biar seluruh Card bisa di klik */
    .stButton > button {
        position: absolute !important; width: 100% !important; height: 180px !important;
        top: 0 !important; left: 0 !important; background: transparent !important;
        color: transparent !important; border: none !important; z-index: 999 !important;
    }

    /* Style Tombol Kembali */
    .back-btn-style button {
        position: relative !important; width: auto !important; height: auto !important;
        background: #26c4b9 !important; color: white !important; 
        padding: 10px 25px !important; border-radius: 12px !important;
        font-weight: bold !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIKA HALAMAN ---

# Tampilan Header (Tetap muncul di semua halaman)
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown(f'''<div class="partner-box">
        <img src="data:image/png;base64,{logo_ptpn}" height="35">
        <img src="data:image/png;base64,{logo_sgn}" height="35">
        <img src="data:image/png;base64,{logo_lpp}" height="35">
    </div>''', unsafe_allow_html=True)
with c2:
    st.markdown(f'''<div class="time-container">
        <div style="font-size:18px;">{tgl_skrg}</div>
        <div class="clock-text">{jam_skrg} WIB</div>
    </div>''', unsafe_allow_html=True)


if st.session_state.page == 'dashboard':
    # Hero Dashboard
    st.markdown(f'''<div class="hero-container">
        <div>
            <h1 class="title-text">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{logo_cane}" height="180">
    </div>''', unsafe_allow_html=True)

    # Grid Menu Utama
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown('<div class="menu-card-container"><div style="font-size:50px;">📝</div><div style="color:white; font-weight:700;">INPUT DATA</div></div>', unsafe_allow_html=True)
        st.button("", key="b1")
    with m2:
        st.markdown('<div class="menu-card-container"><div style="font-size:50px;">🧮</div><div style="color:white; font-weight:700;">HITUNG ANALISA</div></div>', unsafe_allow_html=True)
        # TRIGGER PINDAH KE KALKULATOR
        if st.button("", key="b2"):
            st.session_state.page = 'analisa_tetes'
            st.rerun()
    with m3:
        st.markdown('<div class="menu-card-container"><div style="font-size:50px;">📅</div><div style="color:white; font-weight:700;">DATABASE HARIAN</div></div>', unsafe_allow_html=True)
        st.button("", key="b3")

    m4, m5, m6 = st.columns(3)
    with m4:
        st.markdown('<div class="menu-card-container"><div style="font-size:50px;">📊</div><div style="color:white; font-weight:700;">DATABASE BULANAN</div></div>', unsafe_allow_html=True)
        st.button("", key="b4")
    with m5:
        st.markdown('<div class="menu-card-container"><div style="font-size:50px;">⚖️</div><div style="color:white; font-weight:700;">REKAP STASIUN</div></div>', unsafe_allow_html=True)
        st.button("", key="b5")
    with m6:
        st.markdown('<div class="menu-card-container"><div style="font-size:50px;">📈</div><div style="color:white; font-weight:700;">TREND</div></div>', unsafe_allow_html=True)
        st.button("", key="b6")

elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h1 style='text-align:center; color:white; font-family:Michroma; letter-spacing:5px; margin-top:20px;'>🧪 ANALISA TETES</h1>", unsafe_allow_html=True)
    
    # Wadah Kalkulator
    st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
    col_in, col_res = st.columns(2)
    
    with col_in:
        st.markdown("<h4 style='color:#26c4b9;'>Parameter Input</h4>", unsafe_allow_html=True)
        bx = st.number_input("Brix Teramati", value=8.80, format="%.2f", step=0.01)
        sh = st.number_input("Suhu Teramati (°C)", value=28.3, format="%.1f", step=0.1)
        kor = hitung_interpolasi(sh)
        st.info(f"Faktor Koreksi: {kor:+.3f}")
    
    with col_res:
        hasil = (bx * 10) + kor
        st.markdown(f'''<div style="background:rgba(38,196,185,0.2); padding:40px; border-radius:20px; border:2px solid #26c4b9; text-align:center; margin-top:10px;">
            <h3 style="color:white; margin:0; font-family:Poppins;">HASIL % BRIX AKHIR</h3>
            <h1 style="color:#26c4b9; font-family:Michroma; font-size:65px; margin:15px 0;">{hasil:.3f}</h1>
        </div>''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tombol Kembali ke Dashboard
    st.markdown('<div class="back-btn-style" style="text-align:center; margin-top:20px;">', unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE MENU UTAMA"):
        st.session_state.page = 'dashboard'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
