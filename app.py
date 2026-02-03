import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- 1. SETUP HALAMAN & SESSION STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")
st_autorefresh(interval=1000, key="datarefresh")

# Inisialisasi halaman biar bisa pindah-pindah
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# Waktu & Jam
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# Fungsi Logo
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 2. CSS GLOBAL (Glow & Cards) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.75), rgba(0, 10, 30, 0.75)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    .partner-box {{
        background: rgba(255, 255, 255, 1);
        padding: 8px 20px; border-radius: 12px; display: inline-flex; align-items: center; gap: 20px;
    }}
    .img-partner {{ height: 35px; width: auto; }}

    .hero-container {{
        background: rgba(255, 255, 255, 0.12); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 30px;
        padding: 25px; margin: 10px auto 30px auto; text-align: center; max-width: 90%;
    }}

    .title-text {{
        font-family: 'Orbitron'; color: white; font-size: 65px; letter-spacing: 12px; margin: 0; font-weight: 900;
        text-shadow: 0 0 10px #fff, 0 0 20px #26c4b9, 0 0 40px #26c4b9;
    }}

    .menu-card {{
        background: rgba(255, 255, 255, 0.07); backdrop-filter: blur(10px);
        padding: 25px 10px; border-radius: 20px; text-align: center; color: white;
        height: 180px; border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.3s ease-in-out; display: flex; flex-direction: column; justify-content: center; align-items: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. HALAMAN DASHBOARD ---
if st.session_state.page == 'dashboard':
    # Header
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f'<div class="partner-box"><img src="data:image/png;base64,{logo_ptpn}" class="img-partner"><img src="data:image/png;base64,{logo_sgn}" class="img-partner"><img src="data:image/png;base64,{logo_lpp}" class="img-partner"></div>', unsafe_allow_html=True)
    with c2:
        st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], label_visibility="collapsed")
        st.markdown(f'<div style="text-align: right; color: white;">{tgl_skrg}<br><span style="font-size: 24px; color: #26c4b9; font-weight: bold;">{jam_skrg} WIB</span></div>', unsafe_allow_html=True)

    # Hero
    st.markdown(f'<div class="hero-container"><img src="data:image/png;base64,{logo_cane}" class="main-logo-cane"><h1 class="title-text">CANE METRIX</h1><p style="color:#26c4b9; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p></div>', unsafe_allow_html=True)

    # Grid Menu
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="menu-card"><div style="font-size: 50px;">📝</div><div>INPUT DATA</div></div>', unsafe_allow_html=True)
    with col2:
        # Tombol Hitung yang bisa diklik
        if st.button("🧮 BUKA MENU HITUNG", use_container_width=True):
            st.session_state.page = 'pilih_hitung'
            st.rerun()
    with col3:
        st.markdown('<div class="menu-card"><div style="font-size: 50px;">📅</div><div>DATABASE HARIAN</div></div>', unsafe_allow_html=True)

# --- 4. SUB-MENU PILIHAN HITUNG ---
elif st.session_state.page == 'pilih_hitung':
    st.markdown("<h2 style='text-align: center; color: white;'>PILIH ANALISA</h2>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🧪 Hitung Analisa Tetes", use_container_width=True):
            st.session_state.page = 'hitung_tetes'
            st.rerun()
    with col_b:
        if st.button("🔙 Kembali ke Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()

# --- 5. HALAMAN HITUNG ANALISA TETES ---
elif st.session_state.page == 'hitung_tetes':
    st.markdown("<h2 style='text-align: center; color: #26c4b9;'>🧪 Analisa Tetes</h2>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📥 Input Data")
            # 1. Input Brix Teramati
            brix_obs = st.number_input("Brix Teramati", min_value=0.0, step=0.01, format="%.2f")
            
            # 2. Koreksi Suhu (Berdasarkan Tabel Lampiran lo Beb)
            # Karena di tabel itu koreksi berdasarkan SUHU, kita tetep input suhu ya
            suhu = st.selectbox("Pilih Suhu Teramati (°C)", [27, 28, 29, 30, 31, 32, 33, 34, 35, 36])
            
            tabel_koreksi = {
                27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24,
                32: 0.31, 33: 0.38, 34: 0.46, 35: 0.62, 36: 0.70
            }
            koreksi = tabel_koreksi.get(suhu, 0.0)

        with col2:
            st.markdown("### 📤 Hasil Perhitungan")
            # Rumus: (Brix Obs * 10) + Koreksi Suhu
            brix_pengenceran = brix_obs * 10
            brix_akhir = brix_pengenceran + koreksi
            
            st.metric("Brix Pengenceran (x10)", f"{brix_pengenceran:.2f}")
            st.metric("Koreksi Suhu", f"{koreksi:+.2f}")
            
            st.markdown(f"""
                <div style="background: rgba(38, 196, 185, 0.2); padding: 20px; border-radius: 15px; border: 2px solid #26c4b9; text-align: center;">
                    <h3 style="margin:0; color: white;">% BRIX AKHIR</h3>
                    <h1 style="margin:0; color: #26c4b9; font-size: 45px; font-family: 'Orbitron';">{brix_akhir:.2f}</h1>
                </div>
            """, unsafe_allow_html=True)

    if st.button("⬅️ Kembali"):
        st.session_state.page = 'pilih_hitung'
        st.rerun()
