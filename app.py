import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- 1. SETTING PAGE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

def pindah_halaman(nama_halaman):
    st.session_state.page = nama_halaman
    st.rerun()

# Auto-refresh jam tiap 2 detik
st_autorefresh(interval=2000, key="datarefresh")

# Waktu & Jam
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# Fungsi Load Gambar (Cek file ada atau tidak)
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# LOAD LOGO (Urutan: KB, SGN, PTPN, LPP)
l_kb = get_base64_logo("kb.png")
l_sgn = get_base64_logo("sgn.png")
l_ptpn = get_base64_logo("ptpn.png")
l_lpp = get_base64_logo("lpp.png")
l_cane = get_base64_logo("canemetrix.png")

# --- 2. CSS CUSTOM ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.8), rgba(0, 10, 30, 0.8)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
    }}

    /* KOTAK LOGO PUTIH (FIX 4 LOGO) */
    .partner-box {{ 
        background: white; padding: 12px 30px; border-radius: 12px; 
        display: flex; align-items: center; gap: 25px; width: fit-content;
        min-width: 500px; justify-content: center;
    }}
    .partner-box img {{ height: 35px; width: auto; object-fit: contain; }}

    .jam-digital {{
        color: #26c4b9; font-size: 55px; font-weight: 900; 
        font-family: 'Poppins'; line-height: 1; text-shadow: 0 0 20px rgba(38, 196, 185, 0.8);
    }}

    /* TOMBOL MENU */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important; height: 180px !important; width: 100% !important;
        font-size: 18px !important; font-weight: 700 !important;
    }}
    div.stButton > button:hover {{
        border: 1px solid #26c4b9 !important;
        background: rgba(38, 196, 185, 0.2) !important;
        transform: translateY(-5px);
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
h1, h2 = st.columns([3, 1])
with h1:
    # Susun Logo secara manual di dalam container putih
    html_logos = '<div class="partner-box">'
    for img_data in [l_kb, l_sgn, l_ptpn, l_lpp]:
        if img_data:
            html_logos += f'<img src="data:image/png;base64,{img_data}">'
    html_logos += '</div>'
    
    st.markdown(html_logos, unsafe_allow_html=True)
    
    # Debugging kecil (akan hilang kalau logo KB muncul)
    if not l_kb:
        st.caption("⚠️ kb.png belum terdeteksi di folder")

with h2:
    st.markdown(f'''
    <div style="text-align:right;">
        <div style="color:white; opacity:0.8; font-family:Poppins;">{tgl_skrg}</div>
        <div class="jam-digital">{jam_skrg}</div>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. DASHBOARD ---
if st.session_state.page == 'dashboard':
    st.markdown(f'''
    <div style="background:rgba(255,255,255,0.05); backdrop-filter:blur(15px); padding:50px; border-radius:40px; border:1px solid rgba(255,255,255,0.1); display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
        <div>
            <h1 style="font-family:'Michroma'; color:white; font-size:55px; margin:0; letter-spacing:10px;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:'Poppins'; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{l_cane}" height="180">
    </div>
    ''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.button("📝\nINPUT DATA", on_click=pindah_halaman, args=('input_data',))
    with c2: st.button("🧮\nHITUNG ANALISA", on_click=pindah_halaman, args=('analisa_tetes',))
    with c3: st.button("📅\nDATABASE HARIAN", on_click=pindah_halaman, args=('db_harian',))

# --- HALAMAN LAIN (Contoh) ---
elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='color:white; font-family:Michroma; text-align:center;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI"):
        pindah_halaman('dashboard')
