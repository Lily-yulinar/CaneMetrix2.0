import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

def pindah_halaman(nama_halaman):
    st.session_state.page = nama_halaman
    st.rerun()

# Refresh tiap 2 detik biar jam jalan terus
st_autorefresh(interval=2000, key="datarefresh")

# Waktu & Jam WIB
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# LOAD SEMUA LOGO
l_kb = get_base64_logo("kb.png")
l_sgn = get_base64_logo("sgn.png")
l_ptpn = get_base64_logo("ptpn.png")
l_lpp = get_base64_logo("lpp.png")
l_cane = get_base64_logo("canemetrix.png")

# --- 2. CSS UNTUK GANTI FONT (MICHROMA) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    /* Background & Global Font */
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
        font-family: 'Poppins', sans-serif;
    }}

    /* HEADER LOGO URUTAN: KB, SGN, PTPN, LPP */
    .partner-box {{ 
        background: white; padding: 12px 35px; border-radius: 15px; 
        display: flex; align-items: center; gap: 25px; width: fit-content;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }}
    .partner-box img {{ height: 32px; }}

    /* JAM DIGITAL GEDE */
    .jam-digital {{
        color: #26c4b9; font-size: 55px; font-weight: 900; 
        font-family: 'Poppins'; line-height: 1; text-shadow: 0 0 20px rgba(38, 196, 185, 0.8);
    }}

    /* HERO TEXT (FONT GAMBAR 2) */
    .title-cane {{
        font-family: 'Michroma', sans-serif !important; 
        color: white; 
        font-size: 65px; 
        font-weight: 900; 
        letter-spacing: 12px; 
        margin: 0;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }}

    .subtitle-cane {{
        color: #26c4b9; 
        font-family: 'Poppins', sans-serif; 
        font-weight: 700; 
        letter-spacing: 6px; 
        margin-top: -10px;
    }}

    /* CARD BUTTONS */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 25px !important;
        height: 180px !important; width: 100% !important;
        font-size: 20px !important; font-weight: 700 !important;
        transition: 0.3s ease-in-out;
    }}
    div.stButton > button:hover {{
        border: 1px solid #26c4b9 !important;
        background: rgba(38, 196, 185, 0.2) !important;
        transform: translateY(-8px);
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER SECTION ---
h1, h2 = st.columns([3, 1])
with h1:
    # Urutan: KB, SGN, PTPN, LPP
    html_logos = '<div class="partner-box">'
    if l_kb: html_logos += f'<img src="data:image/png;base64,{l_kb}">'
    if l_sgn: html_logos += f'<img src="data:image/png;base64,{l_sgn}">'
    if l_ptpn: html_logos += f'<img src="data:image/png;base64,{l_ptpn}">'
    if l_lpp: html_logos += f'<img src="data:image/png;base64,{l_lpp}">'
    html_logos += '</div>'
    st.markdown(html_logos, unsafe_allow_html=True)

with h2:
    st.markdown(f'<div style="text-align:right;"><div style="color:white; opacity:0.8;">{tgl_skrg}</div><div class="jam-digital">{jam_skrg}</div></div>', unsafe_allow_html=True)

# --- 4. MAIN DASHBOARD ---
if st.session_state.page == 'dashboard':
    # Container Hero
    st.markdown(f'''
    <div style="background:rgba(255,255,255,0.03); backdrop-filter:blur(20px); padding:60px; border-radius:40px; border:1px solid rgba(255,255,255,0.1); display:flex; justify-content:space-between; align-items:center; margin-top:30px; margin-bottom:40px;">
        <div>
            <h1 class="title-cane">CANE METRIX</h1>
            <p class="subtitle-cane">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{l_cane}" height="200">
    </div>
    ''', unsafe_allow_html=True)

    # Menu Utama
    c1, c2, c3 = st.columns(3)
    with c1: st.button("📝\nINPUT DATA", on_click=pindah_halaman, args=('input_data',), key="b1")
    with c2: st.button("🧮\nHITUNG ANALISA", on_click=pindah_halaman, args=('analisa_tetes',), key="b2")
    with c3: st.button("📅\nDATABASE HARIAN", on_click=pindah_halaman, args=('db_harian',), key="b3")

# --- 5. HALAMAN ANALISA (Halaman Baru) ---
elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='color:white; font-family:Michroma; text-align:center; letter-spacing:5px;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    
    st.markdown('<div style="background:rgba(255,255,255,0.05); padding:40px; border-radius:30px; border:1px solid #26c4b9;">', unsafe_allow_html=True)
    # Form analisa lo masukin di sini
    st.write("Form Analisa Siap Digunakan...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔙 KEMBALI KE DASHBOARD", on_click=pindah_halaman, args=('dashboard',)):
        pass
