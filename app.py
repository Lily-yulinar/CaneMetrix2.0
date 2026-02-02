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

logo_ptpn = get_base64_logo("ptpn.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- CSS (UI TETEP CANTIK) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@400;700&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.7), rgba(0, 10, 30, 0.7)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    .partner-box {{
        background: rgba(255, 255, 255, 1);
        padding: 10px 25px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        gap: 20px;
    }}
    .img-partner {{ height: 40px; width: auto; }}

    .hero-container {{
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 35px;
        padding: 25px 10px;
        margin: 15px auto 40px auto;
        max-width: 85%;
        text-align: center;
    }}

    .main-logo-cane {{
        height: 140px; 
        margin-bottom: -15px; 
        filter: brightness(1.2) drop-shadow(0 0 15px rgba(255,255,255,0.4));
    }}

    .title-text {{
        font-family: 'Orbitron'; color: #ffffff;
        font-size: 65px; letter-spacing: 12px; margin: 0;
    }}

    .sub-text {{
        color: #26c4b9; font-family: 'Poppins';
        font-weight: 600; font-size: 16px; letter-spacing: 6px;
        margin-top: -5px;
    }}

    .menu-card {{
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        padding: 30px 10px;
        border-radius: 25px;
        text-align: center;
        color: white;
        height: 200px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.4s;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    }}
    .menu-card:hover {{
        background: rgba(38, 196, 185, 0.2);
        transform: translateY(-10px);
        border: 1px solid #26c4b9;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
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
            <span style="font-size: 26px; color: #26c4b9; font-weight: bold;">{jam_skrg} WIB</span>
        </div>
    """, unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown(f"""
    <div class="hero-container">
        <img src="data:image/png;base64,{logo_cane}" class="main-logo-cane">
        <h1 class="title-text">CANE METRIX</h1>
        <p class="sub-text">Accelerating QA Performance</p>
    </div>
""", unsafe_allow_html=True)

# --- GRID SUB-MENU (SESUAI URUTAN BARU) ---
m1, m2, m3 = st.columns(3)

# Daftar Menu sesuai request
items = [
    ("🧮", "Hitung"),
    ("📝", "Input Data"),
    ("📅", "Database Harian"),
    ("📊", "Database Bulanan"),
    ("⚖️", "Rekap Stasiun"),
    ("📈", "Trend"),
    ("⚙️", "Pengaturan"),
    ("📥", "Export/Import Data"),
    ("👤", "Akun")
]

for i, (icon, text) in enumerate(items):
    with [m1, m2, m3][i % 3]:
        st.markdown(f"""
            <div class="menu-card">
                <div style="font-size: 55px; margin-bottom: 15px;">{icon}</div>
                <div style="font-size: 16px; font-weight: 700; letter-spacing: 2px;">{text.upper()}</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("") 

# --- FOOTER ---
st.markdown("""<div style="margin-top:30px; text-align:center; color:rgba(255,255,255,0.4); font-size:12px;">CaneMetrix 2.0 &copy; 2026 - Quality Assurance System</div>""", unsafe_allow_html=True)
