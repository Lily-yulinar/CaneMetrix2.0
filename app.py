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

# --- 2. CSS FIX (ANTI BERANTAKAN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0, 10, 30, 0.8), rgba(0, 10, 30, 0.8)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }

    /* Container Menu */
    .menu-wrapper {
        position: relative;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: 0.3s;
        z-index: 1;
    }

    /* Sembunyikan Button Streamlit tapi tetep bisa diklik di atas Wrapper */
    .stButton > button {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 160px;
        background: transparent !important;
        color: transparent !important;
        border: none !important;
        z-index: 10;
        cursor: pointer;
    }

    .menu-wrapper:hover {
        background: rgba(38, 196, 185, 0.15);
        border: 1px solid #26c4b9;
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }

    .menu-icon { font-size: 40px; margin-bottom: 10px; }
    .menu-label { 
        font-family: 'Poppins'; font-weight: 700; font-size: 13px; 
        color: white; letter-spacing: 1px; text-transform: uppercase;
    }

    /* Hero Section */
    .hero-container {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 25px;
        padding: 30px; margin-bottom: 30px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIKA HALAMAN ---

if st.session_state.page == 'dashboard':
    # Header Waktu
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    
    st.markdown(f"""
        <div style="text-align: right; color: white; font-family: 'Poppins'; margin-bottom: 20px;">
            <span style="opacity: 0.8;">{now.strftime("%d %B %Y")}</span><br>
            <span style="font-size: 24px; color: #26c4b9; font-weight: bold;">{now.strftime("%H:%M:%S")} WIB</span>
        </div>
    """, unsafe_allow_html=True)

    # Hero Title
    st.markdown("""
        <div class="hero-container">
            <h1 style="font-family: 'Orbitron'; color: white; font-size: 50px; letter-spacing: 10px; margin: 0;">CANE METRIX</h1>
            <p style="color: #26c4b9; font-family: 'Poppins'; font-weight: 700; letter-spacing: 3px;">ACCELERATING QA PERFORMANCE</p>
        </div>
    """, unsafe_allow_html=True)

    # Grid Menu
    items = [
        ("📝", "Input Data"), ("🧮", "Hitung"), ("📅", "Database Harian"),
        ("📊", "Database Bulanan"), ("⚖️", "Rekap Stasiun"), ("📈", "Trend"),
        ("⚙️", "Pengaturan"), ("📥", "Export/Import"), ("👤", "Akun")
    ]

    # Render Grid 3x3
    for i in range(0, len(items), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(items):
                icon, label = items[i+j]
                with cols[j]:
                    # Gabungkan Visual dan Button dalam satu container
                    st.markdown(f"""
                        <div class="menu-wrapper">
                            <div class="menu-icon">{icon}</div>
                            <div class="menu-label">{label}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Button diletakkan tepat setelah markdown untuk menutupi area yang sama
                    if st.button(label, key=f"btn_{label}"):
                        if label == "Hitung":
                            st.session_state.page = 'analisa_tetes'
                            st.rerun()

elif st.session_state.page == 'analisa_tetes':
    # --- HALAMAN ANALISA TETES ---
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="hero-container">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📥 INPUT")
            bx_obs = st.number_input("Brix Teramati", value=8.80, step=0.01)
            suhu_obs = st.number_input("Suhu Teramati (°C)", value=28.3, step=0.1)
        with c2:
            st.subheader("📤 OUTPUT")
            bx_akhir = (bx_obs * 10) + 0.041 # Contoh statis, bisa pake fungsi interpolasi lo tadi
            st.markdown(f"""
                <div style="background: rgba(38,196,185,0.2); padding: 20px; border-radius: 15px; border: 1px solid #26c4b9;">
                    <h1 style="color:#26c4b9; font-family:Orbitron; text-align:center;">{bx_akhir:.3f}</h1>
                    <p style="color:white; text-align:center;">% BRIX AKHIR</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔙 KEMBALI"):
        st.session_state.page = 'dashboard'
        st.rerun()
