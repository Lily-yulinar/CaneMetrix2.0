import streamlit as st
import datetime
import pytz
import base64
import os

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# --- 2. FUNGSI LOGO & DATA ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_kb = get_base64_logo("kb.png")
logo_cane = get_base64_logo("canemetrix.png")

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
    if suhu_user < suhu_keys[0]: return data_koreksi[suhu_keys[0]]
    if suhu_user > suhu_keys[-1]: return data_koreksi[suhu_keys[-1]]
    for i in range(len(suhu_keys) - 1):
        x0, x1 = suhu_keys[i], suhu_keys[i+1]
        if x0 < suhu_user < x1:
            y0, y1 = data_koreksi[x0], data_koreksi[x1]
            return y0 + (suhu_user - x0) * (y1 - y0) / (x1 - x0)
    return 0.0

# --- 3. CSS (SIMPLER & STRONGER) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    .header-logo-box {{
        background: white; padding: 10px 20px; border-radius: 15px; 
        display: inline-flex; align-items: center; gap: 15px;
    }}
    .header-logo-box img {{ height: 35px; width: auto; }}

    .hero-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px;
        padding: 40px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center;
    }}

    /* Styling tombol asli Streamlit agar terlihat seperti card */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: white !important;
        height: 180px !important;
        width: 100% !important;
        transition: 0.3s !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    div.stButton > button:hover {{
        background: rgba(38, 196, 185, 0.2) !important;
        border-color: #26c4b9 !important;
        box-shadow: 0 0 25px rgba(38, 196, 185, 0.4) !important;
        transform: translateY(-8px) !important;
    }}
    
    /* Menghilangkan border fokus tombol */
    div.stButton > button:focus {{
        box-shadow: 0 0 25px rgba(38, 196, 185, 0.4) !important;
        border-color: #26c4b9 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. FRAGMENT JAM ---
@st.fragment(run_every="1s")
def jam_realtime():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f"""
        <div style="text-align: right; color: white; font-family: 'Poppins';">
            {now.strftime("%d %B %Y")}<br>
            <span style="font-family:'Orbitron'; color:#26c4b9; font-size:24px; font-weight:bold;">
                {now.strftime("%H:%M:%S")} WIB
            </span>
        </div>
    """, unsafe_allow_html=True)

# --- 5. LOGIKA HALAMAN ---

if st.session_state.page == 'dashboard':
    # Top Bar
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f'''<div class="header-logo-box">
            <img src="data:image/png;base64,{logo_ptpn}"><img src="data:image/png;base64,{logo_sgn}">
            <img src="data:image/png;base64,{logo_lpp}"><img src="data:image/png;base64,{logo_kb}">
        </div>''', unsafe_allow_html=True)
    with c2:
        jam_realtime()

    # Hero
    st.markdown(f'''<div class="hero-container">
        <div>
            <h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{logo_cane}" style="height:150px; filter:drop-shadow(0 0 15px #26c4b9);">
    </div>''', unsafe_allow_html=True)

    # Grid Menu - PAKAI TOMBOL ASLI TANPA OVERLAY RUMIT
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Kita taruh icon di atas tombol menggunakan markdown sederhana
        st.markdown("<div style='text-align:center; margin-bottom:-50px; position:relative; z-index:10; pointer-events:none;'><h1>📝</h1></div>", unsafe_allow_html=True)
        if st.button("INPUT DATA", key="btn_input", use_container_width=True):
            st.toast("Fitur Input Data segera hadir!")
        
    with col2:
        st.markdown("<div style='text-align:center; margin-bottom:-50px; position:relative; z-index:10; pointer-events:none;'><h1>🧮</h1></div>", unsafe_allow_html=True)
        if st.button("HITUNG ANALISA", key="btn_hitung", use_container_width=True):
            st.session_state.page = 'analisa_tetes'
            st.rerun()

    with col3:
        st.markdown("<div style='text-align:center; margin-bottom:-50px; position:relative; z-index:10; pointer-events:none;'><h1>📅</h1></div>", unsafe_allow_html=True)
        if st.button("DATABASE HARIAN", key="btn_harian", use_container_width=True):
            st.toast("Fitur Database segera hadir!")

elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            bx = st.number_input("Brix Teramati", value=8.80, step=0.01)
            sh = st.number_input("Suhu (°C)", value=28.3, step=0.1)
            kor = hitung_interpolasi(sh)
            st.info(f"Koreksi Suhu: {kor:+.3f}")
        with cy:
            hasil = (bx * 10) + kor
            st.markdown(f"""
                <div style="background:rgba(38,196,185,0.1); padding:30px; border-radius:20px; border:2px solid #26c4b9; text-align:center;">
                    <h1 style="color:#26c4b9; font-size:60px; font-family:Orbitron;">{hasil:.3f}</h1>
                    <p style="color:white;">% BRIX AKHIR</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔙 KEMBALI KE DASHBOARD"):
        st.session_state.page = 'dashboard'
        st.rerun()
