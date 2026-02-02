import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# Realtime Clock
st_autorefresh(interval=1000, key="datarefresh")

tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# --- FUNGSI MANGGIL LOGO ---
def get_base64_logo(file_name):
    # Nyari file di folder yang sama dengan app.py
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# Panggil logo sesuai request lo (pastiin formatnya .png ya beb)
logo_ptpn = get_base64_logo("ptpn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_sgn = get_base64_logo("sgn.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- CSS CUSTOM ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Poppins:wght@400;700&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.8), rgba(0, 10, 30, 0.8)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Container Logo Partners */
    .partner-card {{
        background: rgba(255, 255, 255, 0.95);
        padding: 8px 15px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        gap: 15px;
    }}
    .img-partner {{ height: 35px; width: auto; }}

    /* Kotak Judul Utama */
    .title-box {{
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 30px;
        padding: 40px;
        margin: 20px auto;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }}

    .logo-cane-main {{ height: 120px; margin-bottom: 15px; filter: drop-shadow(0 0 15px #26c4b9); }}
    .main-title {{ font-family: 'Orbitron'; color: white; font-size: 75px; letter-spacing: 12px; margin: 0; }}
    .sub-title {{ color: #26c4b9; font-family: 'Poppins'; font-weight: 700; letter-spacing: 5px; }}
    </style>
    """, unsafe_allow_html=True)

# --- TAMPILAN HEADER ---
col_l, col_r = st.columns([2, 1])
with col_l:
    st.markdown(f"""
        <div class="partner-card">
            <img src="data:image/png;base64,{logo_ptpn}" class="img-partner">
            <img src="data:image/png;base64,{logo_sgn}" class="img-partner">
            <img src="data:image/png;base64,{logo_lpp}" class="img-partner">
            <span style="color:#333; font-weight:bold; font-size:12px; border-left:2px solid #ddd; padding-left:10px;">PARTNERS</span>
        </div>
    """, unsafe_allow_html=True)

with col_r:
    st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], label_visibility="collapsed")
    st.markdown(f"""<div style="text-align:right; color:white;"><b>{tgl_skrg}</b><br><span style="color:#26c4b9; font-size:24px; font-weight:bold;">{jam_skrg} WIB</span></div>""", unsafe_allow_html=True)

# --- TAMPILAN KOTAK JUDUL ---
st.markdown(f"""
    <div class="title-box">
        <img src="data:image/png;base64,{logo_cane}" class="logo-cane-main">
        <h1 class="main-title">CANE METRIX</h1>
        <p class="sub-title">Accelerating QA Performance</p>
    </div>
""", unsafe_allow_html=True)

# --- MENU GRID ---
# (Looping menu lo yang kemaren taruh sini beb)
