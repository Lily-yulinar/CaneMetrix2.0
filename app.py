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

# Refresh 2 detik
st_autorefresh(interval=2000, key="datarefresh")

# Waktu & Jam
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
    try:
        if os.path.exists(file_name):
            with open(file_name, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except:
        return ""
    return ""

# LOAD SEMUA LOGO (URUTAN: KB, SGN, LPP, PTPN)
l_kb = get_base64_logo("kb.png")
l_sgn = get_base64_logo("sgn.png")
l_lpp = get_base64_logo("lpp.png")
l_ptpn = get_base64_logo("ptpn.png")
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

    /* KOTAK LOGO - Paksa Putih & Panjang */
    .partner-container {{ 
        background: white; padding: 15px 35px; border-radius: 15px; 
        display: flex; align-items: center; justify-content: center; gap: 30px; 
        width: fit-content; min-width: 550px;
    }}
    .partner-container img {{ height: 35px; width: auto; object-fit: contain; }}

    .jam-digital {{
        color: #26c4b9; font-size: 55px; font-weight: 900; 
        font-family: 'Poppins'; line-height: 1; text-shadow: 0 0 20px rgba(38, 196, 185, 0.8);
    }}

    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        height: 180px !important; width: 100% !important;
        font-size: 20px !important; font-weight: 700 !important;
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

# --- 3. HEADER (FIX URUTAN LOGO) ---
h1, h2 = st.columns([3, 1])
with h1:
    # Kita rakit HTML logonya secara manual di sini
    logo_html = '<div class="partner-container">'
    if l_kb: logo_html += f'<img src="data:image/png;base64,{l_kb}">'
    if l_sgn: logo_html += f'<img src="data:image/png;base64,{l_sgn}">'
    if l_lpp: logo_html += f'<img src="data:image/png;base64,{l_lpp}">'
    if l_ptpn: logo_html += f'<img src="data:image/png;base64,{l_ptpn}">'
    logo_html += '</div>'
    
    st.markdown(logo_html, unsafe_allow_html=True)

with h2:
    st.markdown(f'''
    <div style="text-align:right;">
        <div style="color:white; opacity:0.8; font-family:Poppins;">{tgl_skrg}</div>
        <div class="jam-digital">{jam_skrg}</div>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. NAVIGATION LOGIC ---
if st.session_state.page == 'dashboard':
    st.markdown(f'''
    <div class="hero-box" style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h1 style="font-family:'Michroma'; color:white; font-size:55px; margin:0; letter-spacing:10px;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:'Poppins'; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{l_cane}" height="180">
    </div>
    ''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.button("📝\nINPUT DATA", on_click=pindah_halaman, args=('input_data',), key="m1")
    with c2: st.button("🧮\nHITUNG ANALISA", on_click=pindah_halaman, args=('analisa_tetes',), key="m2")
    with c3: st.button("📅\nDATABASE HARIAN", on_click=pindah_halaman, args=('db_harian',), key="m3")

    st.write("") # Spasi
    c4, c5, c6 = st.columns(3)
    with c4: st.button("📊\nDATABASE BULANAN", key="m4")
    with c5: st.button("⚖️\nREKAP STASIUN", key="m5")
    with c6: st.button("📈\nTREND", key="m6")

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
                <p style="color:white; font-family:Poppins;">Koreksi Suhu: {kor:+.3f}</p>
            </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.button("🔙 KEMBALI", on_click=pindah_halaman, args=('dashboard',), key="back")
