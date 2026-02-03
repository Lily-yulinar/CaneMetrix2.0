import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import numpy as np

# --- 1. SETUP & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")
st_autorefresh(interval=1000, key="datarefresh")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# --- DATA TABEL KOREKSI SUHU (SESUAI FOTO TABEL BEB) ---
# Data X (Suhu), Data Y (Koreksi)
suhu_list = np.array([25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50])
koreksi_list = np.array([-0.19, -0.12, -0.05, 0.02, 0.09, 0.16, 0.24, 0.31, 0.38, 0.46, 0.54, 0.62, 0.70, 0.78, 0.86, 0.94, 1.02, 1.10, 1.18, 1.26, 1.34, 1.42, 1.50, 1.58, 1.66, 1.72])

def get_koreksi(suhu_val):
    return np.interp(suhu_val, suhu_list, koreksi_list)

# --- 2. CSS CUSTOM (GAYA AWAL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp { background-color: #0e1117; color: white; }
    
    .hero-container {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 25px;
        padding: 40px; text-align: center; margin-bottom: 40px;
    }
    
    .title-glow {
        font-family: 'Orbitron'; font-size: 50px; font-weight: 900;
        text-shadow: 0 0 20px #26c4b9; color: white; margin-bottom: 5px;
    }

    /* GRID MENU STYLE */
    .menu-grid-container {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;
    }

    .menu-card {
        background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px; padding: 30px; text-align: center; height: 180px;
        transition: 0.3s ease; display: flex; flex-direction: column; 
        justify-content: center; align-items: center;
    }

    .menu-card:hover {
        border-color: #26c4b9; background: rgba(38, 196, 185, 0.15);
        transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Override Streamlit Button biar transparan nempel di Card */
    div.stButton > button {
        background: transparent !important; border: none !important;
        color: white !important; width: 100% !important; height: 100% !important;
        font-family: 'Poppins' !important; font-weight: 700 !important; font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER WAKTU ---
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
st.markdown(f"""
    <div style="text-align: right; margin-bottom: 10px;">
        <span style="opacity:0.7;">{now.strftime("%d %B %Y")}</span><br>
        <span style="color:#26c4b9; font-size:22px; font-weight:bold;">{now.strftime("%H:%M:%S")} WIB</span>
    </div>
""", unsafe_allow_html=True)

# --- 4. LOGIKA HALAMAN ---

# HALAMAN 1: DASHBOARD
if st.session_state.page == 'dashboard':
    st.markdown('<div class="hero-container"><h1 class="title-glow">CANE METRIX</h1><p style="letter-spacing:5px; color:#26c4b9; opacity:0.8;">ACCELERATING QA PERFORMANCE</p></div>', unsafe_allow_html=True)
    
    menu_items = [
        ("📝", "Input Data"), ("🧮", "Hitung"), ("📅", "Database Harian"),
        ("📊", "Database Bulanan"), ("⚖️", "Rekap Stasiun"), ("📈", "Trend"),
        ("⚙️", "Pengaturan"), ("📥", "Export/Import"), ("👤", "Akun")
    ]
    
    # Render 3x3 Grid
    for i in range(0, 9, 3):
        cols = st.columns(3)
        for j in range(3):
            icon, name = menu_items[i+j]
            with cols[j]:
                st.markdown(f'<div class="menu-card">', unsafe_allow_html=True)
                if st.button(f"{icon}\n\n{name.upper()}", key=name):
                    if name == "Hitung":
                        st.session_state.page = 'sub_menu_hitung'
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# HALAMAN 2: SUB-MENU HITUNG
elif st.session_state.page == 'sub_menu_hitung':
    st.markdown("<h2 style='text-align:center;'>PILIH ANALISA</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="menu-card">', unsafe_allow_html=True)
        if st.button("🧪\n\nANALISA TETES"):
            st.session_state.page = 'hitung_tetes'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="menu-card">', unsafe_allow_html=True)
        if st.button("🔙\n\nKEMBALI"):
            st.session_state.page = 'dashboard'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# HALAMAN 3: HITUNG TETES
elif st.session_state.page == 'hitung_tetes':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📥 Input")
        bx_obs = st.number_input("Brix Teramati", value=8.80, step=0.01)
        suhu_in = st.number_input("Suhu Teramati (°C)", value=28.3, step=0.1, min_value=25.0, max_value=50.0)
        
        # Hitung Interpolasi
        koreksi = get_koreksi(suhu_in)
        st.info(f"Koreksi Suhu (Interpolasi): {koreksi:+.3f}")

    with col2:
        st.markdown("### 📤 Hasil")
        bx_pengenceran = bx_obs * 10
        bx_akhir = bx_pengenceran + koreksi
        
        st.metric("Brix Pengenceran (x10)", f"{bx_pengenceran:.2f}")
        st.markdown(f"""
            <div style="background: rgba(38, 196, 185, 0.15); padding: 30px; border-radius: 20px; border: 2px solid #26c4b9; text-align: center;">
                <h4 style="margin:0; opacity:0.8;">% BRIX AKHIR</h4>
                <h1 style="margin:0; color:#26c4b9; font-family:'Orbitron'; font-size:50px;">{bx_akhir:.2f}</h1>
            </div>
        """, unsafe_allow_html=True)

    if st.button("⬅️ KEMBALI"):
        st.session_state.page = 'sub_menu_hitung'
        st.rerun()
