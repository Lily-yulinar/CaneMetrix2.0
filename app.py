import streamlit as st
import datetime
import pytz
import base64
import os
import time

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# --- 2. DATA & LOGIKA ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Load Semua Gambar
logo_ptpn = get_base64_logo("ptpn.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_kb = get_base64_logo("kb.png")
logo_cane = get_base64_logo("canemetrix.png")

# Tabel Koreksi Suhu
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

# --- 3. CSS (KUNCI UKURAN & LAYOUT) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* Kunci Ukuran Logo di Header */
    .header-logo-container img {{
        height: 35px; width: auto; object-fit: contain;
    }}

    .hero-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px;
        padding: 40px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;
        max-height: 300px; overflow: hidden;
    }}

    .logo-cane-large {{ 
        height: 180px !important; width: auto !important; 
        filter: drop-shadow(0 0 15px #26c4b9); 
    }}

    /* Card Menu Hover & Click Fix */
    .menu-wrapper {{
        position: relative; height: 180px; margin-bottom: 10px;
    }}

    .menu-card-container {{
        position: absolute; top:0; left:0; right:0; bottom:0;
        background: rgba(255, 255, 255, 0.07); backdrop-filter: blur(10px);
        border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        transition: 0.3s ease-in-out; z-index: 1;
    }}

    .menu-wrapper:hover .menu-card-container {{
        background: rgba(38, 196, 185, 0.2); border: 1px solid #26c4b9;
        box-shadow: 0 0 25px rgba(38, 196, 185, 0.4); transform: translateY(-8px);
    }}

    .stButton > button {{
        position: absolute !important; width: 100% !important; height: 180px !important;
        background: transparent !important; color: transparent !important;
        border: none !important; z-index: 10 !important; cursor: pointer !important;
    }}
    
    .clock-text {{ font-family: 'Orbitron'; color: #26c4b9; font-size: 22px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. DASHBOARD PAGE ---
if st.session_state.page == 'dashboard':
    # Header Section
    c_top1, c_top2 = st.columns([2, 1])
    with c_top1:
        st.markdown(f'''
            <div class="header-logo-container" style="background:white; padding:10px 20px; border-radius:15px; display:inline-flex; gap:20px; align-items:center;">
                <img src="data:image/png;base64,{logo_ptpn}">
                <img src="data:image/png;base64,{logo_sgn}">
                <img src="data:image/png;base64,{logo_lpp}">
                <img src="data:image/png;base64,{logo_kb}">
            </div>''', unsafe_allow_html=True)
    
    with c_top2:
        # Jam Realtime tanpa flicker seluruh layar
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.datetime.now(tz)
        tgl_str = now.strftime("%d %B %Y")
        jam_placeholder = st.empty()
        jam_placeholder.markdown(f'''
            <div style="text-align: right; color: white; font-family: 'Poppins';">
                {tgl_str}<br><span class="clock-text">{now.strftime("%H:%M:%S")} WIB</span>
            </div>''', unsafe_allow_html=True)

    # Hero Section (Kunci ukuran teks & logo)
    st.markdown(f'''
        <div class="hero-container">
            <div style="flex: 1;">
                <h1 style="font-family:Orbitron; color:white; font-size:50px; margin:0; line-height:1;">CANE METRIX</h1>
                <p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:4px; margin-top:10px;">ACCELERATING QA PERFORMANCE</p>
            </div>
            <div style="flex: 0;">
                <img src="data:image/png;base64,{logo_cane}" class="logo-cane-large">
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Menu Grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="menu-wrapper"><div class="menu-card-container"><div style="font-size:45px;">📝</div><div style="color:white; font-weight:700;">INPUT DATA</div></div>', unsafe_allow_html=True)
        if st.button("", key="btn_input"): st.toast("Segera Hadir!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="menu-wrapper"><div class="menu-card-container"><div style="font-size:45px;">🧮</div><div style="color:white; font-weight:700;">HITUNG ANALISA</div></div>', unsafe_allow_html=True)
        if st.button("", key="btn_hitung"):
            st.session_state.page = 'analisa_tetes'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="menu-wrapper"><div class="menu-card-container"><div style="font-size:45px;">📅</div><div style="color:white; font-weight:700;">DATABASE HARIAN</div></div>', unsafe_allow_html=True)
        st.button("", key="btn_harian")
        st.markdown('</div>', unsafe_allow_html=True)

    # Tambah delay kecil biar jam update tapi nggak bikin flicker gila-gilaan
    time.sleep(0.1)
    st.rerun()

# --- 5. HALAMAN KALKULATOR ---
elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron; margin-bottom:30px;'>🧪 PERHITUNGAN ANALISA TETES</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1])
        with c1:
            bx_obs = st.number_input("Brix Teramati", value=8.80, format="%.2f", step=0.01)
            suhu_obs = st.number_input("Suhu Teramati (°C)", value=28.3, format="%.1f", step=0.1)
            koreksi = hitung_interpolasi(suhu_obs)
            st.info(f"Koreksi Suhu: {koreksi:+.3f}")
        with c2:
            bx_akhir = (bx_obs * 10) + koreksi
            st.markdown(f"""
                <div style="background: rgba(38, 196, 185, 0.15); padding: 30px; border-radius: 20px; border: 2px solid #26c4b9; text-align:center;">
                    <h4 style="color:white; font-family:Poppins; margin:0;">% BRIX AKHIR</h4>
                    <h1 style="color:#26c4b9; font-size:60px; font-family:Orbitron; margin:10px 0;">{bx_akhir:.3f}</h1>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔙 KEMBALI KE DASHBOARD", use_container_width=True):
        st.session_state.page = 'dashboard'
        st.rerun()
