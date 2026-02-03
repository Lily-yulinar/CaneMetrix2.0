import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os
import numpy as np

# --- 1. INITIAL SETTINGS ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# Inisialisasi session state supaya halaman tidak hilang
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# Fungsi sakti buat pindah halaman (pake callback)
def pindah(nama_halaman):
    st.session_state.page = nama_halaman

# --- 2. DATA KOREKSI SUHU (Sesuai Foto Tabel Lo) ---
data_koreksi = {
    25: -0.19, 26: -0.12, 27: -0.05, 28: 0.02, 29: 0.09,
    30: 0.16, 31: 0.24, 32: 0.31, 33: 0.38, 34: 0.46,
    35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86,
    40: 0.94, 41: 1.02, 42: 1.10, 43: 1.18, 44: 1.26,
    45: 1.34, 46: 1.42, 47: 1.5, 48: 1.58, 49: 1.66, 50: 1.72
}

def hitung_koreksi_suhu(suhu_input):
    suhu_list = sorted(data_koreksi.keys())
    koreksi_list = [data_koreksi[s] for s in suhu_list]
    return np.interp(suhu_input, suhu_list, koreksi_list)

# --- 3. CSS CUSTOM (UI Glow Up) ---
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

    /* Styling Tombol agar RESPONSIF */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important; height: 160px !important; width: 100% !important;
        font-size: 18px !important; font-weight: 700 !important; transition: 0.3s;
    }
    
    div.stButton > button:hover {
        border-color: #26c4b9 !important; background: rgba(38, 196, 185, 0.2) !important;
    }

    .jam-digital {
        color: #26c4b9; font-size: 35px; font-weight: 900; 
        font-family: 'Poppins'; text-shadow: 0 0 15px rgba(38, 196, 185, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. HEADER ---
c1, c2 = st.columns([10, 3])
with c2:
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'<div style="text-align:right;"><div class="jam-digital">{now.strftime("%H:%M:%S")}</div></div>', unsafe_allow_html=True)

st_autorefresh(interval=1000, key="global_clock")

# --- 5. LOGIKA NAVIGASI (Sesuai Request Lo) ---

if st.session_state.page == 'dashboard':
    st.markdown('<div class="glass-card"><h1 style="font-family:Michroma; color:white; letter-spacing:5px;">CANE METRIX</h1>'
                '<p style="color:#26c4b9; font-weight:700;">ACCELERATING QA PERFORMANCE</p></div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.button("📝\nINPUT DATA", on_click=pindah, args=('input_data',), key='btn1')
    with col_b:
        # INI TOMBOL YANG LO MAKSUD, BEB!
        st.button("🧮\nHITUNG ANALISA", on_click=pindah, args=('analisa_tetes',), key='btn2')
    with col_c:
        st.button("📅\nDATABASE HARIAN", on_click=pindah, args=('db_harian',), key='btn3')

elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>🧪 ANALISA TETES (% BRIX)</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### 📥 Input Data Lab")
            brix_obs = st.number_input("Brix Teramati", value=8.50, step=0.01, format="%.2f")
            
            # Auto x10
            brix_10x = brix_obs * 10
            st.info(f"Brix Pengenceran (x10): **{brix_10x:.2f}**")
            
            suhu = st.number_input("Suhu (°C)", min_value=25.0, max_value=50.0, value=28.0, step=0.1)
            
        with col_right:
            st.markdown("#### 📊 Hasil Akhir")
            # Logika Interpolasi
            koreksi = hitung_koreksi_suhu(suhu)
            brix_akhir = brix_10x + koreksi
            
            st.markdown(f"""
                <div style="background: rgba(38, 196, 185, 0.1); padding: 30px; border-radius: 20px; border: 2px solid #26c4b9; text-align: center;">
                    <p style="color: white; opacity: 0.8; margin: 0;">% BRIX AKHIR</p>
                    <h1 style="color: white; font-size: 75px; margin: 0;">{brix_akhir:.2f}</h1>
                    <p style="color: #26c4b9; font-weight: bold; margin: 0;">Koreksi: {koreksi:+.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.button("🔙 KEMBALI KE MENU", on_click=pindah, args=('dashboard',), key='btn_back')

# Placeholder biar ga error
elif st.session_state.page in ['input_data', 'db_harian']:
    st.markdown(f"<h2 style='color:white;'>Halaman {st.session_state.page}</h2>", unsafe_allow_html=True)
    st.button("🔙 KEMBALI", on_click=pindah, args=('dashboard',), key='btn_back_alt')
