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

st_autorefresh(interval=2000, key="datarefresh")

# Waktu
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# LOAD LOGO (Urutan sesuai request lo beb)
l_kb = get_base64_logo("kb.png")
l_sgn = get_base64_logo("sgn.png")
l_lpp = get_base64_logo("lpp.png")
l_ptpn = get_base64_logo("ptpn.png")
l_cane = get_base64_logo("canemetrix.png")

# --- 2. CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.8), rgba(0, 10, 30, 0.8)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
    }}

    .partner-box {{ 
        background: white; padding: 15px 30px; border-radius: 12px; 
        display: flex; align-items: center; gap: 25px; width: fit-content;
    }}
    .partner-box img {{ height: 35px; }}

    .jam-digital {{
        color: #26c4b9; font-size: 55px; font-weight: 900; 
        font-family: 'Poppins'; line-height: 1;
    }}

    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important; height: 180px !important; width: 100% !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
h1, h2 = st.columns([3, 1])
with h1:
    # Rakit HTML Logo: KB, SGN, LPP, PTPN
    logos = [l_kb, l_sgn, l_lpp, l_ptpn]
    logo_html = '<div class="partner-box">'
    for img in logos:
        if img:
            logo_html += f'<img src="data:image/png;base64,{img}">'
    logo_html += '</div>'
    st.markdown(logo_html, unsafe_allow_html=True)

with h2:
    st.markdown(f'<div style="text-align:right;"><div style="color:white;">{tgl_skrg}</div><div class="jam-digital">{jam_skrg}</div></div>', unsafe_allow_html=True)

# --- 4. MAIN ---
if st.session_state.page == 'dashboard':
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.05); padding:50px; border-radius:40px; display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h1 style="font-family:'Michroma'; color:white; font-size:50px; margin:0;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-weight:700;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{l_cane}" height="150">
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.button("📝\nINPUT DATA", on_click=pindah_halaman, args=('input_data',))
    with c2: st.button("🧮\nHITUNG ANALISA", on_click=pindah_halaman, args=('analisa_tetes',))
    with c3: st.button("📅\nDATABASE HARIAN", on_click=pindah_halaman, args=('db_harian',))

elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='color:white; text-align:center;'>🧪 KALKULATOR</h2>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI"):
        pindah_halaman('dashboard')
