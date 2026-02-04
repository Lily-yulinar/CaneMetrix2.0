import streamlit as st
import datetime
import pytz
import base64
import os

# --- 1. INITIAL CONFIG (Wajib di Paling Atas) ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide", initial_sidebar_state="collapsed")

# Inisialisasi State Halaman
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# --- 2. FUNGSI LOAD ASSETS ---
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

# --- 3. LOGIKA HITUNG ---
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

# --- 4. CSS (DIBERSIHKAN DARI TUMPANG TINDIH) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.88), rgba(0, 10, 30, 0.88)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-attachment: fixed;
    }}

    .header-box {{ background: white; padding: 8px 15px; border-radius: 12px; display: inline-flex; gap: 10px; }}
    .header-box img {{ height: 30px; width: auto; }}

    .hero-card {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 25px;
        padding: 40px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;
    }}

    /* CSS Tombol Navigasi agar Jadi Card */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: white !important;
        height: 180px !important;
        width: 100% !important;
        transition: 0.3s !important;
        font-family: 'Poppins' !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        display: flex !important;
        flex-direction: column !important;
    }}

    div.stButton > button:hover {{
        border-color: #26c4b9 !important;
        background: rgba(38, 196, 185, 0.15) !important;
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }}
    
    .clock-digital {{ font-family: 'Orbitron'; color: #26c4b9; font-size: 24px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. FRAGMENT JAM (ANTI FLICKER) ---
@st.fragment(run_every="1s")
def render_jam():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f"""
        <div style="text-align: right; color: white;">
            <div style="font-family: 'Poppins'; opacity: 0.8;">{now.strftime("%d %B %Y")}</div>
            <div class="clock-digital">{now.strftime("%H:%M:%S")} WIB</div>
        </div>
    """, unsafe_allow_html=True)

# --- 6. ROUTING HALAMAN ---

if st.session_state.page == 'dashboard':
    # Top Section
    c_logo, c_jam = st.columns([2, 1])
    with c_logo:
        st.markdown(f'''<div class="header-box">
            <img src="data:image/png;base64,{logo_ptpn}"><img src="data:image/png;base64,{logo_sgn}">
            <img src="data:image/png;base64,{logo_lpp}"><img src="data:image/png;base64,{logo_kb}">
        </div>''', unsafe_allow_html=True)
    with c_jam:
        render_jam()

    # Hero Banner
    st.markdown(f'''<div class="hero-card">
        <div>
            <h1 style="font-family:Orbitron; color:white; font-size:50px; margin:0; letter-spacing:2px;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:4px; margin:0;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{logo_cane}" style="height:140px; filter: drop-shadow(0 0 10px #26c4b9);">
    </div>''', unsafe_allow_html=True)

    # Menu Grid (Clean Navigation)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝\n\nINPUT DATA", key="nav_in"):
            st.toast("Module Input belum tersedia")
        
    with col2:
        # Tombol ini sekarang jadi trigger utama
        if st.button("🧮\n\nHITUNG ANALISA", key="nav_calc"):
            st.session_state.page = 'analisa_tetes'
            st.rerun()

    with col3:
        if st.button("📅\n\nDATABASE HARIAN", key="nav_db"):
            st.toast("Module Database belum tersedia")

elif st.session_state.page == 'analisa_tetes':
    # Tombol Back yang solid
    if st.button("⬅ KEMBALI KE DASHBOARD"):
        st.session_state.page = 'dashboard'
        st.rerun()

    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron; margin:20px 0;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    
    # Kalkulator UI
    with st.container():
        st.markdown('<div class="hero-card" style="display:block;">', unsafe_allow_html=True)
        cl1, cl2 = st.columns(2)
        with cl1:
            brix = st.number_input("Brix Teramati", value=8.80, format="%.2f", step=0.01)
            suhu = st.number_input("Suhu Teramati (°C)", value=28.3, format="%.1f", step=0.1)
            koreksi = hitung_interpolasi(suhu)
            st.info(f"Koreksi Suhu: {koreksi:+.3f}")
        with cl2:
            hasil = (brix * 10) + koreksi
            st.markdown(f"""
                <div style="background:rgba(38,196,185,0.1); padding:40px; border-radius:20px; border:2px solid #26c4b9; text-align:center;">
                    <p style="color:white; font-family:Poppins; margin:0;">% BRIX AKHIR</p>
                    <h1 style="color:#26c4b9; font-size:70px; font-family:Orbitron; margin:10px 0;">{hasil:.3f}</h1>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
