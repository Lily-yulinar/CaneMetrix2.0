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

# REFRESH 1 DETIK (Biar jam lebih smooth dan gak telat 2 detik)
st_autorefresh(interval=1000, key="datarefresh")

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

# LOAD LOGO
l_kb = get_base64_logo("kb.png")
l_sgn = get_base64_logo("sgn.png")
l_ptpn = get_base64_logo("ptpn.png")
l_lpp = get_base64_logo("lpp.png")
l_cane = get_base64_logo("canemetrix.png")

# --- 2. CSS CUSTOM (FIX SUBMENU & JAM) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
    }}

    /* HEADER LOGO */
    .partner-box {{ 
        background: white; padding: 12px 30px; border-radius: 15px; 
        display: flex; align-items: center; gap: 25px; width: fit-content;
    }}
    .partner-box img {{ height: 32px; }}

    /* JAM DIGITAL (GLOWING GREEN) */
    .jam-digital {{
        color: #26c4b9; font-size: 55px; font-weight: 900; 
        font-family: 'Poppins'; line-height: 1; text-shadow: 0 0 15px rgba(38, 196, 185, 0.6);
    }}

    /* HERO TEXT MICHROMA */
    .title-cane {{
        font-family: 'Michroma', sans-serif !important; 
        color: white; font-size: 55px; font-weight: 900; 
        letter-spacing: 12px; margin: 0;
    }}
    .subtitle-cane {{
        color: #26c4b9; font-family: 'Poppins'; font-weight: 700; 
        letter-spacing: 5px; margin-top: -10px;
    }}

    /* FIX TOMBOL SUBMENU AGAR KEMBALI SEPERTI GAMBAR 1 */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 25px !important;
        height: 200px !important;
        width: 100% !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        text-align: center !important;
        display: block !important; /* Paksa tumpuk vertikal */
        transition: all 0.3s ease-in-out;
    }}

    div.stButton > button:hover {{
        border: 1px solid #26c4b9 !important;
        background: rgba(38, 196, 185, 0.2) !important;
        transform: translateY(-10px) !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
h1, h2 = st.columns([3, 1])
with h1:
    html_logos = '<div class="partner-box">'
    if l_kb: html_logos += f'<img src="data:image/png;base64,{l_kb}">'
    if l_sgn: html_logos += f'<img src="data:image/png;base64,{l_sgn}">'
    if l_ptpn: html_logos += f'<img src="data:image/png;base64,{l_ptpn}">'
    if l_lpp: html_logos += f'<img src="data:image/png;base64,{l_lpp}">'
    html_logos += '</div>'
    st.markdown(html_logos, unsafe_allow_html=True)

with h2:
    st.markdown(f'''
    <div style="text-align:right;">
        <div style="color:white; opacity:0.8; font-family:Poppins;">{tgl_skrg}</div>
        <div class="jam-digital">{jam_skrg} <span style="font-size:20px;">WIB</span></div>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. DASHBOARD ---
if st.session_state.page == 'dashboard':
    st.markdown(f'''
    <div style="background:rgba(255,255,255,0.03); backdrop-filter:blur(15px); padding:55px; border-radius:40px; border:1px solid rgba(255,255,255,0.1); display:flex; justify-content:space-between; align-items:center; margin-top:30px; margin-bottom:50px;">
        <div>
            <h1 class="title-cane">CANE METRIX</h1>
            <p class="subtitle-cane">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{l_cane}" height="180">
    </div>
    ''', unsafe_allow_html=True)

    # SUB MENU (Layout 3 Kolom)
    # Gunakan format teks \n\n agar ikon dan tulisan terpisah baris
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1: 
        st.button("📄\n\nINPUT DATA", on_click=pindah_halaman, args=('input_data',), key="btn_input")
    with c2: 
        st.button("🧮\n\nHITUNG ANALISA", on_click=pindah_halaman, args=('analisa_tetes',), key="btn_calc")
    with c3: 
        st.button("📅\n\nDATABASE HARIAN", on_click=pindah_halaman, args=('db_harian',), key="btn_db")

# --- 5. HALAMAN LAIN ---
elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='color:white; font-family:Michroma; text-align:center;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI", on_click=pindah_halaman, args=('dashboard',)):
        pass
