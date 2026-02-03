import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- 1. SETTING PAGE & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

def pindah_halaman(nama_halaman):
    st.session_state.page = nama_halaman
    st.rerun()

# Refresh 2 detik biar jam update
st_autorefresh(interval=2000, key="datarefresh")

# Waktu
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# Tabel Koreksi
data_koreksi = {
    25: -0.19, 26: -0.12, 27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16,
    31: 0.24, 32: 0.31, 33: 0.38, 34: 0.46, 35: 0.54, 36: 0.62,
    37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94, 41: 1.02, 42: 1.10,
    43: 1.18, 44: 1.26, 45: 1.34, 46: 1.42, 47: 1.50, 48: 1.58,
    49: 1.66, 50: 1.72
}

def hitung_interpolasi(suhu_user):
    suhu_keys = sorted(data_koreksi.keys())
    if suhu_user in data_koreksi: return data_koreksi[suhu_user]
    for i in range(len(suhu_keys) - 1):
        x0, x1 = suhu_keys[i], suhu_keys[i+1]
        if x0 < suhu_user < x1:
            y0, y1 = data_koreksi[x0], data_koreksi[x1]
            return y0 + (suhu_user - x0) * (y1 - y0) / (x1 - x0)
    return 0.0

def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None # Balikin None kalau file ga ada

# LOAD SEMUA LOGO (Pastiin nama file beneran 'kb.png', 'sgn.png', dll)
logo_kb = get_base64_logo("kb.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_ptpn = get_base64_logo("ptpn.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 2. CSS CUSTOM ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.8), rgba(0, 10, 30, 0.8)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
    }}

    /* KOTAK LOGO LEBIH PANJANG UNTUK 4 LOGO */
    .partner-box {{ 
        background: white; padding: 15px 40px; border-radius: 15px; 
        display: inline-flex; align-items: center; gap: 30px; 
        min-width: 600px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}

    .jam-digital {{
        color: #26c4b9; font-size: 55px; font-weight: 900; 
        font-family: 'Poppins'; line-height: 1; text-shadow: 0 0 20px rgba(38, 196, 185, 0.8);
    }}

    /* TOMBOL MENU CARD */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        height: 180px !important; width: 100% !important;
        font-size: 20px !important; font-weight: 700 !important;
        display: flex !important; flex-direction: column !important;
    }}

    div.stButton > button:hover {{
        border: 1px solid #26c4b9 !important;
        background: rgba(38, 196, 185, 0.2) !important;
        transform: translateY(-5px) !important;
    }}

    .hero-box {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 40px;
        padding: 50px; margin-bottom: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER (URUTAN: KB, SGN, LPP, PTPN) ---
h1, h2 = st.columns([3, 1])
with h1:
    # Buat string HTML untuk logo yang ada saja
    html_logos = ""
    for l_data in [logo_kb, logo_sgn, logo_lpp, logo_ptpn]:
        if l_data:
            html_logos += f'<img src="data:image/png;base64,{l_data}" height="35">'
    
    st.markdown(f'''<div class="partner-box">{html_logos}</div>''', unsafe_allow_html=True)
    
    # Alert kalau KB belum ada (Bisa dihapus kalau udah ok)
    if not logo_kb:
        st.warning("⚠️ File 'kb.png' belum terdeteksi di folder!")

with h2:
    st.markdown(f'<div style="text-align:right;"><div style="color:white; opacity:0.8; font-family:Poppins;">{tgl_skrg}</div><div class="jam-digital">{jam_skrg}</div></div>', unsafe_allow_html=True)

# --- 4. NAVIGATION ---
if st.session_state.page == 'dashboard':
    st.markdown(f'''
    <div class="hero-box" style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h1 style="font-family:'Michroma'; color:white; font-size:55px; margin:0; letter-spacing:10px;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:'Poppins'; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{logo_cane}" height="180">
    </div>
    ''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.button("📝\nINPUT DATA", on_click=pindah_halaman, args=('input_data',), key="m1")
    with c2: st.button("🧮\nHITUNG ANALISA", on_click=pindah_halaman, args=('analisa_tetes',), key="m2")
    with c3: st.button("📅\nDATABASE HARIAN", on_click=pindah_halaman, args=('db_harian',), key="m3")

elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Michroma; margin-top:20px;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    st.markdown('<div class="hero-box">', unsafe_allow_html=True)
    k1, k2 = st.columns(2)
    with k1:
        bx = st.number_input("Brix Teramati", value=8.80, format="%.2f")
        sh = st.number_input("Suhu Teramati (°C)", value=28.3, format="%.1f")
        kor = hitung_interpolasi(sh)
    with k2:
        hasil = (bx * 10) + kor
        st.markdown(f'''
            <div style="background:rgba(38,196,185,0.2); padding:40px; border-radius:25px; border:2px solid #26c4b9; text-align:center;">
                <h1 style="color:#26c4b9; font-size:75px; font-family:Michroma; margin:0;">{hasil:.3f}</h1>
                <p style="color:white;">Koreksi: {kor:+.3f}</p>
            </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.button("🔙 KEMBALI", on_click=pindah_halaman, args=('dashboard',), key="back")
