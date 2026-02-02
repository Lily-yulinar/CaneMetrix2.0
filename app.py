import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- 1. SETUP HALAMAN ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")
st_autorefresh(interval=1000, key="datarefresh")

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

# --- 2. CSS DENGAN EFEK GLOW ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.75), rgba(0, 10, 30, 0.75)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* Container Logo Partner */
    .partner-box {{
        background: rgba(255, 255, 255, 1);
        padding: 8px 20px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .img-partner {{ height: 35px; width: auto; }}

    /* Hero Box (Glassmorphism) */
    .hero-container {{
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px;
        padding: 25px;
        margin: 10px auto 30px auto;
        text-align: center;
        max-width: 90%;
    }}

    .main-logo-cane {{
        height: 120px; 
        margin-bottom: -10px;
        filter: brightness(1.2) drop-shadow(0 0 15px rgba(38, 196, 185, 0.8));
    }}

    /* EFEK JUDUL GLOW */
    .title-text {{
        font-family: 'Orbitron'; 
        color: white;
        font-size: 65px; 
        letter-spacing: 12px; 
        margin: 0;
        font-weight: 900;
        /* Neon Glow Effect */
        text-shadow: 
            0 0 7px #fff,
            0 0 10px #fff,
            0 0 21px #fff,
            0 0 42px #26c4b9,
            0 0 82px #26c4b9,
            0 0 92px #26c4b9,
            0 0 102px #26c4b9,
            0 0 151px #26c4b9;
    }}

    .sub-text {{
        color: #26c4b9; 
        font-family: 'Poppins';
        font-weight: 700; 
        font-size: 18px; 
        letter-spacing: 5px;
        margin-top: 5px;
        text-transform: uppercase;
    }}

    /* Menu Cards */
    .menu-card {{
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        padding: 25px 10px;
        border-radius: 20px;
        text-align: center;
        color: white;
        height: 180px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.3s ease-in-out;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        margin-bottom: 20px;
    }}
    .menu-card:hover {{
        background: rgba(38, 196, 185, 0.2);
        transform: translateY(-8px);
        border: 1px solid #26c4b9;
        box-shadow: 0 0 20px rgba(38, 196, 185, 0.4);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. TAMPILAN HEADER ---
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown(f"""
        <div class="partner-box">
            <img src="data:image/png;base64,{logo_ptpn}" class="img-partner">
            <img src="data:image/png;base64,{logo_sgn}" class="img-partner">
            <img src="data:image/png;base64,{logo_lpp}" class="img-partner">
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], label_visibility="collapsed")
    st.markdown(f"""
        <div style="text-align: right; color: white; font-family: 'Poppins';">
            <span style="font-size: 14px; opacity: 0.7;">{tgl_skrg}</span><br>
            <span style="font-size: 24px; color: #26c4b9; font-weight: bold;">{jam_skrg} WIB</span>
        </div>
    """, unsafe_allow_html=True)

# --- 4. HERO SECTION ---
st.markdown(f"""
    <div class="hero-container">
        <img src="data:image/png;base64,{logo_cane}" class="main-logo-cane">
        <h1 class="title-text">CANE METRIX</h1>
        <p class="sub-text">Accelerating QA Performance</p>
    </div>
""", unsafe_allow_html=True)

# --- 5. GRID MENU ---
items = [
    ("📝", "Input Data"), ("🧮", "Hitung"), ("📅", "Database Harian"),
    ("📊", "Database Bulanan"), ("⚖️", "Rekap Stasiun"), ("📈", "Trend"),
    ("⚙️", "Pengaturan"), ("📥", "Export/Import Data"), ("👤", "Akun")
]

for i in range(0, len(items), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(items):
            icon, text = items[i+j]
            with cols[j]:
                st.markdown(f"""
                    <div class="menu-card">
                        <div style="font-size: 50px; margin-bottom: 10px;">{icon}</div>
                        <div style="font-size: 16px; font-weight: 700; letter-spacing: 1px;">{text.upper()}</div>
                    </div>
                """, unsafe_allow_html=True)
