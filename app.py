import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os
import numpy as np

# --- 1. SETUP & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")
st_autorefresh(interval=1000, key="datarefresh")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# Waktu
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# Database Tabel Koreksi (Sesuai Foto Lo Beb)
# x = Suhu, y = Nilai Koreksi
data_suhu = np.array([27, 28, 29, 30, 31, 32, 33, 34, 35, 36])
data_koreksi = np.array([-0.05, 0.02, 0.09, 0.16, 0.24, 0.31, 0.38, 0.46, 0.62, 0.70])

def hitung_interpolasi(suhu_input):
    return np.interp(suhu_input, data_suhu, data_koreksi)

# --- 2. CSS (Balik ke Gaya Glow Lo) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    .stApp {{ background: #0e1117; color: white; }}
    
    .hero-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px;
        padding: 40px; text-align: center; margin-bottom: 30px;
    }}
    .title-glow {{
        font-family: 'Orbitron'; font-size: 55px; font-weight: 900; letter-spacing: 10px;
        text-shadow: 0 0 15px #26c4b9; color: white; margin: 0;
    }}
    .menu-card {{
        background: rgba(255, 255, 255, 0.07); padding: 30px; border-radius: 20px;
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.3s; cursor: pointer; height: 160px;
    }}
    .menu-card:hover {{ border-color: #26c4b9; transform: translateY(-5px); background: rgba(38, 196, 185, 0.1); }}
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA HALAMAN ---

# --- A. DASHBOARD (9 MENU) ---
if st.session_state.page == 'dashboard':
    st.markdown(f"""
        <div style="text-align: right; padding-bottom: 20px;">
            <span style="font-family: 'Poppins'; opacity: 0.8;">{tgl_skrg}</span><br>
            <span style="font-family: 'Poppins'; color: #26c4b9; font-weight: bold; font-size: 20px;">{jam_skrg} WIB</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="hero-container"><h1 class="title-glow">CANE METRIX</h1><p style="color:#26c4b9; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p></div>', unsafe_allow_html=True)

    items = [
        ("📝", "Input Data"), ("🧮", "Hitung"), ("📅", "Database Harian"),
        ("📊", "Database Bulanan"), ("⚖️", "Rekap Stasiun"), ("📈", "Trend"),
        ("⚙️", "Pengaturan"), ("📥", "Export/Import"), ("👤", "Akun")
    ]

    for i in range(0, len(items), 3):
        cols = st.columns(3)
        for j in range(3):
            icon, text = items[i+j]
            with cols[j]:
                # Tombol Hitung yang memicu perubahan halaman
                if text == "Hitung":
                    if st.button(f"{icon}\n{text.upper()}", key=text, use_container_width=True):
                        st.session_state.page = 'sub_menu_hitung'
                        st.rerun()
                else:
                    st.markdown(f'<div class="menu-card"><div style="font-size:40px;">{icon}</div><div style="font-weight:700;">{text.upper()}</div></div>', unsafe_allow_html=True)

# --- B. SUB-MENU HITUNG ---
elif st.session_state.page == 'sub_menu_hitung':
    st.markdown("## 🧮 Menu Perhitungan")
    if st.button("🧪 Hitung Analisa Tetes", use_container_width=True):
        st.session_state.page = 'analisa_tetes'
        st.rerun()
    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.page = 'dashboard'
        st.rerun()

# --- C. HALAMAN ANALISA TETES ---
elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='text-align:center; color:#26c4b9;'>🧪 Perhitungan Analisa Tetes</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Input")
        brix_obs = st.number_input("Brix Teramati", min_value=0.0, step=0.1, format="%.2f")
        suhu_input = st.number_input("Suhu Teramati (°C)", min_value=27.0, max_value=36.0, value=27.5, step=0.1)
        
        # Eksekusi Interpolasi
        koreksi_final = hitung_interpolasi(suhu_input)
        st.success(f"Koreksi Suhu (Interpolasi): {koreksi_final:+.3f}")

    with col2:
        st.markdown("### Output")
        brix_10 = brix_obs * 10
        brix_akhir = brix_10 + koreksi_final
        
        st.metric("Brix Pengenceran (x10)", f"{brix_10:.2f}")
        st.markdown(f"""
            <div style="background:#26c4b9; padding:20px; border-radius:15px; text-align:center; color:#000;">
                <h4 style="margin:0;">% BRIX AKHIR</h4>
                <h1 style="margin:0; font-family:'Orbitron'; font-size:45px;">{brix_akhir:.2f}</h1>
            </div>
        """, unsafe_allow_html=True)

    if st.button("🔙 Kembali"):
        st.session_state.page = 'sub_menu_hitung'
        st.rerun()
