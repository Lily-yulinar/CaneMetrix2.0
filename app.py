import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- INITIAL CONFIG ---
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

# --- CSS SUPER POP-UP & GIANT LOGO ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Poppins:wght@400;700&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* Partner Logos - No Box, Just Large & Clean */
    .partner-wrapper {{
        display: flex;
        align-items: center;
        gap: 40px;
        padding: 20px 0;
    }}
    .img-giant-partner {{ height: 75px; width: auto; filter: drop-shadow(0 0 10px rgba(255,255,255,0.3)); }}

    /* Main Title Box - Full Impact */
    .hero-container {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 2px solid rgba(38, 196, 185, 0.3);
        border-radius: 50px;
        padding: 80px 20px;
        margin: 50px auto;
        text-align: center;
        box-shadow: 0 0 50px rgba(0, 0, 0, 0.6);
    }}

    .logo-cane-giant {{ 
        height: 320px; /* INI BARU GEDE BEB! */
        margin-bottom: 30px; 
        filter: drop-shadow(0 0 30px rgba(38, 196, 185, 1)); 
    }}
    
    .giant-title {{ 
        font-family: 'Orbitron'; 
        color: #ffffff; 
        font-size: 110px; /* Ukuran Judul Raksasa */
        font-weight: 900;
        letter-spacing: 20px; 
        margin: 0;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.8), 0 0 60px rgba(0, 255, 255, 0.4);
        line-height: 1.2;
    }}

    .giant-subtitle {{ 
        color: #26c4b9; 
        font-family: 'Poppins'; 
        font-weight: 700; 
        font-size: 30px; /* Subtitle juga gue gedein */
        letter-spacing: 10px; 
        text-transform: uppercase;
        margin-top: 15px;
    }}

    /* Sub Menu - Tetap Cakep */
    .menu-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 40px 20px;
        border-radius: 30px;
        text-align: center;
        color: white;
        height: 280px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    
    .menu-card:hover {{
        background: rgba(38, 196, 185, 0.4);
        transform: scale(1.05);
        border: 1px solid #26c4b9;
        box-shadow: 0 0 40px rgba(38, 196, 185, 0.5);
    }}

    .icon-box {{ font-size: 90px; margin-bottom: 20px; }}
    .text-box {{ font-size: 22px; font-weight: 800; letter-spacing: 2px; }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col_head_1, col_head_2 = st.columns([3, 1])

with col_head_1:
    st.markdown(f"""
        <div class="partner-wrapper">
            <img src="data:image/png;base64,{logo_ptpn}" class="img-giant-partner">
            <img src="data:image/png;base64,{logo_sgn}" class="img-giant-partner">
            <img src="data:image/png;base64,{logo_lpp}" class="img-giant-partner">
        </div>
    """, unsafe_allow_html=True)

with col_head_2:
    st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], label_visibility="collapsed")
    st.markdown(f"""
        <div style="text-align:right; color:white; font-family:'Poppins'; margin-top:10px;">
            <b style="font-size:20px;">{tgl_skrg}</b><br>
            <span style="color:#26c4b9; font-size:35px; font-weight:900;">{jam_skrg} WIB</span>
        </div>
    """, unsafe_allow_html=True)

# --- HERO SECTION (KOTAK RAKSASA) ---
st.markdown(f"""
    <div class="hero-container">
        <img src="data:image/png;base64,{logo_cane}" class="logo-cane-giant">
        <h1 class="giant-title">CANE METRIX</h1>
        <p class="giant-subtitle">Accelerating QA Performance</p>
    </div>
""", unsafe_allow_html=True)

# --- SUB MENU SECTION ---
st.write("") # Spacer
m1, m2, m3 = st.columns(3)
menus = [
    ("📝", "Input Data"), ("📅", "Database Harian"), ("📊", "Database Bulanan"),
    ("⚖️", "Rekap Stasiun"), ("🧮", "Hitung"), ("👤", "Akun"),
    ("📈", "Trend"), ("⚙️", "Pengaturan"), ("📥", "Export Data")
]

for i, (icon, text) in enumerate(menus):
    with [m1, m2, m3][i % 3]:
        st.markdown(f"""
            <div class="menu-card">
                <div class="icon-box">{icon}</div>
                <div class="text-box">{text.upper()}</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("") 

# --- FOOTER ---
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #26c4b9, #1a4a7a); padding: 20px; border-radius: 20px; text-align: center; color: white; font-weight: 900; font-size: 26px; margin-top:50px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        TOTAL SAMPEL MASUK HARI INI: 45
    </div>
    """, unsafe_allow_html=True)
