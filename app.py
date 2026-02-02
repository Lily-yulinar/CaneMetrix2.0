import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- KONFIGURASI ---
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

# Panggil file yang udah lo upload beb
logo_ptpn = get_base64_logo("ptpn.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- CSS PROPOSIONAL ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Poppins:wght@400;700&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.8), rgba(0, 10, 30, 0.8)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* Logo Partners di Kiri (Tanpa Teks, Lebih Gede) */
    .partner-row {{
        background: rgba(255, 255, 255, 0.95);
        padding: 12px 25px;
        border-radius: 15px;
        display: inline-flex;
        align-items: center;
        gap: 25px; /* Spasi antar logo */
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .img-partner {{ height: 50px; width: auto; }} /* Ukuran Partner Proposional */

    /* Kotak Judul & Logo Utama */
    .title-box {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 35px;
        padding: 60px 20px;
        margin: 40px auto;
        text-align: center;
    }}

    .logo-cane-main {{ 
        height: 200px; /* Logo CaneMetrix Gede & Proposional */
        margin-bottom: 25px; 
        filter: drop-shadow(0 0 20px rgba(38, 196, 185, 0.8)); 
    }}
    
    .main-title {{ 
        font-family: 'Orbitron'; color: white; 
        font-size: 85px; letter-spacing: 15px; margin: 0;
        text-shadow: 0 0 20px rgba(255,255,255,0.4);
    }}

    .sub-title {{ color: #26c4b9; font-family: 'Poppins'; font-weight: 700; font-size: 22px; letter-spacing: 6px; }}

    /* SUB MENU CARD (Biar Muncul Lagi) */
    .menu-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 35px 20px;
        border-radius: 25px;
        text-align: center;
        color: white;
        height: 250px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: 0.4s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }}
    
    .menu-card:hover {{
        background: rgba(38, 196, 185, 0.3);
        transform: translateY(-12px);
        border: 1px solid #26c4b9;
        box-shadow: 0 10px 30px rgba(0,255,255,0.2);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_l, col_r = st.columns([2, 1])
with col_l:
    st.markdown(f"""
        <div class="partner-row">
            <img src="data:image/png;base64,{logo_ptpn}" class="img-partner">
            <img src="data:image/png;base64,{logo_sgn}" class="img-partner">
            <img src="data:image/png;base64,{logo_lpp}" class="img-partner">
        </div>
    """, unsafe_allow_html=True)

with col_r:
    st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], label_visibility="collapsed")
    st.markdown(f"""<div style="text-align:right; color:white; font-family:'Poppins';"><b>{tgl_skrg}</b><br><span style="color:#26c4b9; font-size:28px; font-weight:bold;">{jam_skrg} WIB</span></div>""", unsafe_allow_html=True)

# --- MAIN BOX ---
st.markdown(f"""
    <div class="title-box">
        <img src="data:image/png;base64,{logo_cane}" class="logo-cane-main">
        <h1 class="main-title">CANE METRIX</h1>
        <p class="sub-title">Accelerating QA Performance</p>
    </div>
""", unsafe_allow_html=True)

# --- GRID SUB-MENU (INI DIA BEB!) ---
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
                <div style="font-size: 80px; margin-bottom: 15px;">{icon}</div>
                <div style="font-size: 20px; font-weight: 700; letter-spacing: 2px;">{text.upper()}</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("") # Spacer biar rapi di mobile

# --- FOOTER ---
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #26c4b9, #1a4a7a); padding: 15px; border-radius: 15px; text-align: center; color: white; font-weight: bold; font-size: 22px; margin-top:30px;">
        Jumlah sampel masuk hari ini: 45
    </div>
    """, unsafe_allow_html=True)
