import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- 1. SETTING DASAR ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# Refresh tiap 1 detik buat Jam
st_autorefresh(interval=1000, key="datarefresh")

# State Halaman (PENTING!)
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

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
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Load Gambar
logo_ptpn = get_base64_logo("ptpn.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 2. STYLE CSS (JAM DIGEDEIN & BOLD) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.8), rgba(0, 10, 30, 0.8)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
    }}

    .partner-box {{ 
        background: white; padding: 10px 40px; border-radius: 10px; 
        display: inline-flex; align-items: center; gap: 40px;
    }}

    /* CSS JAM GEDE & BOLD */
    .jam-container {{
        text-align: right; color: white; font-family: 'Poppins';
    }}
    .jam-digital {{
        color: #26c4b9; font-size: 45px; font-weight: 900; 
        line-height: 1; text-shadow: 0 0 15px rgba(38, 196, 185, 0.6);
    }}
    .tgl-digital {{ font-size: 18px; font-weight: 400; }}

    .hero-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px;
        padding: 40px; margin: 20px 0;
    }}

    .menu-card {{
        background: rgba(255, 255, 255, 0.08); border-radius: 20px;
        height: 180px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; border: 1px solid rgba(255,255,255,0.1);
        transition: 0.3s; position: relative;
    }}
    .menu-card:hover {{ border: 1px solid #26c4b9; background: rgba(38, 196, 185, 0.1); transform: translateY(-5px); }}

    /* Button Overlay */
    .stButton > button {{
        position: absolute; width: 100%; height: 100%; top: 0; left: 0;
        background: transparent !important; color: transparent !important; border: none !important;
    }}
    
    .back-btn button {{
        background: #26c4b9 !important; color: white !important; font-weight: bold !important;
        position: relative !important; width: auto !important; height: auto !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER (Logo & Jam) ---
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown(f'''<div class="partner-box">
        <img src="data:image/png;base64,{logo_ptpn}" height="30">
        <img src="data:image/png;base64,{logo_sgn}" height="30">
        <img src="data:image/png;base64,{logo_lpp}" height="30">
    </div>''', unsafe_allow_html=True)
with c2:
    st.markdown(f'''<div class="jam-container">
        <div class="tgl-digital">{tgl_skrg}</div>
        <div class="jam-digital">{jam_skrg} WIB</div>
    </div>''', unsafe_allow_html=True)

# --- 4. LOGIC HALAMAN ---

if st.session_state.page == 'dashboard':
    # JUDUL UTAMA
    st.markdown(f'''
    <div class="hero-container" style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="font-family:'Michroma'; color:white; font-size:50px; margin:0; letter-spacing:8px;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-weight:700; letter-spacing:4px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{logo_cane}" height="150">
    </div>
    ''', unsafe_allow_html=True)

    # GRID MENU
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="menu-card"><span style="font-size:50px;">📝</span><br><b style="color:white;">INPUT DATA</b></div>', unsafe_allow_html=True)
        st.button("A", key="m1")
    
    with col2:
        # INI TOMBOL KERAMATNYA
        st.markdown('<div class="menu-card" style="border: 1px solid #26c4b9;"><span style="font-size:50px;">🧮</span><br><b style="color:white;">HITUNG ANALISA</b></div>', unsafe_allow_html=True)
        if st.button("B", key="m2"):
            st.session_state.page = 'kalkulator'
            st.rerun()

    with col3:
        st.markdown('<div class="menu-card"><span style="font-size:50px;">📅</span><br><b style="color:white;">DATABASE HARIAN</b></div>', unsafe_allow_html=True)
        st.button("C", key="m3")

elif st.session_state.page == 'kalkulator':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Michroma;'>🧪 KALKULATOR ANALISA TETES</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="hero-container">', unsafe_allow_html=True)
        k1, k2 = st.columns(2)
        with k1:
            st.markdown("<h3 style='color:#26c4b9;'>Input Data</h3>", unsafe_allow_html=True)
            bx_in = st.number_input("Brix Teramati", value=8.80, format="%.2f")
            su_in = st.number_input("Suhu (°C)", value=28.3, format="%.1f")
            koreksi = hitung_interpolasi(su_in)
        with k2:
            hasil = (bx_in * 10) + koreksi
            st.markdown(f'''
                <div style="background:rgba(38,196,185,0.2); padding:30px; border-radius:20px; border:2px solid #26c4b9; text-align:center;">
                    <h4 style="color:white;">HASIL % BRIX AKHIR</h4>
                    <h1 style="color:#26c4b9; font-size:60px; font-family:Michroma;">{hasil:.3f}</h1>
                    <p style="color:white;">Faktor Koreksi Suhu: {koreksi:+.3f}</p>
                </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="back-btn" style="text-align:center;">', unsafe_allow_html=True)
    if st.button("🔙 BALIK KE DASHBOARD"):
        st.session_state.page = 'dashboard'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
