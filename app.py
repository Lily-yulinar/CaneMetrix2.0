import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os
import numpy as np

# --- 1. SETTING PAGE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# Inisialisasi Session State agar halaman tidak reset
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# FUNGSI CALLBACK: Ini rahasia biar tombolnya "sadar" pas diklik
def set_page(name):
    st.session_state.page = name

# --- 2. DATA KOREKSI SUHU (Interpolasi dari Foto Lo) ---
data_koreksi = {
    25: -0.19, 26: -0.12, 27: -0.05, 28: 0.02, 29: 0.09,
    30: 0.16, 31: 0.24, 32: 0.31, 33: 0.38, 34: 0.46,
    35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86,
    40: 0.94, 41: 1.02, 42: 1.10, 43: 1.18, 44: 1.26,
    45: 1.34, 46: 1.42, 47: 1.50, 48: 1.58, 49: 1.66, 50: 1.72
}

def get_koreksi(temp):
    s_keys = sorted(data_koreksi.keys())
    s_vals = [data_koreksi[k] for k in s_keys]
    return float(np.interp(temp, s_keys, s_vals))

# --- 3. CSS CUSTOM (UI & Button Style) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        padding: 30px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }

    /* Styling Tombol agar lebih responsif */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important; height: 160px !important; width: 100% !important;
        font-size: 18px !important; font-weight: 700 !important;
    }
    
    div.stButton > button:active {
        transform: scale(0.98);
        border-color: #26c4b9 !important;
    }

    .jam-digital {
        color: #26c4b9; font-size: 35px; font-weight: 900;
        font-family: 'Poppins'; text-shadow: 0 0 15px rgba(38, 196, 185, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. HEADER (Waktu Otomatis) ---
c_h1, c_h2 = st.columns([10, 3])
with c_h2:
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'<div style="text-align:right;"><div class="jam-digital">{now.strftime("%H:%M:%S")}</div></div>', unsafe_allow_html=True)

st_autorefresh(interval=1000, key="refresh_clock")

# --- 5. NAVIGASI UTAMA ---

if st.session_state.page == 'dashboard':
    st.markdown('<div class="glass-card"><h1 style="font-family:Michroma; color:white; letter-spacing:5px;">CANE METRIX</h1>'
                '<p style="color:#26c4b9; font-weight:700;">ACCELERATING QA PERFORMANCE</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("📝\nINPUT DATA", on_click=set_page, args=('input',), key='btn_in')
    with col2:
        # Tombol Hitung Analisa dengan Callback
        st.button("🧮\nHITUNG ANALISA", on_click=set_page, args=('analisa',), key='btn_an')
    with col3:
        st.button("📅\nDATABASE HARIAN", on_click=set_page, args=('db',), key='btn_db')

elif st.session_state.page == 'analisa':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        L, R = st.columns(2)
        
        with L:
            st.write("### Input Lab")
            b_teramati = st.number_input("Brix Teramati", value=8.50, step=0.01, format="%.2f")
            
            # Auto-pengenceran x10
            b_pengenceran = b_teramati * 10
            st.success(f"Brix Pengenceran (x10): **{b_pengenceran:.2f}**")
            
            suhu = st.number_input("Suhu (°C)", min_value=25.0, max_value=50.0, value=28.0, step=0.1)
            
        with R:
            st.write("### Hasil")
            # Hitung Koreksi & Brix Akhir
            koreksi_nilai = get_koreksi(suhu)
            brix_persen = b_pengenceran + koreksi_nilai
            
            st.markdown(f"""
                <div style="background: rgba(38, 196, 185, 0.1); padding: 30px; border-radius: 20px; border: 2px solid #26c4b9; text-align: center;">
                    <p style="color: white; opacity: 0.8; margin: 0;">% BRIX AKHIR</p>
                    <h1 style="color: white; font-size: 80px; margin: 0;">{brix_persen:.2f}</h1>
                    <p style="color: #26c4b9; font-weight: bold; margin: 0;">Koreksi Suhu: {koreksi_nilai:+.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.button("🔙 KEMBALI", on_click=set_page, args=('dashboard',), key='back_an')

elif st.session_state.page == 'input':
    st.write("Halaman Input Data")
    st.button("🔙 KEMBALI", on_click=set_page, args=('dashboard',), key='back_in')

elif st.session_state.page == 'db':
    st.write("Halaman Database")
    st.button("🔙 KEMBALI", on_click=set_page, args=('dashboard',), key='back_db_page')
