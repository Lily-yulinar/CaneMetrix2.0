import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")
st_autorefresh(interval=1000, key="datarefresh")

tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Ambil logo lo beb
logo_ptpn = get_base64_logo("ptpn.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- CSS TUNING (BIAR KELIHATAN) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Poppins:wght@400;700&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* KOTAK LOGO PARTNER (Putih Transparan biar logo kelihatan jelas) */
    .partner-box {{
        background: rgba(255, 255, 255, 0.9); /* Putih pekat dikit biar warna logo muncul */
        padding: 15px 30px;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        gap: 30px;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
        margin-bottom: 10px;
    }}
    .img-partner {{ height: 55px; width: auto; object-fit: contain; }}

    /* KOTAK JUDUL UTAMA */
    .hero-container {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 60px 20px;
        margin: 30px auto;
        text-align: center;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }}

    /* LOGO CANEMETRIX (Glow Effect) */
    .main-logo-glow {{
        height: 220px; /* Ukuran Proposional Gede */
        margin-bottom: 20px;
        filter: drop-shadow(0 0 15px rgba(38, 196, 185, 0.8));
    }}

    .title-text {{
        font-family: 'Orbitron'; color: #ffffff;
        font-size: 80px; letter-spacing: 15px; margin: 10px 0;
        text-shadow: 0 0 30px rgba(38, 196, 185, 1);
    }}

    .sub-text {{
        color: #26c4b9; font-family: 'Poppins';
        font-weight: 700; font-size: 20px; letter-spacing: 8px;
        text-transform: uppercase;
    }}

    /* SUB-MENU CARDS */
    .menu-card {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        padding: 40px 20px;
        border-radius: 30px;
        text-align: center;
        color: white;
        height: 260px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.5s;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    }}
    .menu-card:hover {{
        background: rgba(38, 196, 185, 0.25);
        transform: translateY(-15px);
        border: 1px solid #26c4b9;
        box-shadow: 0 0 30px rgba(38, 196, 185, 0.4);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col_head_l, col_head_r = st.columns([2, 1])

with col_head_l:
    st.markdown(f"""
        <div class="partner-box">
            <img src="data:image/png;base64,{logo_ptpn}" class="img-partner">
            <img src="data:image/png;base64,{logo_sgn}" class="img-partner">
            <img src="data:image/png;base64,{logo_lpp}" class="img-partner">
        </div>
    """, unsafe_allow_html=True)

with col_head_r:
    st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], label_visibility="collapsed")
    st.markdown(f"""
        <div style="text-align: right; color: white; font-family: 'Poppins';">
            <span style="font-size: 18px; opacity: 0.8;">{tgl_skrg}</span><br>
            <span style="font-size: 32px; color: #26c4b9; font-weight: bold;">{jam_skrg} WIB</span>
        </div>
    """, unsafe_allow_html=True)

# --- HERO SECTION (KOTAK JUDUL) ---
st.markdown(f"""
    <div class="hero-container">
        <img src="data:image/png;base64,{logo_cane}" class="main-logo-glow">
        <h1 class="title-text">CANE METRIX</h1>
        <p class="sub-text">Accelerating QA Performance</p>
    </div>
""", unsafe_allow_html=True)

# --- SUB-MENU GRID ---
st.write("") # Spacer
m1, m2, m3 = st.columns(3)
items = [
    ("📝", "Input Data"), ("📅", "Database Harian"), ("📊", "Database Bulanan"),
    ("⚖️", "Rekap Stasiun"), ("🧮", "Hitung"), ("👤", "Akun"),
    ("📈", "Trend"), ("⚙️", "Pengaturan"), ("📥", "Export Data")
]

for i, (icon, text) in enumerate(items):
    with [m1, m2, m3][i % 3]:
        st.markdown(f"""
            <div class="menu-card">
                <div style="font-size: 80px; margin-bottom: 20px;">{icon}</div>
                <div style="font-size: 22px; font-weight: 700; letter-spacing: 3px;">{text.upper()}</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("") 

# --- FOOTER ---
st.markdown("""
    <div style="margin-top: 50px; padding: 20px; background: linear-gradient(90deg, #26c4b9, #1a4a7a); border-radius: 20px; text-align: center; color: white;">
        <span style="font-size: 24px; font-weight: bold;">Sistem Quality Assurance - Pabrik Gula Terintegrasi</span>
    </div>
""", unsafe_allow_html=True)
